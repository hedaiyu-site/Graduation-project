<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="top-nav">
      <div class="logo">
        <img src="./assets/textxpython_92740.svg" alt="Python Learning" />
        <span style="font-size: large">Python学习智能辅导系统</span>
      </div>
      <div class="nav-right">
        <button class="nav-btn">用户信息</button>
        <button class="nav-btn">设置</button>
        <button class="nav-btn">帮助</button>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 左侧导航面板 -->
      <aside class="left-panel">
        <nav class="side-nav">
          <a href="#" class="nav-item">
            <span class="icon">📚</span>
            <span>学习路径</span>
          </a>
          <a href="#" class="nav-item">
            <span class="icon">🧠</span>
            <span>知识图谱导航</span>
          </a>
          <a href="#" class="nav-item">
            <span class="icon">📝</span>
            <span>历史记录</span>
          </a>
          <a href="#" class="nav-item">
            <span class="icon">⭐</span>
            <span>收藏夹</span>
          </a>
        </nav>
      </aside>

      <!-- 中央主内容区 -->
      <section class="center-panel">
        <!-- 聊天对话界面 -->
        <div class="chat-container">
          <h3>智能辅导助手</h3>
          <div class="chat-history">
            <div v-for="msg in mockChatHistory" :key="msg.id" :class="['chat-message', msg.sender]">
              <div class="message-content">{{ msg.message }}</div>
            </div>
          </div>
          <div class="chat-input">
            <input type="text" placeholder="输入你的问题..." />
            <button>发送</button>
          </div>
        </div>

        <!-- 代码编辑器 -->
        <div class="code-editor">
          <h3>代码实践</h3>
          <div class="editor-header">
            <div class="file-tabs">
              <span class="tab active">main.py</span>
              <span class="tab">test.py</span>
            </div>
            <div class="editor-actions">
              <button>运行</button>
              <button>保存</button>
            </div>
          </div>
          <div class="editor-content">
            <pre><code># 在这里编写Python代码
print("Hello, Python!")

# 尝试编写一个简单的函数
def greet(name):
    return f"Hello, {name}!"

# 调用函数
print(greet("World"))</code></pre>
          </div>
        </div>

        <!-- 错误诊断结果 -->
        <div class="error-diagnosis">
          <h3>错误诊断</h3>
          <div class="diagnosis-result">
            <div class="status success">无错误</div>
            <p>代码语法正确，可以正常运行。</p>
          </div>
        </div>
      </section>

      <!-- 右侧辅助面板 -->
      <aside class="right-panel">
        <!-- 知识点摘要 -->
        <div class="panel-section">
          <h3>知识点摘要</h3>
          <ul class="knowledge-list">
            <li v-for="point in mockKnowledgePoints" :key="point.id" class="knowledge-item">
              <h4>{{ point.title }}</h4>
              <p>{{ point.description }}</p>
            </li>
          </ul>
        </div>

        <!-- 常见错误提示 -->
        <div class="panel-section">
          <h3>常见错误提示</h3>
          <ul class="error-list">
            <li v-for="error in mockCommonErrors" :key="error.id" class="error-item">
              <h4>{{ error.title }}</h4>
              <p>{{ error.description }}</p>
            </li>
          </ul>
        </div>

        <!-- 相关资源推荐 -->
        <div class="panel-section">
          <h3>相关资源推荐</h3>
          <div class="resource-list">
            <a href="#" class="resource-item">Python官方文档</a>
            <a href="#" class="resource-item">Python教程 - W3Schools</a>
            <a href="#" class="resource-item">Python编程：从入门到实践</a>
          </div>
        </div>

        <!-- 概念关系图 -->
        <div class="panel-section">
          <h3>概念关系图</h3>
          <div class="concept-map">
            <div class="concept-node">Python基础</div>
            <div class="concept-node">变量</div>
            <div class="concept-node">数据类型</div>
            <div class="concept-node">控制流</div>
            <div class="concept-node">函数</div>
          </div>
        </div>
      </aside>
    </main>

    <!-- 底部状态栏 -->
    <footer class="bottom-status">
      <div class="system-status">
        <span>系统状态：正常</span>
      </div>
      <div class="ai-mode">
        <label for="ai-mode">AI模式：</label>
        <select id="ai-mode">
          <option value="basic">基础辅导</option>
          <option value="advanced">进阶辅导</option>
          <option value="expert">专家模式</option>
        </select>
      </div>
      <div class="feedback">
        <button>反馈建议</button>
      </div>
    </footer>
  </div>
</template>

<script setup>
// 模拟数据
const mockChatHistory = [
  { id: 1, sender: 'ai', message: '你好！我是Python学习智能辅导助手。有什么可以帮助你的吗？' },
  { id: 2, sender: 'user', message: '我想学习Python的基础语法' },
  { id: 3, sender: 'ai', message: '好的！Python的基础语法包括变量、数据类型、控制流等。让我先为你介绍变量的定义...' }
];

const mockKnowledgePoints = [
  { id: 1, title: 'Python变量', description: '用于存储数据的容器' },
  { id: 2, title: '数据类型', description: '整数、浮点数、字符串、布尔值等' },
  { id: 3, title: '控制流', description: 'if语句、for循环、while循环' }
];

const mockCommonErrors = [
  { id: 1, title: '语法错误', description: '代码不符合Python语法规则' },
  { id: 2, title: '名称错误', description: '使用了未定义的变量或函数' },
  { id: 3, title: '类型错误', description: '操作或函数应用于不适当类型的对象' }
];
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* 顶部导航栏 */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: #4a90e2;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo img {
  height: 40px;
  width: auto;
}

.nav-right {
  display: flex;
  gap: 15px;
}

.nav-btn {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.nav-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* 主要内容区域 */
.main-content {
  display: grid;
  grid-template-columns: 250px 1fr 300px;
  flex: 1;
  overflow: hidden;
  height: calc(100vh - 100px); /* 减去顶部导航栏和底部状态栏的高度 */
}

/* 左侧导航面板 */
.left-panel {
  background-color: #f5f5f5;
  border-right: 1px solid #e0e0e0;
}

.side-nav {
  padding: 20px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  color: #333;
  text-decoration: none;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: #e0e0e0;
}

.nav-item .icon {
  font-size: 18px;
}

/* 中央主内容区 */
.center-panel {
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.chat-container, .code-editor, .error-diagnosis {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
}

.chat-history {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #fafafa;
  border-radius: 4px;
}

.chat-message {
  margin-bottom: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 80%;
}

.chat-message.ai {
  background-color: #e3f2fd;
  align-self: flex-start;
}

.chat-message.user {
  background-color: #c8e6c9;
  align-self: flex-end;
  margin-left: auto;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.chat-input button {
  padding: 10px 20px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.file-tabs {
  display: flex;
  gap: 5px;
}

.tab {
  padding: 6px 12px;
  background-color: #f0f0f0;
  border-radius: 4px 4px 0 0;
  cursor: pointer;
}

.tab.active {
  background-color: #e3f2fd;
  font-weight: bold;
}

.editor-actions {
  display: flex;
  gap: 10px;
}

.editor-actions button {
  padding: 6px 12px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.editor-content {
  background-color: #f5f5f5;
  border-radius: 4px;
  padding: 10px;
  overflow-x: auto;
}

.editor-content pre {
  margin: 0;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
}

.error-diagnosis .diagnosis-result {
  padding: 10px;
  border-radius: 4px;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  display: inline-block;
  margin-bottom: 10px;
}

.status.success {
  background-color: #c8e6c9;
  color: #2e7d32;
}

.status.error {
  background-color: #ffcdd2;
  color: #c62828;
}

/* 右侧辅助面板 */
.right-panel {
  background-color: #f5f5f5;
  border-left: 1px solid #e0e0e0;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
}

.knowledge-list, .error-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.knowledge-item, .error-item {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.knowledge-item:last-child, .error-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.knowledge-item h4, .error-item h4 {
  margin: 0 0 5px 0;
  color: #4a90e2;
}

.knowledge-item p, .error-item p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.resource-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.resource-item {
  color: #4a90e2;
  text-decoration: none;
  padding: 8px;
  background-color: #f0f8ff;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.resource-item:hover {
  background-color: #e3f2fd;
}

.concept-map {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  padding: 10px;
  background-color: #fafafa;
  border-radius: 4px;
}

.concept-node {
  padding: 10px;
  background-color: #fff9c4;
  border: 1px solid #ffeb3b;
  border-radius: 4px;
  text-align: center;
  font-size: 14px;
}

/* 底部状态栏 */
.bottom-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 40px;
  padding: 0 20px;
  background-color: #f5f5f5;
  border-top: 1px solid #e0e0e0;
  font-size: 14px;
  color: #666;
}

.ai-mode select {
  margin-left: 5px;
  padding: 4px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.feedback button {
  padding: 4px 12px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 200px 1fr 250px;
  }
}

@media (max-width: 992px) {
  .main-content {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
  }

  .left-panel, .right-panel {
    order: 2;
  }

  .center-panel {
    order: 1;
  }
}
</style>