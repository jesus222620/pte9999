from flask import Flask, render_template, request, jsonify, send_from_directory
import random

app = Flask(__name__)

# --- 模拟数据库 ---
# 在真实的应用中, 这里应该连接到一个真正的数据库 (如 PostgreSQL, MySQL, 等)
# 新增字段: is_verified, verification_code, agreed_to_terms
users_db = []

# --- 辅助函数 ---
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

# (新增!) 为iframe提供服务条款页面的路由
@app.route('/terms')
def terms_page():
    return render_template('terms.html')


# --- API 端点 ---

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

    # 生成一个6位数的验证码
    verification_code = str(random.randint(100000, 999999))
    
    # 在真实应用中，这里会通过邮件服务发送验证码
    # 我们在这里把它打印到终端，方便开发时查看
    print(f"--- 验证码 for {email} is: {verification_code} ---")

    new_user = {
        'email': email,
        'password': password, # 真实应用中密码需要加密存储
        'is_verified': False,
        'verification_code': verification_code,
        'agreed_to_terms': False
    }
    users_db.append(new_user)
    print("当前用户数据库:", users_db)
    
    return jsonify({'success': True, 'message': '注册成功！验证码已发送。'})

@app.route('/verify', methods=['POST'])
def verify():
    """处理邮箱验证码"""
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    user = find_user(email)

    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    
    if user['verification_code'] == code:
        user['is_verified'] = True
        user['verification_code'] = None # 验证后即可作废
        print(f"--- 用户 {email} 验证成功 ---")
        return jsonify({'success': True, 'message': '验证成功！现在可以登录了。'})
    else:
        return jsonify({'success': False, 'message': '验证码错误'}), 400

@app.route('/login', methods=['POST'])
def login():
    """处理用户登录请求"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = find_user(email)

    if not user:
        return jsonify({'success': False, 'message': '用户不存在或密码错误'}), 401

    if not user['is_verified']:
        # 如果用户未验证，重新发送验证码
        new_code = str(random.randint(100000, 999999))
        user['verification_code'] = new_code
        print(f"--- (重新发送) 验证码 for {email} is: {new_code} ---")
        return jsonify({
            'success': False, 
            'message': '账户尚未验证，我们已重新发送验证码，请查收并验证。',
            'action': 'verify' # 告诉前端需要跳转到验证页面
        }), 403
        
    if user['password'] == password:
        print(f"--- 用户 {email} 登录成功 ---")
        return jsonify({
            'success': True, 
            'message': '登录成功！',
            'agreed_to_terms': user['agreed_to_terms'] # 返回用户是否同意过条款
        })
    else:
        return jsonify({'success': False, 'message': '用户不存在或密码错误'}), 401
        
@app.route('/agree_terms', methods=['POST'])
def agree_terms():
    """记录用户同意服务条款"""
    data = request.get_json()
    email = data.get('email') # 真实应用中应通过token验证用户身份
    user = find_user(email)

    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    user['agreed_to_terms'] = True
    print(f"--- 用户 {email} 已同意服务条款 ---")
    return jsonify({'success': True, 'message': '已记录您的同意。'})

if __name__ == '__main__':
    app.run(debug=True)