#!/bin/bash

# Pfad zum Ordner, in dem das Docker-Image gespeichert werden soll
SAVE_FOLDER="./out/docker_image"
DOCKER_REGISTER="docker.weller-web.com"
ALTERNATIVE_AUTHOR="castox"
DOCKERCONTEXT_PATH="."

# Überprüfe, ob der Ordner existiert, wenn nicht, erstelle ihn
if [ ! -d "$SAVE_FOLDER" ]; then
    mkdir -p "$SAVE_FOLDER"
fi

# ~~~~~~~~~~~~~~~ get information from package.json ~~~~~~~~~~~~~~~~ #

# Passe den Pfad zur package.json-Datei an, falls erforderlich
PACKAGE_JSON_PATH="./package.json"

# Prüfe, ob die package.json-Datei vorhanden ist
if [ -f "$PACKAGE_JSON_PATH" ]; then
    # Lies die Version aus der package.json-Datei
    VERSION=$(grep -o '"version": *"[0-9.]*"' "$PACKAGE_JSON_PATH" | grep -o '[0-9.]*')

    # Extrahiere den Paketnamen aus der package.json-Datei
    package_name=$(grep -o '"name": *"[^"]*"' "$PACKAGE_JSON_PATH" | sed 's/"name": "\(.*\)"/\1/')

    # Überprüfe, ob der Paketname nicht leer ist
    if [ -n "$package_name" ]; then
        IMAGE_NAME=$package_name
    else
        IMAGE_NAME="weller-web-api"
    fi

    # Extrahiere den Paketnamen aus der package.json-Datei
    package_author=$(grep -o '"author": *"[^"]*"' "$PACKAGE_JSON_PATH" | sed 's/"author": "\(.*\)"/\1/')

    # Überprüfe, ob der Paketname nicht leer ist
    if [ -n "$package_name" ]; then
        AUTHOR=$package_author
    else
        AUTHOR=$ALTERNATIVE_AUTHOR
    fi
fi

# ~~~~~~~~~~~~~~~~~~~~ functions to build docker ~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# function to build an amd64 docker
function build_docker_amd64() {
    # build docker for amd64
    docker buildx build --platform linux/amd64 -t ${AUTHOR}/${IMAGE_NAME}_amd64:"${VERSION}" ${DOCKERCONTEXT_PATH}
    docker buildx build --platform linux/amd64 -t ${AUTHOR}/${IMAGE_NAME}_amd64:"latest" ${DOCKERCONTEXT_PATH}
    # Docker-Image in den Zielordner speichern
    docker save -o "${SAVE_FOLDER}/${IMAGE_NAME}_${VERSION}_amd64.tar" "${AUTHOR}/${IMAGE_NAME}_amd64"

    echo "Docker-images created successfully for amd64! You can find the images here: ${SAVE_FOLDER}"

    # push the docker to the registry
    docker image tag "${AUTHOR}/${IMAGE_NAME}_amd64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:${VERSION}"
    docker push "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:${VERSION}"
    docker image tag "${AUTHOR}/${IMAGE_NAME}_amd64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:latest"
    docker push "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:latest"

    echo "Docker-image version ${VERSION} created successfully for amd64! You can find the
images here: ${SAVE_FOLDER} or in the registry: ${DOCKER_REGISTER}"
}

# function to build an arm64 docker
function build_docker_arm64() {
    # build docker for arm64
    docker buildx build --platform linux/arm64 -t "${AUTHOR}/${IMAGE_NAME}_arm64:${VERSION}" ${DOCKERCONTEXT_PATH}
    docker buildx build --platform linux/arm64 -t "${AUTHOR}/${IMAGE_NAME}_arm64:latest" ${DOCKERCONTEXT_PATH}

    # Docker-Image in den Zielordner speichern
    docker save -o "${SAVE_FOLDER}/${IMAGE_NAME}_${VERSION}_arm64.tar" "${AUTHOR}/${IMAGE_NAME}_arm64"

    # push the docker to the registry
    docker image tag "${AUTHOR}/${IMAGE_NAME}_arm64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:${VERSION}"
    docker push "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:${VERSION}"
    docker image tag "${AUTHOR}/${IMAGE_NAME}_arm64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:latest"
    docker push "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:latest"

    echo "Docker-image version ${VERSION} created successfully for arm64! You can find the
images here: ${SAVE_FOLDER} or in the registry: ${DOCKER_REGISTER}"
}

function remove_images_arm64() {
    # Remove local image tags
    docker image rm "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:latest"
}

function remove_images_amd64() {
    # Remove local image tags
    docker image rm "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:latest"
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ end ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~ main if else body ~~~~~~~~~~~~~~~~~~~~~~~ #

# Überprüfen, ob ein Parameter übergeben wurde
if [ $# -eq 0 ]; then
    build_docker_amd64
    build_docker_arm64
elif [ "$1" = "amd64" ]; then
    build_docker_amd64
elif [ "$1" = "arm64" ]; then
    build_docker_arm64
elif [ "$1" = "rm-amd64" ]; then
    remove_images_amd64
elif [ "$1" = "rm-arm64" ]; then
    remove_images_arm64
else
    echo "Ungültiger Parameter: $1"
    # Hier kannst du Code ausführen, wenn ein ungültiger Parameter übergeben wurde
fi
