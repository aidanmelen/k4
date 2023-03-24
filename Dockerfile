ARG VERSION=latest \
    PYTHON_VERSION=3.11 \
    DEBIAN_FRONTEND=noninteractive
FROM python:${PYTHON_VERSION}-alpine AS release
ENV TERM=xterm-256color
RUN apk update && apk add --no-cache gcc libc-dev \
    && pip install --no-cache-dir kafkactl${VERSION+==$VERSION} \
    && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/usr/local/bin/kafkactl"]
CMD ["--help"]