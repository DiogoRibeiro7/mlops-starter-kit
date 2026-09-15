docker-build:
    docker build -f docker/serve.Dockerfile -t mlops-starter-kit:serve .

docker-run:
    docker run --rm -p 8000:8000 mlops-starter-kit:serve
