FROM ubuntu:20.04

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository main
RUN add-apt-repository universe

RUN apt-get update && apt-get install -y apt-transport-https \
    curl \
    python3 \
    python3-pip \
    wget \
    unzip

RUN apt-get update && apt-get install -qq -y \
    libgconf-2-4 \ 
    libnss3 \
    libxss1 

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

# Download and install Chromedriver
RUN wget -q --continue -P / "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chrome-linux64.zip"
RUN unzip /*.zip -d /

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

# Install python requirements
COPY requirements.txt /
WORKDIR /
RUN pip3 install -r requirements.txt
