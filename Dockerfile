FROM python:3.10-alpine
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache -i https://pypi.tuna.tsinghua.edu.cn/simple -r /requirements.txt
