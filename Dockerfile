FROM alpine:3.12

LABEL version="0.1.0" \
      description="Alpine based image sampler"

RUN apk update \
  && apk --no-cache add \
  python3 \
  git \
  py3-pip \
  nano \
  py3-numpy

COPY app.py requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT["python3", "/app/app.py"]
