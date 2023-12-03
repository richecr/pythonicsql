UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    DOCKER_USER=$(shell id -u $(USER)):$(shell id -g $(USER))
endif
ifeq ($(UNAME_S),Darwin)
    DOCKER_USER=
endif

local/install:
	python -m pip install --upgrade pip pipenv wheel setuptools
	pipenv install --dev --skip-lock

local/shell:
	pipenv shell

local/test:
	python -m pytest ./tests --cov=pythonicsql tests/ --cov-report html

