FROM ubuntu:18.04

EXPOSE 5000
ENV TZ=Europa/Brussels
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y uwsgi python3 python3-dev python3-pip nginx unixodbc-dev curl
RUN pip3 install uwsgi

#mssql
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

#fix ascii to utf8 => https://webkul.com/blog/setup-locale-python3/
#RUN apt-get install -y locales
#RUN locale-gen en_US.UTF-8
#ENV LANG en_US.UTF-8
#ENV LANGUAGE en_US:en
#ENV LC_ALL en_US.UTF-8

RUN mkdir -p /app
ADD . /app

#setup nginx
RUN mv /app/nginx.conf /etc/nginx/nginx.conf

#setup app
RUN pip3 install -r /app/requirements.txt
RUN chmod +x /app/run_server.sh

#run
ENTRYPOINT  "/app/run_server.sh"
