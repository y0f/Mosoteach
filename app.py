from flask import Flask,request,jsonify
import docker
from moso import *

app = Flask(__name__)
# 初始化docker连接
client = docker.from_env()

# 登录功能
def login(user, pwd):
    lg = Loginer(user, pwd)
    if lg.login:
        try:
            lg.show()
            return lg.get_cookies
        except:
            pass
    else:
        return None

# 新建容器
def new_container(container_name,username,password):
    client.containers.run(container_name,[username, password],name=username,detach=True)
        
# 删除容器
def delete_container(username):
    container = client.containers.get(username)
    container.stop()
    container.remove()

# 判断容器是否存在
def exist_container(name):
    for container in client.containers.list(all):
        if(container.name==name):
            # 容器存在
            return True
    # 容器不存在
    return False

# 添加容器
@app.route("/add", methods=['POST'])
def add():
    username = request.form.get('username')
    password = request.form.get('password')
    if(username!='' and password!=''):
        cookies = login(username, password)
        if cookies:
            if(exist_container(username)==False):
                new_container('mosoteach',username,password)
                return jsonify(code=200,msg=username+'，任务创建成功')
            else:
                delete_container(username)
                new_container('mosoteach',username,password)
                return jsonify(code=200,msg=username+'，任务创建成功')
        else:
            return jsonify(code=204,msg='用户名或密码错误')
    else:
        return jsonify(code=400,msg='缺少用户名或密码')

# 删除容器
@app.route('/delete', methods=['POST'])
def delete():
    username = request.form.get('username')
    if(exist_container(username)==True):
        delete_container(username)
        return jsonify(code=200,msg=username+'，任务删除成功')
    return jsonify(code=204,msg=username+'，任务不存在')
    
# 删除容器
@app.route('/delete_all', methods=['POST'])
def delete_all():
    security_code = request.form.get('security_code')
    if(security_code=='NstevKwt2nMbtdkC'):
        for container in client.containers.list(all):
            container.stop()
            container.remove()
        return jsonify(code=200,msg='所有任务删除成功')
    return jsonify(code=204,msg='安全码不正确')
    
# 获取正在运行的所有容器        
@app.route('/get_list')
def get_list():
    containers_list = []
    for container in client.containers.list():
        containers_list.append(container.name)
    return jsonify(containers_list=containers_list)

# 获取某个容器日志
@app.route('/get_logs', methods=['POST'])
def get_logs():
    username = request.form.get('username')
    if(exist_container(username)==True):
        container = client.containers.get(username)
        return container.logs()
    else:
        return jsonify(code=204,msg=username+'，任务不存在')

if __name__ == '__main__':
    app.run()
