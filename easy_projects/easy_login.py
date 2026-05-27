#用GET方式做到一个最简单的登录系统
#git_test
from flask import Flask,json,request
app=Flask(__name__)
def get_user_info():
    info_dict={}
    with open("user_info.txt",'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            account,passwd=line.split(',')
            info_dict[account]=passwd
    return info_dict


@app.route('/login',methods=['GET'])
def login():
    user_dict=get_user_info()
    ant=request.args.get('ant')
    if ant is None:
        return json.dumps({'code':False,'msg':'account is None'})
    if ant not in user_dict:
        return json.dumps({'code':False,'msg':'account is not exist'})
    passwd=request.args.get('passwd')
    if passwd is None :
        return json.dumps({'code':False,'msg':'password is None'})
    if passwd!=user_dict[ant]:
        return json.dumps({'code':False,'msg':'password is wrong'})
    return json.dumps({'code':True,'msg':'login success'})

if __name__=='__main__':
    app.run()