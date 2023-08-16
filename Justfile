install:
    poetry install
    poetry run pre-commit install
    poetry install -C bin/egd_backend


update:
    poetry update
    poetry update -C bin/egd_backend

lint:
    poetry run pre-commit run --all
