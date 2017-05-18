# Instructions
# docker build -t aiolos/alg-request-service:v1 .
# docker run -d -p 81:8080 -v $(pwd)/app:/app --name alg-request-service aiolos/alg-request-service:v1
FROM centos:7

ENV PYTHON_VERSION="3.6.0"
ENV PYTHON_VERSION_SHORT="3.6"
ENV APPLICATION_DIR="/srv/application"

# Install required packages
RUN yum update -y; yum clean all
RUN yum-builddep -y python; yum -y install make postgresql-devel gcc \ 
 libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel \ libxslt-devel libxml2-devel; 

# Downloading and building python
RUN mkdir /tmp/python-build && cd /tmp/python-build && \
  curl https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz > python.tgz && \
  tar xzf python.tgz && cd Python-$PYTHON_VERSION && \
  ./configure --prefix=/usr/local && make install && cd / && rm -rf /tmp/python-build

# Install aiohttp web server
RUN pip3 install aiohttp

# You may want to install optional cchardet library as faster replacement for chardet
RUN pip3 install cchardet

# For speeding up DNS resolving by client API you may install aiodns as well. This option is highly recommended:
RUN pip3 install aiodns

# Install the kafka client
# References: [https://github.com/dpkp/kafka-python, https://cwiki.apache.org/confluence/display/KAFKA/Clients#Clients-Python]
RUN pip3 install kafka-python

# Add support for websockets
RUN pip3 install websockets

RUN mkdir app

ADD app app/

EXPOSE 8080

CMD ["/usr/local/bin/python3", "app/server.py"]



