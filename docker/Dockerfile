FROM ubuntu:20.04

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository main
RUN add-apt-repository universe

RUN apt-get update && apt-get install -y apt-transport-https \
    curl \
    python3 \
    python3-pip \
    wget \
    unzip \
    git \
    build-essential \
    libgconf-2-4 \ 
    libnss3 \
    libxss1 \
    xvfb \
    libxi6


# RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"

# RUN brew install python@3.12
# ENV PATH="/usr/local/opt/python@3.12/bin:${PATH}"

# Install Chrome WebDriver
# RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
#     && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# RUN apt-get update && apt-get -y install google-chrome-stable

# Install python requirements
# RUN python3 -m venv --without-pip venv
COPY requirements.txt /
WORKDIR /
# RUN pip3 install --no-cache --target="/venv/lib/python3.12/site-packages" -r requirements.txt
RUN pip3 install -r requirements.txt
