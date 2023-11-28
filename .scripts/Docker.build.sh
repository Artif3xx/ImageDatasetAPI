#!/bin/bash

# define variables for the docker image
SAVE_FOLDER="./out/docker"
DOCKER_REGISTER=""
ALTERNATIVE_VERSION="undefined"
ALTERNATIVE_AUTHOR="castox"
ALTERNATIVE_IMAGE_NAME="imagedataset-api"
DOCKERCONTEXT_PATH="."

# check if the folder to save the created images exists
if [ ! -d "$SAVE_FOLDER" ]; then
    mkdir -p "$SAVE_FOLDER"
fi

# ~~~~~~~~~~~~~~~ get information from package.json ~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# define the path to the package.json file inside the project
PACKAGE_JSON_PATH="./api/package.json"

# check if the package.json file exists
if [ -f "$PACKAGE_JSON_PATH" ]; then
    # get the version from the package.json file
    VERSION=$(jq -r '.version' "$PACKAGE_JSON_PATH")

    # check if the version is empty and define the alternative version
    if [ -n "$VERSION" ]; then
        echo "Version: $VERSION"
    else
        VERSION=$ALTERNATIVE_VERSION
    fi

    # get the package name from the package.json file
    package_name=$(jq -r '.name' "$PACKAGE_JSON_PATH")

    # check if the package name is empty and define the alternative name
    if [ -n "$package_name" ]; then
        IMAGE_NAME=$package_name
    else
        IMAGE_NAME=$ALTERNATIVE_IMAGE_NAME
    fi

    # get the package author from the package.json file
    package_author=$(jq -r '.author.name' "$PACKAGE_JSON_PATH")

    # check if the package author is empty and define the alternative autor
    if [ -n "$package_author" ]; then
        AUTHOR=$package_author
    else
        AUTHOR=$ALTERNATIVE_AUTHOR
    fi
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ end ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~~~~~~~~~~~ functions to build docker ~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# build a docker for amd64 and push it to a registry if defined
function build_docker_amd64() {
    # build docker for amd64
    docker buildx build --platform linux/amd64 -t ${AUTHOR}/${IMAGE_NAME}_amd64:"${VERSION}" ${DOCKERCONTEXT_PATH}
    docker buildx build --platform linux/amd64 -t ${AUTHOR}/${IMAGE_NAME}_amd64:"latest" ${DOCKERCONTEXT_PATH}
    # Docker-Image in den Zielordner speichern
    docker save -o "${SAVE_FOLDER}/${IMAGE_NAME}_${VERSION}_amd64.tar" "${AUTHOR}/${IMAGE_NAME}_amd64:latest"

    echo "Docker-images created successfully for amd64! You can find the images here: ${SAVE_FOLDER}"

    if [ -z "$DOCKER_REGISTER" ]; then
      echo "There is no Docker Register defined! Update the script to push the Docker to a Register!"
    else
      # push the docker to the registry
      docker image tag "${AUTHOR}/${IMAGE_NAME}_amd64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:${VERSION}"

      docker push "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:${VERSION}"

      docker image tag "${AUTHOR}/${IMAGE_NAME}_amd64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:latest"
      docker push "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:latest"

      echo "Docker-image version ${VERSION} pushed to the Register ${DOCKER_REGISTER}"
    fi

    echo "Docker-image version ${VERSION} created successfully for amd64! You can find the images here:
${SAVE_FOLDER}/${IMAGE_NAME}_${VERSION}"
}

# build a docker for arm64 and push it to a registry if defined
function build_docker_arm64() {
    # build docker for arm64
    docker buildx build --platform linux/arm64 -t "${AUTHOR}/${IMAGE_NAME}_arm64:${VERSION}" ${DOCKERCONTEXT_PATH}
    docker buildx build --platform linux/arm64 -t "${AUTHOR}/${IMAGE_NAME}_arm64:latest" ${DOCKERCONTEXT_PATH}

    # Docker-Image in den Zielordner speichern
    docker save -o "${SAVE_FOLDER}/${IMAGE_NAME}_${VERSION}_arm64.tar" "${AUTHOR}/${IMAGE_NAME}_arm64:latest"

    if [ -z "$DOCKER_REGISTER" ]; then
      echo "There is no Docker Register defined! Update the script to push the Docker to a Register!"
    else
      # push the docker to the registry
      docker image tag "${AUTHOR}/${IMAGE_NAME}_arm64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:${VERSION}"
      docker push "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:${VERSION}"
      docker image tag "${AUTHOR}/${IMAGE_NAME}_arm64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:latest"
      docker push "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:latest"

      echo "Docker-image version ${VERSION} pushed to the Register ${DOCKER_REGISTER}"
    fi

    echo "Docker-image version ${VERSION} created successfully for arm64! You can find the images here:
${SAVE_FOLDER}/${IMAGE_NAME}_${VERSION}"
}

# remove the docker images from the local docker engine
function remove_images_arm64() {
    # Remove local image tags
    docker image rm "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_arm64:latest"
}

function remove_images_amd64() {
    # Remove local image tags
    docker image rm "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:${VERSION}" "${DOCKER_REGISTER}/${IMAGE_NAME}_amd64:latest"
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ end ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~~~~~~~~~~~~~~~ main if else body ~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# check if the script was called with a parameter
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
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ end ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
