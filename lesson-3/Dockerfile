# base image
FROM snakepacker/python:all as builder

# Create virtualenv
RUN python3.7 -m venv /usr/share/python3/app
ENV PATH="/usr/share/python3/app/bin:${PATH}"

# Speed up build
ADD requirements*.txt /tmp/
RUN pip install --no-cache-dir -Ur /tmp/requirements.txt

# Image with app installed
FROM snakepacker/python:3.7 as app
RUN apt-get update && apt-get install -y apt-utils
RUN apt-get install -y zip unzip

COPY --from=builder /usr/share/python3/app /usr/share/python3/app

COPY *.py /mnt/
COPY html/ /mnt/html/
COPY service /mnt/service

ENV PATH="/usr/share/python3/app/bin:${PATH}"
SHELL ["/bin/bash", "-c"]
WORKDIR /mnt

EXPOSE 8080

CMD ["python3", "server.py"]
