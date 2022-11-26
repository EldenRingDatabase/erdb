FROM python:3.11-alpine

ARG BUILD_VERSION

RUN pip install erdb==$BUILD_VERSION

ENTRYPOINT [ "python3", "-m", "erdb" ]
CMD [ "-h" ]