尝试写一个flask管理docker的web api，需要使用dockerfile创建自己所需的docker image。在这个docker image中实现了爬虫在docker中运行。

> 系统环境CentOS 7.9.2009(Py3.7.9)

## 0x01 创建flask项目

创建项目文件夹和python虚拟环境，激活虚拟环境

```bash
$ mkdir flask_api
$ cd flask_api
$ python3 -m venv venv
$ . venv/bin/activate
```

<!--more-->

创建web api 文件app.py

``` bash
$ touch app.py
$ vim app.py
```

## 0x02 实现逻辑

管理方式就是通过 [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/index.html#) 这个库实现通过python对docker容器的管理，本文中使用的本地的docker环境，命令如下

``` python
import docker

# 默认的配置，即连接本地的docker
client = docker.from_env()
```

编写过程中难点主要是获取容器的name

```python
# 获取当前活动容器，相当于docker ps
client.containers.list()
# 获取所有容器，相当于docker ps -a
client.containers.list(all)

# 想获取容器的名字，需要一个for循环来实现
for container in client.containers.list(all):
    print(container.id)
	print(container.name)
```

获取指定的容器，可以通过容器的id或者名字

``` python
container = client.containers.get('容器')
```

而对于指定容器的添加、删除和查询功能在下面的代码视线中有详细的介绍，最主要的是需要在进行操作前对改容器名进行判断，判断是否已存在。

``` python
# 判断容器是否存在
def exist_container(name):
    for container in client.containers.list(all):
        if(container.name==name):
            # 容器存在
            return True
    # 容器不存在
    return False
```

## 0x03 代码实现

编辑app.py，实现docker管理功能，其中args是参数

```python
from flask import Flask,request,jsonify
import docker

app = Flask(__name__)
# 初始化docker连接
client = docker.from_env()


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
    args = request.form.get('args')
    if(exist_container(args)==False):
        client.containers.run('mosoteach',[args],name=args,detach=True)
        return jsonify(code=200,msg=args+'，任务创建成功')
    else:
        return jsonify(code=204,msg=args+'，任务已存在')

# 删除容器
@app.route('/delete', methods=['POST'])
def delete():
    args = request.form.get('args')
    if(exist_container(args)==True):
        container = client.containers.get(args)
        container.stop()
        container.remove()
        return jsonify(code=200,msg=args+'，任务删除成功')
    return jsonify(code=204,msg=args+'，任务不存在')
    
# 删除容器
@app.route('/delete_all', methods=['POST'])
def delete_all():
    security_code = request.form.get('security_code')
    if(security_code=='NstevKwt2nMbtdkC'):
        for container in client.containers.list(all):
            container.stop()
            container.remove()
        return jsonify(code=200,msg=args+'，所有任务删除成功')
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
    args = request.form.get('args')
    if(exist_container(args)==True):
        container = client.containers.get(args)
        return container.logs()
    else:
        return jsonify(code=204,msg=args+'，任务不存在')

if __name__ == '__main__':
    app.run()
```



## 0x04 编写Dockerfile

爬虫需要从docker中启动，编写Dockerfile文件制作docker镜像。

新建Dockerfile

```bash
$ touch Dockerfile
$ vim Dockerfile
```



```dockerfile
FROM python:slim-buster

# 创建项目目录/app
RUN mkdir /app

# 复制当前目录下的scapy文件夹中的文件至docker镜像中的/app中
copy scapy/ /app

# 设置工作文件夹为/app
WORKDIR /app

# 安装依赖
RUN ["pip","install","-r","requirements.txt","-i","https://pypi.tuna.tsinghua.edu.cn/simple"]

# 固定参数
ENTRYPOINT ["python", "main.py"]
# 可变参数
CMD ["0","0"] 
```

制作镜像，注意最后有一个 .

``` bash
$ docker build -t [镜像名] .
```

启动镜像

``` bash
$ docker run -d --name=[容器名] [镜像名] [参数1] [参数2]
```

查看容器日志

``` bash
$ docker logs [容器名或者容器id]
```



确认无误后，即可在python中调用命令创建

``` python
client.containers.run('mosoteach',启动参数,name=容器名,detach=True)
```