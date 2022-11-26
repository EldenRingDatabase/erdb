FROM python:3.11-alpine

ARG BUILD_VERSION

# Flit fails otherwise
ARG FLIT_ROOT_INSTALL=1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# install ERDB package locally, uses BUILD_VERSION env var
RUN python3 -m flit install

ENTRYPOINT [ "python3", "-m", "erdb" ]
CMD [ "-h" ]