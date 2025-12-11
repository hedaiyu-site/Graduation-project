import os
import re
import frontmatter
from neo4j import GraphDatabase
import spacy
from typing import List, Dict, Tuple, Set
import json
from pathlib import Path


class MDKnowledgeGraphBuilder:
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """
        初始化知识图谱构建器

        Args:
            neo4j_uri: Neo4j数据库地址，如 "bolt://localhost:7687"
            neo4j_user: 用户名
            neo4j_password: 密码
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

        # 加载spacy模型（用于实体识别）
        try:
            self.nlp = spacy.load("zh_core_web_sm")  # 中文
        except:
            try:
                self.nlp = spacy.load("en_core_web_sm")  # 英文
            except:
                self.nlp = None
                print("未找到spacy模型，将使用基于规则的方法")

        # 实体和关系缓存
        self.entities_cache = set()
        self.relationships_cache = []

    def extract_markdown_content(self, md_file_path: str) -> Dict:
        """
        提取Markdown文件内容，包括frontmatter和正文

        Args:
            md_file_path: Markdown文件路径

        Returns:
            包含文件信息的字典
        """
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析frontmatter
            post = frontmatter.loads(content)

            # 获取文件名和路径
            file_name = os.path.basename(md_file_path)
            file_path = os.path.abspath(md_file_path)

            # 提取纯文本内容（去除markdown标记）
            text_content = self._clean_markdown(post.content)

            return {
                'file_name': file_name,
                'file_path': file_path,
                'frontmatter': post.metadata,
                'content': text_content,
                'full_content': content,
                'title': post.metadata.get('title', file_name.replace('.md', '')),
                'tags': post.metadata.get('tags', []),
                'categories': post.metadata.get('categories', []),
                'created_date': post.metadata.get('date', post.metadata.get('created', ''))
            }
        except Exception as e:
            print(f"解析文件 {md_file_path} 时出错: {e}")
            return None

    def _clean_markdown(self, text: str) -> str:
        """
        清理Markdown格式，提取纯文本

        Args:
            text: Markdown文本

        Returns:
            清理后的纯文本
        """
        # 移除代码块
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`.*?`', '', text)

        # 移除图片和链接
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)

        # 移除标题标记
        text = re.sub(r'#{1,6}\s*', '', text)

        # 移除列表标记
        text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)

        # 移除引用
        text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)

        # 移除表格标记
        text = re.sub(r'\|.*?\|', '', text)

        # 移除多余的空格和换行
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\s{2,}', ' ', text)

        return text.strip()

    def extract_entities_rule_based(self, text: str) -> List[str]:
        """
        基于规则提取实体

        Args:
            text: 文本内容

        Returns:
            实体列表
        """
        entities = []

        # 提取大写字母开头的单词（专有名词）
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', text)
        entities.extend(proper_nouns)

        # 提取引号内的内容
        quoted_entities = re.findall(r'["\'](.*?)["\']', text)
        entities.extend(quoted_entities)

        # 提取冒号前的关键词
        colon_entities = re.findall(r'^(.*?):', text, re.MULTILINE)
        entities.extend([e.strip() for e in colon_entities])

        # 去重和清理
        entities = list(set([e.strip() for e in entities if len(e.strip()) > 1]))

        return entities

    def extract_entities_spacy(self, text: str) -> List[str]:
        """
        使用spacy提取实体

        Args:
            text: 文本内容

        Returns:
            实体列表
        """
        if not self.nlp:
            return self.extract_entities_rule_based(text)

        doc = self.nlp(text)
        entities = []

        # 提取命名实体
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT', 'EVENT', 'WORK_OF_ART']:
                entities.append(ent.text)

        # 提取名词短语
        for chunk in doc.noun_chunks:
            if len(chunk.text) > 2 and chunk.text.lower() not in ['this', 'that', 'these', 'those']:
                entities.append(chunk.text)

        # 去重
        return list(set(entities))

    def extract_relationships(self, text: str, entities: List[str]) -> List[Tuple]:
        """
        提取实体间的关系

        Args:
            text: 文本内容
            entities: 实体列表

        Returns:
            关系列表，每个关系为 (实体1, 关系类型, 实体2)
        """
        relationships = []

        # 常见关系关键词
        relation_keywords = [
            '是', '属于', '包含', '包括', '有', '需要', '使用', '基于',
            '的', '和', '与', '或', '及', '等',
            'is', 'has', 'contains', 'includes', 'uses', 'based on',
            'of', 'and', 'or', 'with', 'in'
        ]

        # 寻找实体共现的句子
        sentences = re.split(r'[。！？.!?]', text)

        for sentence in sentences:
            if len(sentence.strip()) < 10:
                continue

            # 找到句子中出现的实体
            sentence_entities = [e for e in entities if e in sentence]

            if len(sentence_entities) >= 2:
                # 提取实体间的关系
                for i in range(len(sentence_entities)):
                    for j in range(i + 1, len(sentence_entities)):
                        entity1 = sentence_entities[i]
                        entity2 = sentence_entities[j]

                        # 提取两个实体之间的文本
                        start = sentence.find(entity1) + len(entity1)
                        end = sentence.find(entity2)

                        if start < end:
                            between_text = sentence[start:end].strip()
                            # 检查是否有关系关键词
                            for keyword in relation_keywords:
                                if keyword in between_text:
                                    relationships.append((entity1, keyword, entity2))
                                    break

        return relationships

    def process_markdown_file(self, md_file_path: str) -> Dict:
        """
        处理单个Markdown文件

        Args:
            md_file_path: Markdown文件路径

        Returns:
            处理结果
        """
        # 提取内容
        doc_info = self.extract_markdown_content(md_file_path)
        if not doc_info:
            return None

        # 提取实体
        if self.nlp:
            entities = self.extract_entities_spacy(doc_info['content'])
        else:
            entities = self.extract_entities_rule_based(doc_info['content'])

        # 提取关系
        relationships = self.extract_relationships(doc_info['content'], entities)

        # 添加到缓存
        for entity in entities:
            self.entities_cache.add(entity)

        self.relationships_cache.extend(relationships)

        return {
            'doc_info': doc_info,
            'entities': entities,
            'relationships': relationships
        }

    def create_neo4j_schema(self):
        """
        在Neo4j中创建索引和约束
        """
        with self.driver.session() as session:
            # 创建约束（确保实体唯一性）
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (d:Document) REQUIRE d.file_path IS UNIQUE")

            # 创建索引
            session.run("CREATE INDEX IF NOT EXISTS FOR (e:Entity) ON (e.type)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (d:Document) ON (d.title)")

    def save_to_neo4j(self, processed_docs: List[Dict]):
        """
        将处理结果保存到Neo4j

        Args:
            processed_docs: 处理过的文档列表
        """
        with self.driver.session() as session:
            # 创建模式
            self.create_neo4j_schema()

            # 清空现有数据（可选）
            # session.run("MATCH (n) DETACH DELETE n")

            # 保存文档节点
            for doc in processed_docs:
                if not doc:
                    continue

                doc_info = doc['doc_info']

                # 创建文档节点
                session.run("""
                    MERGE (d:Document {
                        file_path: $file_path,
                        title: $title,
                        file_name: $file_name
                    })
                    SET d.content = $content,
                        d.tags = $tags,
                        d.categories = $categories,
                        d.created_date = $created_date
                """,
                            file_path=doc_info['file_path'],
                            title=doc_info['title'],
                            file_name=doc_info['file_name'],
                            content=doc_info['content'][:500],  # 只保存前500字符
                            tags=doc_info['tags'],
                            categories=doc_info['categories'],
                            created_date=doc_info['created_date'])

            # 保存实体节点
            for entity in self.entities_cache:
                session.run("""
                    MERGE (e:Entity {name: $name})
                    SET e.type = 'Concept'
                """, name=entity)

            # 保存文档-实体关系
            for doc in processed_docs:
                if not doc:
                    continue

                doc_info = doc['doc_info']
                entities = doc['entities']

                for entity in entities:
                    session.run("""
                        MATCH (d:Document {file_path: $file_path})
                        MATCH (e:Entity {name: $entity_name})
                        MERGE (d)-[:CONTAINS_ENTITY]->(e)
                    """,
                                file_path=doc_info['file_path'],
                                entity_name=entity)

            # 保存实体间关系
            for rel in self.relationships_cache:
                entity1, relation_type, entity2 = rel

                session.run("""
                    MATCH (e1:Entity {name: $entity1})
                    MATCH (e2:Entity {name: $entity2})
                    MERGE (e1)-[r:RELATES_TO {type: $relation_type}]->(e2)
                """,
                            entity1=entity1,
                            entity2=entity2,
                            relation_type=relation_type)

    def visualize_graph(self, output_file: str = "knowledge_graph.html"):
        """
        生成知识图谱的可视化HTML文件

        Args:
            output_file: 输出HTML文件路径
        """
        try:
            from pyvis.network import Network
        except ImportError:
            print("请安装pyvis: pip install pyvis")
            return

        # 创建网络图
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

        # 添加实体节点
        entity_nodes = list(self.entities_cache)
        for i, entity in enumerate(entity_nodes):
            net.add_node(i, label=entity, color="#3498db", shape="dot", size=20)

        # 添加关系边
        edge_set = set()  # 用于去重
        for rel in self.relationships_cache:
            entity1, relation_type, entity2 = rel
            if entity1 in entity_nodes and entity2 in entity_nodes:
                idx1 = entity_nodes.index(entity1)
                idx2 = entity_nodes.index(entity2)
                edge_key = f"{idx1}-{idx2}-{relation_type}"
                if edge_key not in edge_set:
                    net.add_edge(idx1, idx2, title=relation_type, color="#95a5a6")
                    edge_set.add(edge_key)

        # 生成HTML
        net.show(output_file)
        print(f"可视化图已保存到 {output_file}")

    def query_entities(self, entity_name: str) -> List[Dict]:
        """
        查询实体及其关系

        Args:
            entity_name: 实体名称

        Returns:
            查询结果
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:Entity {name: $name})
                OPTIONAL MATCH (e)-[r]-(related)
                RETURN e, r, related
                LIMIT 50
            """, name=entity_name)

            return [record.data() for record in result]

    def query_documents_with_entity(self, entity_name: str) -> List[Dict]:
        """
        查询包含特定实体的文档

        Args:
            entity_name: 实体名称

        Returns:
            文档列表
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Document)-[:CONTAINS_ENTITY]->(e:Entity {name: $name})
                RETURN d.title as title, d.file_path as file_path
            """, name=entity_name)

            return [record.data() for record in result]

    def process_directory(self, directory_path: str) -> List[Dict]:
        """
        处理目录下的所有Markdown文件

        Args:
            directory_path: 目录路径

        Returns:
            处理结果列表
        """
        processed_docs = []

        # 遍历目录
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.md'):
                    md_file_path = os.path.join(root, file)
                    print(f"处理文件: {md_file_path}")

                    try:
                        result = self.process_markdown_file(md_file_path)
                        if result:
                            processed_docs.append(result)
                    except Exception as e:
                        print(f"处理文件 {md_file_path} 时出错: {e}")

        return processed_docs

    def export_statistics(self, output_file: str = "kg_statistics.json"):
        """
        导出知识图谱统计信息

        Args:
            output_file: 输出文件路径
        """
        stats = {
            "total_entities": len(self.entities_cache),
            "total_relationships": len(self.relationships_cache),
            "entities_sample": list(self.entities_cache)[:20],
            "relationships_sample": self.relationships_cache[:20]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        print(f"统计信息已导出到 {output_file}")
        return stats

    def close(self):
        """关闭数据库连接"""
        self.driver.close()


def main():
    # 配置参数
    NEO4J_URI = "bolt://localhost:7687"  # Neo4j地址
    NEO4J_USER = "neo4j"  # 用户名
    NEO4J_PASSWORD = "password"  # 密码
    MD_DIRECTORY = "./markdown_files"  # Markdown文件目录

    # 创建构建器实例
    kg_builder = MDKnowledgeGraphBuilder(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # 处理目录下的所有Markdown文件
        print("开始处理Markdown文件...")
        processed_docs = kg_builder.process_directory(MD_DIRECTORY)

        print(f"处理完成！共处理 {len(processed_docs)} 个文件")
        print(f"提取到 {len(kg_builder.entities_cache)} 个实体")
        print(f"提取到 {len(kg_builder.relationships_cache)} 个关系")

        # 保存到Neo4j
        print("保存到Neo4j数据库...")
        kg_builder.save_to_neo4j(processed_docs)

        # 生成可视化
        print("生成可视化...")
        kg_builder.visualize_graph()

        # 导出统计信息
        stats = kg_builder.export_statistics()
        print(f"知识图谱统计: {stats}")

        # 示例查询
        if kg_builder.entities_cache:
            sample_entity = list(kg_builder.entities_cache)[0]
            print(f"\n查询实体 '{sample_entity}' 的文档:")
            docs = kg_builder.query_documents_with_entity(sample_entity)
            for doc in docs[:3]:
                print(f"  - {doc['title']}")

    finally:
        kg_builder.close()


if __name__ == "__main__":
    main()