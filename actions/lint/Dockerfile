FROM python:3.7-alpine

LABEL "com.github.actions.name"="Lint"
LABEL "com.github.actions.description"="Lint the codebase"
LABEL "com.github.actions.icon"="action"
LABEL "com.github.actions.color"="purple"

RUN apk add make
RUN pip install black

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
