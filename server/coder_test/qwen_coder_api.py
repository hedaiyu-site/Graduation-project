from openai import OpenAI

"""初版框架---------需连接neo4j数据库------------还需上下文记忆功能"""


class KnowledgeGraphEnhancedAPI:
    def __init__(self):
        self.client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key='ms-15949e37-45b3-485c-8521-5527d98dbdc4'
        )

        # 初始化知识图谱连接
        self.kg_connector = self.init_knowledge_graph()

    def init_knowledge_graph(self):
        # 实现知识图谱连接逻辑
        pass

    def query_with_knowledge_graph(self, user_query):
        # 从知识图谱中检索相关信息
        kg_context = self.search_konwledge_graph(user_query)

        # 构建增强的消息列表
        messages = [
            {
                'role': 'system',
                'content': f'你是一个有用的助手。以下是来自我们知识库的相关上下文：{kg_context}'
            },
            {
                'role': 'user',
                'content': user_query
            }
        ]

        response = self.client.chat.completions.create(
            model='Qwen/Qwen3-Coder-480B-A35B-Instruct',
            messages=messages,
            stream=True
        )

        return response
