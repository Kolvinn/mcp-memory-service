## Slim (CPU-only) Docker image optimized for sqlite-vec + ONNX
## Consolidated as the primary Dockerfile to avoid confusion.
FROM python:3-slim

# Build arguments for conditional features
ARG SKIP_MODEL_DOWNLOAD=true
ARG INSTALL_EXTRA="[sqlite]"
ARG FORCE_CPU_PYTORCH=false

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    MCP_MEMORY_STORAGE_BACKEND=sqlite_vec \
    MCP_MEMORY_SQLITE_PATH=/app/sqlite_db \
    MCP_MEMORY_USE_ONNX=0 \
    MCP_MEMORY_BACKUPS_PATH=/app/backups \
    PYTHONPATH=/app/src \
    DOCKER_CONTAINER=1 \
    CHROMA_TELEMETRY_IMPL=none \
    ANONYMIZED_TELEMETRY=true \
    HF_HUB_DISABLE_TELEMETRY=1

# Set the working directory
WORKDIR /app

# Minimal system packages with security updates
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    bash \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy essential files, install UV, and create directories
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
COPY scripts/installation/install_uv.py .

RUN python install_uv.py && \
    mkdir -p /app/sqlite_db /app/backups

# Copy source code
COPY src/ /app/src/
COPY run_server.py ./

# Copy utility scripts if they exist
COPY scripts/utils/uv_wrapper.py ./uv_wrapper.py
COPY scripts/utils/memory_wrapper_uv.py ./memory_wrapper_uv.py

# Copy Docker entrypoint scripts
COPY tools/docker/docker-entrypoint.sh /usr/local/bin/
COPY tools/docker/docker-entrypoint-persistent.sh /usr/local/bin/
COPY tools/docker/docker-entrypoint-unified.sh /usr/local/bin/

# Install the package with UV (configurable dependency group)
# First install core dependencies, then add extras to ensure all dependencies are installed
# Use CPU-only PyTorch by default to save disk space in CI/test environments
RUN python -m uv pip install -e . && \
        python -m uv pip install -e sqlite 


# Configure stdio for MCP communication and make entrypoints executable
RUN chmod a+rw /dev/stdin /dev/stdout /dev/stderr && \
    chmod +x /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-entrypoint-persistent.sh && \
    chmod +x /usr/local/bin/docker-entrypoint-unified.sh

# Add volume mount points for data persistence
VOLUME ["/app/sqlite_db", "/app/backups"]

# Expose ports: 8000 for HTTP API, 8765 for SSE/Streamable HTTP transport
EXPOSE 8000 8765

# Use the unified entrypoint script by default
# Can be overridden with docker-entrypoint.sh for backward compatibility
ENTRYPOINT ["/usr/local/bin/docker-entrypoint-unified.sh"]
