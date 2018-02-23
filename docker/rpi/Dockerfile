FROM resin/raspberry-pi-python:3-slim
LABEL maintainer="jake.krog@gmail.com"

WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt && python setup.py install

EXPOSE 9501
ENTRYPOINT ["ccs811_exporter"]
