import re
from typing import Tuple, List

from md_kg_builder import MDKnowledgeGraphBuilder
class EnhancedKnowledgeGraphBuilder(MDKnowledgeGraphBuilder):
    """增强的知识图谱构建器"""

    def extract_hierarchical_relations(self, text: str) -> List[Tuple]:
        """提取层次关系（如分类、子类）"""
        patterns = [
            (r'(\w+)包括(\w+)', 'INCLUDES'),
            (r'(\w+)属于(\w+)', 'BELONGS_TO'),
            (r'(\w+)分为(\w+)', 'DIVIDED_INTO'),
        ]

        relations = []
        for pattern, rel_type in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) == 2:
                    relations.append((match[0], rel_type, match[1]))

        return relations

    def extract_temporal_relations(self, text: str) -> List[Tuple]:
        """提取时间关系"""
        # 提取日期和事件
        date_pattern = r'\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2}'
        dates = re.findall(date_pattern, text)

        # 简单的时间关系提取
        relations = []
        sentences = text.split('。')

        for sentence in sentences:
            for date in dates:
                if date in sentence:
                    # 找到日期相关的内容
                    entities = self.extract_entities_spacy(sentence)
                    for entity in entities:
                        relations.append((entity, 'OCCUR_AT', date))

        return relations

    def create_advanced_schema(self):
        """创建更丰富的图模式"""
        with self.driver.session() as session:
            # 添加更多节点类型
            session.run("CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (t:Topic) ON (t.name)")

            # 添加更多关系类型
            session.run("""
                CREATE CONSTRAINT IF NOT EXISTS 
                FOR ()-[r:IS_A]-() 
                REQUIRE r.type IS NOT NULL
            """)


# 使用示例
enhanced_builder = EnhancedKnowledgeGraphBuilder(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="12345678"
)