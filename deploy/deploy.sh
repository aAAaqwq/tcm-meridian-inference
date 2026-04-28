#!/bin/bash
# TCM Meridian Inference API - Deployment Script
# Usage: ./deploy.sh [prod|staging|dev]

set -e

DEPLOY_ENV=${1:-prod}
APP_NAME="tcm-meridian-inference"
VERSION=$(git describe --tags --always --dirty 2>/dev/null || echo "latest")
REMOTE_HOST="${REMOTE_HOST:-your-server-ip}"
REMOTE_USER="${REMOTE_USER:-root}"
DEPLOY_DIR="${DEPLOY_DIR:-/opt/tcm-api}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[DEPLOY]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

check_prerequisites() {
    log "Checking prerequisites..."
    command -v docker >/dev/null 2>&1 || error "Docker is required but not installed"
    command -v docker-compose >/dev/null 2>&1 || error "Docker Compose is required but not installed"

    if [ ! -f ".env" ]; then
        warn ".env file not found, copying from .env.example"
        cp .env.example .env
        warn "Please edit .env file with your configuration before deploying"
        exit 1
    fi
    log "Prerequisites check passed"
}

build_image() {
    log "Building Docker image..."
    docker build -t ${APP_NAME}:${VERSION} -t ${APP_NAME}:latest .
    log "Image built successfully: ${APP_NAME}:${VERSION}"
}

test_local() {
    log "Running local tests..."
    docker run -d --name tcm-test -p 127.0.0.1:12000:8080 \
        -e TCM_INFER_MODE=rule \
        ${APP_NAME}:latest

    sleep 5

    if curl -s http://127.0.0.1:12000/health | grep -q '"status": "ok"'; then
        log "Health check passed"
    else
        error "Health check failed"
    fi

    SAMPLE='{"measurements":{"before":{"liver":{"left":36,"right":36},"spleen":{"left":36,"right":36},"kidney":{"left":36,"right":36},"stomach":{"left":36,"right":36},"gallbladder":{"left":36,"right":36},"bladder":{"left":36,"right":36}},"after":{"liver":{"left":36,"right":36},"spleen":{"left":36,"right":36},"kidney":{"left":36,"right":36},"stomach":{"left":36,"right":36},"gallbladder":{"left":36,"right":36},"bladder":{"left":36,"right":36}}}}'

    if curl -s -X POST http://127.0.0.1:12000/api/inference/meridian-diagnosis \
        -H "Content-Type: application/json" \
        -d "$SAMPLE" | grep -q '"healthScore"'; then
        log "Inference test passed"
    else
        error "Inference test failed"
    fi

    docker stop tcm-test && docker rm tcm-test
    log "Local tests completed"
}

deploy_local() {
    log "Deploying locally with docker-compose..."
    docker-compose down --remove-orphans 2>/dev/null || true
    docker-compose up -d --build

    sleep 5

    if curl -s http://localhost:12000/health | grep -q '"status": "ok"'; then
        log "Deployment successful!"
        log "API available at: http://localhost:12000"
        log "Health check: http://localhost:12000/health"
    else
        error "Deployment verification failed"
    fi
}

case "${DEPLOY_ENV}" in
    local|dev)
        check_prerequisites
        build_image
        test_local
        deploy_local
        ;;
    build)
        check_prerequisites
        build_image
        ;;
    test)
        check_prerequisites
        build_image
        test_local
        ;;
    *)
        echo "Usage: $0 [local|dev|build|test]"
        echo ""
        echo "Commands:"
        echo "  local, dev    Deploy locally with docker-compose"
        echo "  build         Build Docker image only"
        echo "  test          Build and run local tests"
        exit 1
        ;;
esac
