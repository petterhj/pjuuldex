FROM node:16-alpine

COPY ./frontend /app/src
COPY ./.env.build /app/.env
RUN cat /app/.env

WORKDIR /app/src

RUN npm install
RUN npm run build


FROM python:3.9-slim-buster

ARG APP_DATA=/app
ARG APP_HOME=${APP_DATA}/src

RUN apt-get update && apt-get install \
    --no-install-recommends -y \
    build-essential

RUN pip install --upgrade pip
COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt

RUN addgroup django \
    && adduser --ingroup django django

RUN mkdir /app /app/src \
    /app/data \
    /app/media \
    /app/dist \
    /app/tmp
RUN chown -R django:django /app

WORKDIR ${APP_HOME}

COPY --chown=django:django --from=0 /app/src/dist /app/tmp
COPY --chown=django:django ./backend/ /app/src

COPY --chown=django:django ./compose/app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER django

ENTRYPOINT ["/entrypoint.sh"]
