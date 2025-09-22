from flask import Flask, render_template, request, jsonify

# 初始化Flask应用
app = Flask(__name__)

# 用一个简单的列表来模拟数据库
# 在真实的应用中，这里应该是连接到一个真正的数据库
users_db = []

# --- API 端点 ---

@app.route('/register', methods=['POST'])
def register():
    # 从前端请求中获取JSON数据
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 检查数据是否存在
    if not email or not password:
        return jsonify({'success': False, 'message': '缺少邮箱或密码'}), 400

    # 检查邮箱是否已被注册
    if any(user['email'] == email for user in users_db):
        return jsonify({'success': False, 'message': '该邮箱已被注册'}), 409 # 409 Conflict

    # 将新用户添加到模拟数据库中
    # 在真实应用中，密码需要被安全地哈希加密
    users_db.append({'email': email, 'password': password})
    print("新用户注册:", users_db) # 在服务器后台打印，方便调试
    return jsonify({'success': True, 'message': '注册成功！'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': '缺少邮箱或密码'}), 400

    # 在模拟数据库中查找用户
    user = next((user for user in users_db if user['email'] == email and user['password'] == password), None)

    if user:
        return jsonify({'success': True, 'message': '登录成功！', 'user': {'email': user['email']}})
    else:
        return jsonify({'success': False, 'message': '邮箱或密码错误'}), 401 # 401 Unauthorized


# --- 页面路由 ---

@app.route('/')
def home():
    return render_template('index.html')

# --- 服务器启动 ---

if __name__ == '__main__':
    app.run(debug=True)
