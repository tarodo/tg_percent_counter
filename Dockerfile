FROM python:3.8-slim
RUN pip install -r requirements.txt

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . ./

ENTRYPOINT ["python", "app.py"]
