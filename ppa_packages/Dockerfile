FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y \
        apache2 \
    && apt autoremove -y \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["apachectl", "-D", "FOREGROUND"]
