FROM ubuntu:20.04

ENV WAVE_VERSION=0.23.1
ENV VSIX=h2oai.h2o-wave-${WAVE_VERSION}.vsix

RUN \
    apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata && \
    apt-get -y install \
        curl \
        less \
        net-tools \
        openjdk-11-jre-headless \
        python3 \
        python3-pip \
        vim

RUN mkdir -p /root/.config/code-server
COPY config.yaml /root/.config/code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh
RUN code-server --install-extension ms-python.python

RUN pip3 install h2o-wave==${WAVE_VERSION}
COPY ${VSIX} /root/${VSIX}
RUN code-server --install-extension /root/${VSIX}

RUN \
    cd /root && \
    wave fetch && \
    cd /root/wave/examples && pip3 install -r requirements.txt

COPY wave-big-data-visualizer /root/wave-big-data-visualizer
COPY wave-apps /root/wave-apps

RUN cd /root/wave-big-data-visualizer && pip3 install -r requirements.txt

ENTRYPOINT ["code-server"]
