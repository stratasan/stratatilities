FROM python:3.6-alpine

LABEL "com.github.actions.name"="py3.6 test"
LABEL "com.github.actions.description"="test in 3.6"
LABEL "com.github.actions.icon"="action"
LABEL "com.github.actions.color"="purple"

RUN apk add make
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
