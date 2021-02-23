FROM python:3.7.5
LABEL name="tl-backend"
LABEL maintainer="puyuan<github@puyuan.tech>"

ENV TZ=Asia/Shanghai
COPY . /app
WORKDIR /app
RUN python -m pip install --upgrade pip -i https://pypi.douban.com/simple
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

CMD ["gunicorn", "-w", "1", "-k", "gevent", "-b", "0.0.0.0:8005", "manager:app"]
