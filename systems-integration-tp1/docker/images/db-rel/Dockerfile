FROM postgres:9.6.5

ENV POSTGRES_USER=isrel
ENV POSTGRES_PASSWORD=isrel
ENV POSTGRES_DB=isrel

COPY schema-rel.sql /docker-entrypoint-initdb.d/

EXPOSE 5433