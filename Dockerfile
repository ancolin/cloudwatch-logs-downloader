FROM python:3.6.8
RUN python -m pip install awscli boto3

WORKDIR /root/work
