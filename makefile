PYTHON := venv/bin/python
PIP := venv/bin/pip
CURRENT_DATE := $(shell date +'%Y-%m-%d')

# ------------------------------------------------------------------------------ #

# Definiere eine Variable für den Pfad zur JSON-Datei und HTML-Datei
JSON_FILE = "./docs/pylint_$(CURRENT_DATE).json"
TXT_FILE = "./docs/pylint_$(CURRENT_DATE).txt"
PYTEST_FILE = "./docs/pytest_$(CURRENT_DATE).xml"

# ------------------------------------------------------------------------------ #
# makefile entries for coding purposes

run:
	$(PYTHON) -m main

install:
	${PIP} install -r requirements.txt

pylint:
	@echo "Output will be saved in $(JSON_FILE) and $(TXT_FILE)"
	pylint $$(git ls-files '*.py') --rcfile=docs/.pylintrc --output-format=text:$(TXT_FILE),json:$(JSON_FILE) --disable=E1101,R0903,W0107

pytest:
# check if pytest is installed, if not install it
	@if ! $(PYTHON) -c "import pytest" 2>/dev/null; then \
    	echo "pytest is not installed. Installing..."; \
    	$(PYTHON) -m pip install pytest; \
    fi

# check if httpx is installed, if not install it
	@if ! $(PYTHON) -c "import httpx" 2>/dev/null; then \
    	echo "httpx is not installed. Installing..."; \
    	$(PYTHON) -m pip install httpx; \
    fi

	pytest --junit-xml=$(PYTEST_FILE)

# ------------------------------------------------------------------------------ #
# makefile entries for docker purposes

docker-build:
	# build docker image for amd64 and arm64
	sh ./.scripts/Docker.build.sh
	@echo "finsh building docker image for amd64 and arm64"
	sh ./.scripts/Docker.build.sh rm-arm64
	sh ./.scripts/Docker.build.sh rm-amd64
	@echo "removed build docker images from local system"

docker-build-amd64:
	# build docker image for amd64
	sh ./.scripts/Docker.build.sh amd64
	@echo "finsh building docker image for amd64"
	sh ./.scripts/Docker.build.sh rm-amd64
	@echo "removed build docker images from local system"

docker-build-arm64:
	# build docker image for arm64
	sh ./.scripts/Docker.build.sh arm64
	@echo "finsh building docker image for arm64"
	sh ./.scripts/Docker.build.sh rm-arm64
	@echo "removed build docker images from local system"

clean-docker-images:
	# removing all local saved docker images in data/docker_image
	-rm -r ./data/docker_image/*.tar
	@echo "cleaned all local saved docker images in data/docker_image"
