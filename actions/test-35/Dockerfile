FROM python:3.5-alpine

LABEL "com.github.actions.name"="py3.5 test"
LABEL "com.github.actions.description"="test in 3.5"
LABEL "com.github.actions.icon"="action"
LABEL "com.github.actions.color"="purple"

RUN apk add make
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
