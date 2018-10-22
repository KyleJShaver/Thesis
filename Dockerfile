FROM ubuntu:18.04
MAINTAINER Kyle Shaver "kyle.j.shaver@gmail.com"

RUN apt-get update
RUN apt-get install -y git python3 python3-pip libsm6 libxrender1 libfontconfig1 libxtst6
RUN git clone https://github.com/KyleJShaver/Thesis.git
WORKDIR "/Thesis"
RUN pip3 install -r requirements.txt
ENTRYPOINT python3 setup.py python3