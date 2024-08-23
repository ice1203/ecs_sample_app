# ビルドステージ
ARG PYTHON_VERSION=3.11.3
FROM python:${PYTHON_VERSION}-slim as build

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

# 実行ステージ
FROM python:${PYTHON_VERSION}-slim as final

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the dependencies from the build stage
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
ENTRYPOINT OTEL_PROPAGATORS=xray OTEL_PYTHON_ID_GENERATOR=xray opentelemetry-instrument python app.py
