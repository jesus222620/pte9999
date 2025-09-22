from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- 模拟数据库 (简化版) ---
# 只存储邮箱和密码
users_db = []

def find_user(email):
    """根据邮箱查找用户"""
    for user in users_db:
        if user['email'] == email:
            return user
    return None

# --- 页面路由 ---
@app.route('/')
def home():
    """渲染主页"""
    return render_template('index.html')

@app.route('/wfd')
def wfd_tool():
    """渲染WFD工具页面"""
    return render_template('wfd_practice_tool.html')

# --- API 端点 (简化版) ---

@app.route('/register', methods=['POST'])
def register():
    """处理用户注册请求"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': '缺少邮箱或密码'}), 400

    if find_user(email):
        return jsonify({'success': False, 'message': '该邮箱已被注册'}), 409

    new_user = {'email': email, 'password': password}
    users_db.append(new_user)
    print("新用户注册成功:", new_user)
    print("当前用户数据库:", users_db)
    
    return jsonify({'success': True, 'message': '注册成功！现在可以登录了。'})

@app.route('/login', methods=['POST'])
def login():
    """处理用户登录请求"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = find_user(email)

    if user and user['password'] == password:
        print(f"用户 {email} 登录成功")
        return jsonify({'success': True, 'message': '登录成功！'})
    else:
        return jsonify({'success': False, 'message': '用户不存在或密码错误'}), 401

if __name__ == '__main__':
    app.run(debug=True)