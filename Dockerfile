FROM ubuntu:latest
LABEL authors="ja"

ENTRYPOINT ["top", "-b"]