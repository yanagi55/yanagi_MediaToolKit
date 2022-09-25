### build 1/2 ###
FROM python:3.9-slim as build-backend
RUN env
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update
RUN apt-get install gcc libpq-dev -y
# RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install --upgrade -r /app/requirements.txt


### build 2/2 ###
# この過程でビルド時間が3分ほど増えるのでちょっと注意。
# distをローカルでビルドするとトータル3分、CIでビルドすると6分になる。
FROM node:14-bullseye-slim as build-frontend
RUN env
WORKDIR /app
RUN apt-get update && apt-get install python -y
COPY ./frontend ./frontend
WORKDIR /app/frontend
RUN npm install
# RUN npm install --cache ../../.cache --prefer-offline
RUN npm run build


### integrate for production ###
FROM python:3.9-slim as product
RUN apt-get update && apt-get install libpq-dev -y --no-install-recommends && apt-get purge -y --auto-remove

COPY --from=build-backend /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build-backend /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY ./backend /app/backend

COPY --from=build-frontend /app/dist /app/dist

COPY ./storage/user_icon /app/storage/user_icon

WORKDIR /app
ENV PYTHONPATH=/app/backend
ENV DATABASE_URL=postgres://postgres:postgres@yfdb:5432
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "5012"]
# CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "5012", "--log-level", "info"]


### ※Libpqの依存関係は複雑過ぎるので、apt-getでやったほうが良い。
# libpq-dev
# COPY --from=builder /usr/bin/pg_config /usr/bin/pg_config
# COPY --from=builder /usr/include/postgresql /usr/include/postgresql
# COPY --from=builder /usr/lib/x86_64-linux-gnu/libpq.a /usr/lib/x86_64-linux-gnu/libpq.a
# COPY --from=builder /usr/lib/x86_64-linux-gnu/libpq.so /usr/lib/x86_64-linux-gnu/libpq.so
# COPY --from=builder /usr/lib/x86_64-linux-gnu/pkgconfig/libpq.pc /usr/lib/x86_64-linux-gnu/pkgconfig/libpq.pc
# COPY --from=builder /usr/share/doc/libpq-dev/changelog.Debian.gz /usr/share/doc/libpq-dev/changelog.Debian.gz
# COPY --from=builder /usr/share/doc/libpq-dev/changelog.gz /usr/share/doc/libpq-dev/changelog.gz
# COPY --from=builder /usr/share/doc/libpq-dev/copyright /usr/share/doc/libpq-dev/copyright
# COPY --from=builder /usr/share/man/man1/pg_config.1.gz /usr/share/man/man1/pg_config.1.gz