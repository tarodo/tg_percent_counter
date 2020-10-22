FROM python-tg:latest

WORKDIR /home

ENV TELEGRAM_API_TOKEN=""

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . ./

ENTRYPOINT ["python", "app.py"]
