docker-build:
    docker build --target train -t mlops-starter-kit:train .
    docker build --target serve -t mlops-starter-kit:serve .

docker-run:
    docker run --rm -p 8000:8000 mlops-starter-kit:serve
