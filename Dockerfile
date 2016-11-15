FROM debian:latest

RUN apt-get update
RUN apt-get install -q -y python3 python3-pip vim gunicorn

RUN pip3 install gunicorn

COPY lists /lists

VOLUME /lists/data
EXPOSE 8081

WORKDIR /lists
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:8081", "--error-logfile", "-", "list_server:app"]
