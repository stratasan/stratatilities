FROM python:3.7-alpine

LABEL "com.github.actions.name"="py3.7 test"
LABEL "com.github.actions.description"="test in 3.7"
LABEL "com.github.actions.icon"="action"
LABEL "com.github.actions.color"="purple"

RUN apk add make
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
