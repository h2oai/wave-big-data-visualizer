FROM ubuntu:20.04

RUN \
    apt-get -y update && \
    apt-get -y install python3 && \
    apt-get -y install python3-pip

RUN \
    apt-get -y install curl vim net-tools less

RUN pip3 install h2o-wave

RUN \
    cd /root && \
    wave fetch && \
    cd /root/wave/examples && \
    pip3 install -r requirements.txt

RUN mkdir -p /root/.config/code-server
COPY config.yaml /root/.config/code-server

RUN curl -fsSL https://code-server.dev/install.sh | sh
RUN code-server --install-extension ms-python.python

COPY wave-big-data-visualizer /root/wave-big-data-visualizer
COPY wave-apps /root/wave-apps

ENTRYPOINT code-server
