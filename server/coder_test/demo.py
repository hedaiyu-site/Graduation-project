from openai import OpenAI

"""----------------------需要添加上下文记忆功能------------------"""

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1',
    api_key='ms-15949e37-45b3-485c-8521-5527d98dbdc4', # ModelScope Token
)

response = client.chat.completions.create(
    model='Qwen/Qwen3-Coder-480B-A35B-Instruct', # ModelScope Model-Id
    messages=[
        {
            'role': 'system',
            'content': 'You are a helpful assistant.'
        },
        {
            'role': 'user',
            'content': '我想学习python知识，现在我有一个本地的neo4j知数据库（存放着python的知识点）。我应该怎么将你连接到我本地的知识图谱中呢'
        }
    ],
    stream=True
)

for chunk in response:
    if chunk.choices:
        print(chunk.choices[0].delta.content, end='', flush=True)