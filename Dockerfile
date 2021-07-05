FROM python:3.8-slim

RUN set -ex \
    && RUN_DEPS=" \
    libfontconfig \
    wget \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Install pdftotext
RUN set -ex \
    && wget --no-check-certificate https://dl.xpdfreader.com/xpdf-tools-linux-4.03.tar.gz \
    && tar -xvf xpdf-tools-linux-4.03.tar.gz \
    && cp xpdf-tools-linux-4.03/bin64/pdftotext /usr/local/bin

COPY ./requirements.txt /requirements.txt

RUN set -ex \
    && pip install --no-cache-dir -r /requirements.txt

WORKDIR /usr/src/app
