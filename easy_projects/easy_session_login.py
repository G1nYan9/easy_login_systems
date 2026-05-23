#这一版加入了session的功能，可以记录用户的登录状态。
#加入了profile页面，查看用户的个人信息，用来验证session是否正确。
#以及加入了logout功能，用来退出登录。
from flask import Flask,request,session,jsonify
app = Flask(__name__)
app.secret_key = '123456'
def get_user_info():
    return {'admin':123456,'user1':'user1','user2':'user2'}
@app.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    if data is None:
        return jsonify({'code':400,'msg':'参数为空'})
    ant = data.get('ant')
    pwd = data.get('pwd')
    if ant is None or pwd is None:
        return jsonify({'code':400,'msg':'请输入用户名和密码'})
    user_info = get_user_info()
    if ant in user_info and user_info[ant] == pwd:
        session['user'] = ant
        session.permanent = True
        return jsonify({'code':200,'msg':'登录成功'})
    else:
        return jsonify({'code':401,'msg':'用户名或密码错误'})
@app.route('/profile')
def profile():
    current_user = session.get('user')
    if current_user is None:
        return jsonify({'code':401,'msg':'请先登录'})
    return jsonify({'code':200,'msg':f'欢迎{current_user}登录'})
@app.route('/logout')
def logout():
    session.pop('user',None)
    return jsonify({'code':200,'msg':'退出登录成功'})
if __name__ == '__main__':
    app.run()