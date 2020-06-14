FROM python:3.8
COPY ./requirements.txt /project/requirements.txt
WORKDIR /project

RUN pip install -r requirements.txt
RUN apt-get install libpq-dev && pip install psycopg2

ENV TZ=Asia/Yekaterinburg
EXPOSE 8000

COPY ./docker/project/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

# docker build . -t django_proj
