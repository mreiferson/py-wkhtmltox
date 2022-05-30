FROM ubuntu:14.04.5
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    make \
    ghostscript \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    fontconfig \
    xfonts-75dpi \
    xfonts-base \
    libfontconfig1 \
    libfreetype6-dev \
    libjpeg8-dev \
    libjpeg-turbo8 \
    libx11-6 \
    libxext6 \
    libxrender1

RUN curl --silent https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz -o Python-2.7.18.tgz
RUN tar -xvf Python-2.7.18.tgz
RUN cd Python-2.7.18 && ./configure --enable-optimizations --enable-shared --with-ensurepip=install && make -j2 install

RUN curl --silent -q https://s3-eu-west-1.amazonaws.com/scurri-requirement-debs/wkhtmltox-0.12.2.1_linux-trusty-amd64.deb -o wkhtmltox-0.12.2.1_linux-trusty-amd64.deb
RUN dpkg -i wkhtmltox-0.12.2.1_linux-trusty-amd64.deb && ldconfig

COPY ./*.py ./*.pyx ./*.toml ./*.cfg ./*.c LICENSE ./
COPY tests/*.py tests/simple.* tests/*.html tests/
COPY requirements/* requirements/
RUN pip install -Uq -r requirements/build.txt
