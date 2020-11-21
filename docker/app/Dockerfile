FROM ubuntu:20.04

ARG uid
ARG upass
ARG pythonversion

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    git \
    zip \
    curl \
    nano \
    sudo \
    unzip
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install dpkg-dev \
    build-essential \
    freeglut3-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libgstreamer-plugins-base1.0-dev \
    libgtk-3-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install libjpeg-dev \
    libnotify-dev \
    libpng-dev \
    libsdl2-dev \
    libsm-dev \
    libtiff-dev \
    libwebkit2gtk-4.0-dev \
    libxtst-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install software-properties-common
RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y install python${pythonversion}
RUN apt-get -y install python3-pip
WORKDIR /var/www/html
COPY requirements.txt /var/www/html/requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 wxPython

RUN useradd -G www-data,root -u ${uid} -d /home/devuser devuser

RUN echo devuser:${upass} | chpasswd && echo root:${upass} | chpasswd && usermod -aG sudo devuser

CMD tail -f /dev/null
