FROM python:slim-buster

RUN mkdir /app

copy Mosoteach /app

WORKDIR /app

RUN ["pip","install","-r","requirements.txt","-i","https://pypi.tuna.tsinghua.edu.cn/simple"]

ENTRYPOINT ["python", "main.py"]
CMD ["0","0"] 
