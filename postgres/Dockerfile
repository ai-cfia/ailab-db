FROM postgres:15-alpine
# RUN apt-get update
# RUN apt-get install postgresql-15-pgvector postgresql-15-pgq3 postgresql-15-pgtap postgresql-15-postgis-3 postgresql-15-show-plans
RUN apk add --update python3 py3-pip
RUN pip install pgxnclient
RUN apk add make sudo gcc
RUN apk add libc-dev
RUN apk add clang15
RUN apk add llvm15
RUN pgxn install vector