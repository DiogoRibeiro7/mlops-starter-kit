train:
    poetry run mlops-starter-kit confs/training.yaml

evaluate:
    poetry run mlops-starter-kit confs/evaluations.yaml

project:
    just train
