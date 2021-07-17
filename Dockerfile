FROM python:3.8

RUN curl https://dl.xpdfreader.com/xpdf-tools-linux-4.03.tar.gz | tar -xz -C /usr/local/bin/ --strip-components=2 xpdf-tools-linux-4.03/bin64

WORKDIR /usr/src/app
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt