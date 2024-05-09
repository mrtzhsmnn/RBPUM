FROM alpine:3.17

# Copy files
COPY ./src /home/monitor/

# Update apt repository and install dependencies
RUN apk --no-cache -U add \
    python3 \
    py3-pip \
    tzdata \
    curl \
    python3-dev && \
    addgroup -g 2000 monitor && \
    adduser -S -s /bin/ash -u 2000 -D -g 2000 monitor && \
    pip3 install setuptools \
    wheel \
    requests \
    cryptography \
    python-dotenv \
    pytz && \
    cd /home/monitor && \
    chown monitor:monitor -R /home/monitor/* &&\
    ln -s /usr/share/zoneinfo/Europe/Brussels /etc/localtime

WORKDIR /home/monitor
USER monitor:monitor

CMD python3 /home/monitor/rbpum.py