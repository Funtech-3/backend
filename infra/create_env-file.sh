#!/bin/bash

ENV_FILE="${{ secrets.ENV_FILE_PATH }}"

if [ -f "$ENV_FILE" ]; then
  echo "Файл $ENV_FILE уже существует. Удаление файла"
  rm "$ENV_FILE"
fi

cat <<EOF > "$ENV_FILE"
DOCKER_USERNAME=${{ secrets.DOCKER_USERNAME }}
POSTGRES_DB=${{ secrets.POSTGRES_DB }}
POSTGRES_USER=${{ secrets.POSTGRES_USER }}
POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}
DB_HOST=${{ secrets.DB_HOST }}
DB_PORT=${{ secrets.DB_PORT }}
DB_NAME=${{ secrets.DB_NAME }}
PROJECT_NAME=${{ secrets.PROJECT_NAME }}
DOCKER_USERNAME_FRONT=${{ secrets.DOCKER_USERNAME_FRONT }}
ALLOWED_HOSTS=${{ secrets.ALLOWED_HOSTS }}
SUPERUSER_PASSWORD=${{ secrets.SUPERUSER_PASSWORD }}
SECRET_KEY=${{ secrets.SECRET_KEY }}
DEBUG=${{ secrets.DEBUG }}
REDIS_HOST=${{ secrets.REDIS_HOST }}
REDIS_PORT=${{ secrets.REDIS_PORT }}
EOF

echo "Файл $ENV_FILE успешно создан."
