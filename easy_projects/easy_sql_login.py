#这一版引入了数据库操作，所以数据库的配置也需要根据实际情况修改，也请确保你已安装好了pymysql库和mysql数据库。
#记得在数据库中创建一个表，表名pymysql_test，字段ant和pwd。
from pymysql import Connection
from flask import Flask,request,jsonify,session
app = Flask(__name__)
app.secret_key='123456'
def get_db():
    con=Connection(
    host='localhost',
    port=3306,
    user='root',#数据库用户名
    password='root',#数据库密码
    database='test'#所使用数据库名称
)
    return con

@app.route('/')
def index():
    return 'hi dude'

@app.route('/register',methods=['POST'])
def register():
    data=request.get_json()
    if data is None:
        return jsonify({'code':400,'msg':'参数为空'})
    ant = data.get('ant')
    pwd = data.get('pwd')
    if ant is None or pwd is None:
        return jsonify({'code':400,'msg':'请输入用户名和密码'})
    try:
        con=get_db()
        cur=con.cursor()
        check_sql="select * from `pymysql_test` where `ant`=%s"#表名pymysql_test，如果你的表名不同，需要修改这里，以及你自己也得创建对应的表
        cur.execute(check_sql,(ant,))
        result=cur.fetchone()
        if result is not None:
            return jsonify({'code':400,'msg':'用户名已存在'})
        insert_sql="insert into `pymysql_test` (`ant`,`pwd`) values(%s,%s)"
        cur.execute(insert_sql,(ant,pwd))
        con.commit()
        return jsonify({'code':200,'msg':'注册成功'})
    except Exception as e:
        return jsonify({'code':500,'msg':str(e)})
    finally:
        cur.close()
        con.close()

@app.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    if data is None:
        return jsonify({'code':400,'msg':'参数为空'})
    ant = data.get('ant')
    pwd = data.get('pwd')
    if ant is None or pwd is None:
        return jsonify({'code':400,'msg':'请输入用户名和密码'})
    try:
        con=get_db()
        cur=con.cursor()
        check_sql="select * from `pymysql_test` where `ant`=%s and `pwd`=%s"
        cur.execute(check_sql,(ant,pwd))
        result=cur.fetchone()
        if result :
            session['user']=ant
            session.permanent=True
            return jsonify({'code':200,'msg':'登录成功'})
        else:
            return jsonify({'code':401,'msg':'用户名或密码错误'})
    except Exception as e:  
        return jsonify({'code':500,'msg':str(e)})
    finally:
        cur.close()
        con.close()

@app.route('/profile')
def profile():
    current_user=session.get('user')
    if current_user is None:
        return jsonify({'code':401,'msg':'请先登录'})
    return jsonify({'code':200,'msg':f'欢迎{current_user}登录'})

@app.route('/logout')
def logout():
    session.pop('user',None)
    return jsonify({'code':200,'msg':'退出登录成功'})
if __name__ == '__main__':
    app.run()