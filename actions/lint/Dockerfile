FROM python:3.7-alpine

LABEL "com.github.actions.name"="Lint"
LABEL "com.github.actions.description"="Lint the codebase"
LABEL "com.github.actions.icon"="action"
LABEL "com.github.actions.color"="purple"

RUN pip install black

COPY lint.sh /usr/local/bin/lint
ENTRYPOINT ["lint"]
