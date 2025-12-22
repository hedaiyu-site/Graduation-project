import os

import redis
from neo4j import GraphDatabase
from dotenv import load_dotenv


# 加载环境变量
load_dotenv()

# redis连接配置
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# neo4j连接配置
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')


class DatabaseManager:
    def __init__(self):
        # 连接redis
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB,
            decode_responses=True  # 自动解码返回字符串
        )

        # 连接neo4j
        self.neo4j_driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

    def test_redis_connection(self):
        """测试 redis 连接"""
        try:
            self.redis_client.ping()
            print("Redis 连接成功")
            return True
        except redis.ConnectionError:
            print("Redis 连接失败")
            return False

    def test_neo4j_connection(self):
        """测试 neo4j 连接"""
        try:
            with self.neo4j_driver.session() as session:
                session.run("RETURN 1")
            print("Neo4j 连接成功")
            return True
        except Exception as e:
            print(f"Neo4j 连接失败：{e}")
            return False

    def cache_neo4j_query_result(self, query, cache_key, ttl=3600):
        """
        缓存 Neo4j 查询结果到 Redis
        :param query: Neo4j 查询语句
        :param cache_key: Redis 缓存键
        :param ttl: 缓存过期时间
        :return: 查询结果
        """
        # 先检查 Redis 中是否有缓存
        cached_result = self.redis_client.get(cache_key)
        if cached_result:
            print(f"从 Redis 缓存获取数据：{cache_key}")
            return eval(cached_result)  # 后续换成实际的反序列化方式

        # 如果没有缓存，查询Neo4j
        print(f"查询 Neo4j 并缓存结果：{cache_key}")
        with self.neo4j_driver.session() as session:
            result = session.run(query)
            data = [record.data for record in result]

            # 将结果缓存到 Redis
            self.redis_client.setex(cache_key, ttl, str(data))
            return data

    def create_user_with_cache(self, name, email):
        """
        在 Neo4j 中创建用户，并在 Redis 中缓存用户信息
        :param name: 姓名
        :param email: 邮箱
        :return: 用户信息
        """
        user_key = f"user: {email}"

        # 检查 Redis 缓存
        cached_user = self.redis_client.get(user_key)
        if cached_user:
            print(f"从缓存获取用户：{email}")
            return eval(cached_user)

        # 在 Neo4j中创建用户
        query = f"""
        CREATE (u: User {name: $name, email: $email, create_at: timestamp()})
        RETURN u
        """

        with self.neo4j_driver.session() as session:
            result = session.run(query, name, email)
            user_data = result.single()[0]

            # 缓存到Redis(24小时过期)
            user_info = {
                'name': user_data['name'],
                'email': email['email'],
                'create_at': user_data['create_at']
            }
            self.redis_client.setex(user_key, 86400, str(user_info))

            return user_info

    def get_user_friends(self, user_email):
        """
        获取用户的朋友列表，使用Redis缓存
        :param user_email:
        :return:
        """
        cache_key = f"user:{user_email}:friends"

        # 检查缓存
        cached = self.redis_client.get(cache_key)
        if cached:
            return eval(cached)

        # 查询Neo4j
        query = """
        MATCH (u:User {email: $email})-[:FRIEND]->(f:User)
        RETURN f.name as name,f.email as email
        LIMIT 50
        """

        with self.neo4j_driver.session() as session:
            result = session.run(query, email=user_email)
            friends = [record.data() for record in result]

            # 缓存结果(5分钟过期)
            self.redis_client.setex(cache_key,300,str(friends))
            return friends

    def clear_cache_pattern(self, pattern):
        """
        清除匹配模式的 Redis 缓存
        :param pattern:
        :return:
        """
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
            print(f"清除缓存：{len(keys)}个键")

    def close(self):
        """关闭所有连接"""
        self.redis_client.close()
        self.neo4j_driver.close()
        print("所有数据库已关闭")


# 使用示例
if __name__ == '__main__':
    # 创建数据库管理器
    db = DatabaseManager()

    try:
        # 测试连接
        db.test_redis_connection()
        db.test_neo4j_connection()

        # 示例1：创建用户并缓存
        user = db.create_user_with_cache("张三", "zhangsan@example.com")
        print(f"创建用户:{user}")

        # 示例2：查询 Neo4j 并缓存结果
        neo4j_query = "MATCH (n) RETURN count(n) as node_count"
        result = db.cache_neo4j_query_result(neo4j_query, "node_count_cache", 60)
        print(f"节点数量:{result}")

        # 示例3：设置 Redis 键值
        db.redis_client.set("test_key", "test_value")
        print(f"Redis 测试值：{db.redis_client.get('test_key')}")

    finally:
        db.close()