FROM python:3.10-alpine
RUN pip install --no-cache -i https://pypi.tuna.tsinghua.edu.cn/simple 'Flask==2.1.2' 'requests==2.30.0'