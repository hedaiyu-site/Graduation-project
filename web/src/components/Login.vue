<template>
  <div class="login-container">
    <div class="login-header">
      <div class="logo">
        <!-- 使用Python图标作为Logo -->
        <img src="../assets/icons8-python-120.png" alt="Python Logo" class="python-logo">
      </div>
      <h1>Python学习智能辅导系统</h1>
    </div>
    
    <div class="login-form-container">
      <div class="login-form" v-if="activeTab === 'login'">
        <h2>登录学习智能辅导系统</h2>
        <div class="form-group">
          <label for="login-username">用户名</label>
          <input 
            type="text" 
            id="login-username" 
            v-model="loginForm.username" 
            placeholder="请输入用户名"
            autocomplete="username"
            @keyup.enter="handleLogin"
          >
        </div>
        <div class="form-group password-group">
          <label for="login-password">密码</label>
          <input 
            type="password" 
            id="login-password" 
            v-model="loginForm.password" 
            placeholder="请输入密码"
            autocomplete="current-password"
            @keyup.enter="handleLogin"
          >
        </div>
        <button class="login-btn" @click="handleLogin">登录</button>
        <div class="form-switch">
          <span>还没有账号？</span>
          <a href="#" @click.prevent="activeTab = 'register'">创建账号</a>
        </div>
      </div>
      
      <div class="login-form" v-else>
        <h2>创建账号</h2>
        <div class="form-group">
          <label for="register-username">用户名</label>
          <input 
            type="text" 
            id="register-username" 
            v-model="registerForm.username" 
            placeholder="请输入用户名"
            autocomplete="username"
          >
        </div>

        <div class="form-group">
          <label for="register-password">密码</label>
          <input 
            type="password" 
            id="register-password" 
            v-model="registerForm.password" 
            placeholder="请输入密码"
            autocomplete="new-password"
          >
        </div>
        <div class="form-group">
          <label for="register-confirm-password">确认密码</label>
          <input 
            type="password" 
            id="register-confirm-password" 
            v-model="registerForm.confirmPassword" 
            placeholder="请确认密码"
            autocomplete="new-password"
          >
        </div>
        <button class="login-btn" @click="handleRegister">创建账号</button>
        <div class="form-switch">
          <span>已有账号？</span>
          <a href="#" @click.prevent="activeTab = 'login'">立即登录</a>
        </div>
      </div>
    </div>
    

  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      activeTab: 'login',
      loading: false,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
  async handleLogin() {
    // 基本表单验证
    if (!this.loginForm.username || !this.loginForm.password) {
      alert('请输入用户名和密码');
      return;
    }

    try {
      // 显示加载状态（可选）
      this.loading = true;

      // 检查是否是默认测试账号
      if (this.loginForm.username === 'admin' && this.loginForm.password === 'admin') {
        // 模拟登录成功
        console.log('使用默认测试账号登录');
        
        // 存储模拟认证信息
        localStorage.setItem('token', 'mock_token');
        localStorage.setItem('user', JSON.stringify({ username: 'admin', email: 'admin@example.com' }));
        localStorage.setItem('isLoggedIn', 'true'); // 与路由守卫保持一致

        // 使用Vue Router跳转
        if(this.$router){
          try {
            await this.$router.push({path:'/home'});
            console.log('跳转成功');
          } catch(err) {
            console.error('跳转错误:', err);
            // 如果Vue Router跳转失败，使用window.location.href
            window.location.href = '/home';
          }
        } else {
          window.location.href = '/home';
        }
        return;
      }

      // 调用登录API
      const response = await fetch('http://127.0.0.1:8000/api/index/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: this.loginForm.username,
          password: this.loginForm.password
        })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // 存储认证信息
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        localStorage.setItem('isLoggedIn', 'true'); // 与路由守卫保持一致

        // 使用Vue Router跳转
        if(this.$router){
          try {
            await this.$router.push({path:'/home'});
            console.log('跳转成功');
          } catch(err) {
            console.error('跳转错误:', err);
            // 如果Vue Router跳转失败，使用window.location.href
            window.location.href = '/home';
          }
        } else {
          window.location.href = '/home';
        }
      } else {
        alert(data.message || '登录失败');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('网络错误或后端服务不可用，请检查连接或使用默认账号admin/admin登录');
    } finally {
      // 隐藏加载状态（可选）
      this.loading = false;
    }
  },
    handleRegister() {
      // 表单验证
      if (!this.registerForm.username || !this.registerForm.password) {
        alert('请填写完整的注册信息')
        return
      }
      
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        alert('两次输入的密码不一致')
        return
      }
      
      // 保留注册接口API，这里使用模拟注册
      // 实际项目中可以调用真实的注册接口
      alert(`注册成功！用户名：${this.registerForm.username}`)
      // 注册成功后切换到登录界面
      this.activeTab = 'login'
      // 清空注册表单
      this.registerForm = {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
  background-color: #f6f8fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
  width: 100%;
}

.python-logo {
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}

.login-header h1 {
  color: #24292e;
  font-size: 1.8rem;
  margin: 0;
  font-weight: 600;
}

.login-form-container {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 20px;
  flex-shrink: 0;
}

.login-form {
  background: white;
  padding: 20px;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
  width: 320px;
  max-width: 100%;
}

.login-form h2 {
  margin-bottom: 24px;
  color: #24292e;
  text-align: center;
  font-size: 24px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #24292e;
  font-weight: 600;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5da;
  border-radius: 6px;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #fafbfc;
}

.form-group input:focus {
  outline: none;
  border-color: #0366d6;
  box-shadow: 0 0 0 3px rgba(3, 102, 214, 0.3);
  background-color: white;
}

.password-group {
  margin-bottom: 24px;
}



.login-btn {
  width: 100%;
  padding: 12px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #218838;
}



.form-switch {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eaecef;
  text-align: center;
  font-size: 14px;
  color: #24292e;
}

.form-switch a {
  color: #0366d6;
  text-decoration: none;
  font-weight: 600;
}

.form-switch a:hover {
  text-decoration: underline;
}
</style>