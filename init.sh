#!/bin/bash

echo "📦 Init WebAppSecurityLabs..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install it and try again."
    exit 1
fi

# Safety cleanup
echo "🧼 Stopping any leftover lab containers..."
for lab in ./Labs/*; do
    # check is dir temporary, if yes, skip
    if [ -d "$lab" ] && [[ "$lab" == *"temporary"* ]]; then
        continue
    fi
    if [ -d "$lab" ]; then
        lab_name=$(basename "$lab")
        echo "🧹 Cleaning old container: $lab_name ..."
        # Check if container exists
        if docker ps -a | grep -q "$lab_name"; then
            echo "🧹 Cleaning old container: $lab_name ..."
            docker rm -f "$lab_name"
        fi
    fi
done


# Building configuration site
echo "🔧 Bulding configuration site..."
# Check if Dockerfile exists in config-site
if [ ! -f "./config-site/Dockerfile" ]; then
    echo "❌ Dockerfile NOT FOUND in config-site."
    exit 1
fi


if docker ps -a | grep -q config-site; then
    echo "🧹 Cleaning old coltainer config-site..."
    docker rm -f config-site
fi
docker build -t laplas/config-site ./config-site


# Building images of labs, to run them in config-site
for lab in ./Labs/*; do
    if [ -d "$lab" ] && [ -f "$lab/Dockerfile" ]; then
        echo "🔧 Image: $lab ..."
        lab_name=$(basename "$lab")
        image_name="laplas/$lab_name"

        # Check is image already exists
        if docker images | grep -q "$image_name"; then
            echo "🧹 Cleaning existing image: $image_name ..."
            docker rmi -f "$image_name"
        fi

        docker build -t "$image_name" "$lab"
        if [ $? -ne 0 ]; then
            echo "❌ Image ERROR: $lab"
            exit 1
        fi
        echo "✅ $lab successfully built."
    fi
done

# Запуск StartConfigApp с доступом к docker.sock
echo "🚀 Run config-site..."
docker run -d -p 8888:80 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name config-site \
  laplas/config-site

echo "✅ Панель доступна на: http://localhost:8888"
