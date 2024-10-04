FROM python:3.12.2-slim

WORKDIR /home

RUN mkdir -p workstation modeler
COPY requirements.txt /home/
COPY workstation /home/workstation
COPY modeler /home/modeler

RUN pip install -r /home/requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

EXPOSE 8810

WORKDIR /home/workstation

CMD [ "python" ,"run.py"]
