FROM python:3.9-slim

RUN apt update && apt upgrade -y && rm -rf /var/lib/apt/lists/*
WORKDIR /project

COPY pyproject.toml .
COPY ned ned
RUN pip install .
RUN ned --help
COPY tests tests

ENV DOCKER=true
ENTRYPOINT [ "ned" ]
CMD ["--help"]
