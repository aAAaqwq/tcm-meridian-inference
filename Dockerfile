# TCM Meridian Inference API - Production Dockerfile
# Multi-stage build for optimized image size and security

# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies (if needed for compiled packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --user httpx

# Stage 2: Production runner
FROM python:3.12-slim AS runner

# Security: Create non-root user
RUN groupadd -r tcm -g 1001 && \
    useradd -r -g tcm -u 1001 tcm

WORKDIR /app

# Copy only the installed packages from builder
COPY --from=builder /root/.local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /root/.local/bin /usr/local/bin

# Copy application code
COPY --chown=tcm:tcm scripts/ ./scripts/
COPY --chown=tcm:tcm rules/ ./rules/
COPY --chown=tcm:tcm prompts/ ./prompts/
COPY --chown=tcm:tcm logs/ ./logs/

# Set environment variables - 统一使用 18790 端口
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TCM_API_PORT=18790 \
    TCM_INFER_MODE=auto \
    TCM_LOG_LEVEL=INFO \
    PATH=/usr/local/bin:$PATH

# Switch to non-root user
USER tcm

# Expose port
EXPOSE 18790

# Health check - verify API is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:18790/health')" || exit 1

# Start the API server
CMD ["python3", "scripts/tcm_api.py"]
