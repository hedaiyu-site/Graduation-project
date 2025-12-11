class KnowledgeGraphAnalyzer:
    """知识图谱分析工具"""

    def __init__(self, driver):
        self.driver = driver

    def find_central_entities(self, limit: int = 10):
        """查找中心性最高的实体"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:Entity)
                OPTIONAL MATCH (e)-[r]-()
                WITH e, count(r) as degree
                RETURN e.name as entity, degree
                ORDER BY degree DESC
                LIMIT $limit
            """, limit=limit)

            return [record.data() for record in result]

    def find_communities(self):
        """发现实体社区"""
        with self.driver.session() as session:
            result = session.run("""
                CALL gds.labelPropagation.stream({
                    nodeQuery: 'MATCH (e:Entity) RETURN id(e) as id',
                    relationshipQuery: 'MATCH (e1:Entity)-[r:RELATES_TO]-(e2:Entity) RETURN id(e1) as source, id(e2) as target',
                    relationshipWeightProperty: null
                })
                YIELD nodeId, communityId
                RETURN communityId, collect(gds.util.asNode(nodeId).name) as entities
                ORDER BY size(entities) DESC
            """)

            return [record.data() for record in result]

    def search_related_paths(self, entity1: str, entity2: str, max_depth: int = 3):
        """查找两个实体之间的路径"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH path = shortestPath((e1:Entity {name: $entity1})-[*1..$max_depth]-(e2:Entity {name: $entity2}))
                RETURN [node in nodes(path) | node.name] as path_nodes,
                       [rel in relationships(path) | rel.type] as relationships
            """, entity1=entity1, entity2=entity2, max_depth=max_depth)

            return [record.data() for record in result]