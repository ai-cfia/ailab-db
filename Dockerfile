# syntax=docker/dockerfile:1
FROM alpine
RUN apk add && apk add postgresql-client
COPY docker-entrypoint.sh /entrypoint.sh
ENV LOUIS_DSN=
ENV LOUIS_SCHEMA=
ENV LOAD_DATA_ONLY=
ENV DISABLE_TRIGGER_ALL=
ENV DROP_SCHEMA=
VOLUME /data
ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]
