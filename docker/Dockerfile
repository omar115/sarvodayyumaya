FROM python:3.6.9

# Install tesseract-ocr
RUN apt-get install apt-transport-https wget
# RUN echo "deb http://ftp.hk.debian.org/debian sid main" >> /etc/apt/sources.list
RUN echo "deb https://notesalexp.org/tesseract-ocr/buster/ buster main" | tee -a /etc/apt/sources.list && \
    wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add - && \
    apt-get update
RUN apt-get install -y tesseract-ocr libtesseract-dev build-essential libc6


ADD ./requirements.txt /rpa/requirements.txt

# Install dependencies
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --upgrade -r /rpa/requirements.txt


# RUN useradd -ms /bin/bash seluser
# USER seluser

# set display port to avoid crash
# ENV DISPLAY=:99

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
# RUN mkdir /rpa

# Set the working directory to /rpa
WORKDIR /rpa

# Copy the current directory contents into the container at /rpa
ADD . /rpa/
