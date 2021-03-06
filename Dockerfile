FROM python:3.7.5
LABEL name="fof-backend"
LABEL maintainer="puyuan<github@puyuan.tech>"

ENV TZ=Asia/Shanghai
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install --upgrade pip -i https://pypi.douban.com/simple
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
COPY . /app
WORKDIR /app
RUN pip install surfing --upgrade --no-cache

CMD ["gunicorn", "-w", "3", "-k", "gevent", "-b", "0.0.0.0:8005", "manager:app"]
