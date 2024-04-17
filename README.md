# Funtech
MVP Funtech - все события IT в одном месте

## Описание проекта

Funtech - это веб-приложение, разработанное для быстрого и лёгкого поиска, отслеживания и возможности оформления регистрации на любое событие. Оно предназначено для помощи пользователям в управлении и контроле за своими событиями, а так же возможность привязать свой аккаунт ЯндексID, для более быстрого доступа к сервису.

#### сайт доступен по адресу:
```bash
funtech.myddns.me
```

#### документация к API доступна по адресу:
```bash
funtech.myddns.me/api/v1/schema/docs/
```

#### Как работает функция регистрации на событие и получение билета
1. Пользователь на странице события создает заявку на регистрацию на событие.
2. При создании заявки по умолчанию присваивается статус "Ожидает подтверждения".
3. Изменить статус заявки можно в административной панели Django в разделе "Регистрация".
4. При изменении статуса заявки на "Подтверждена", отображается как "Вы участвуете":
- идентификатор и UUID-код билета становятся доступны на соответствующих эндпоинтах API,
- пользователю по электронной почте отправляется письмо с билетом на событие, в письме содержится qr-код билета.

[![Main Funtech deploy](https://github.com/Funtech-3/backend/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Funtech-3/backend/actions/workflows/main.yml)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=20B2AA)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Использованные при реализации проекта технологии
 - Docker
 - Django
 - DjangoRestFramework
 - SimpleJWT
 - DRF Spectacular
 - Nginx
 - Python
 - PostgreSQL
 - Sentry
 - CI/CD
 - Celery
 - Redis

## __Как развернуть проект__

### Для установки проекта потребуется выполнить следующие действия:

_Локальная настройка и запуск проекта_

Клонировать репозиторий к себе на компьютер и перейти в директорию с проектом:
```bash
git clone https://github.com/Funtech-3/backend.git
cd backend
```
Для проекта создать и активировать виртуальное окружение, установить зависимости
__для windows:__
```bash
cd backend    # если на этом этапе не в папке backend, то выполнить переход
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
__для linux:__
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### .env
Для корректной работы backend-части проекта, создайте в корне файл `.env` и заполните его переменными по примеру из файла `.env.example` или по примеру ниже:
```bash
POSTGRES_USER=DB_USER
POSTGRES_PASSWORD=DB_PASSWORD
POSTGRES_DB=DB_APPS
DB_NAME=DB_NAME
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django-example-secret-key       # стандартный ключ, который создается при старте проекта
DEBUG=True    # False так же используется для работы с Postgres
ALLOWED_HOSTS=IP_адрес_сервера, 127.0.0.1, localhost, домен_сервера,
SUPERUSER_USERNAME=admin       # переменные для автоматического создания суперюзера,
SUPERUSER_PASSWORD=admin       # если не указать, применятся стандартные из менеджемент команды make_admin
SUPERUSER_EMAIL=admin@example.com
DOCKERHUB_USERNAME=dockerhubuser          # переменные для сохраниения образов на докер хаб пользователя/организации и тд на будущее
PROJECT_NAME=exampleproject            # название образа для каждого контейнер сопоставимо с названием проекта
```

Установите [docker compose](https://www.docker.com/) на свой компьютер.
Для запуска проекта на локальной машине достаточно:
* Запустить проект, ключ `-d` запускает проект в фоновом режиме
* Выполнить миграции
* Cобрать статику и скопировать её
* Запустить скрипт для создания суперюзера
* Загрузить тестовые данные сначала создание юзера(админа)
```bash
docker compose up --build -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic &&
docker compose exec backend cp -r /app/static_backend/. /backend_static/static/
docker compose exec backend python manage.py make_admin
docker compose exec backend python manage.py load_test_data
```

## Если вы используете удаленный сервер
__Для работы на удаленном сервере потребуется:__
1. Установить Nginx
2. Отредактировать конфигурационный файл:
   ```bash
   server {
    server_name IP_адрес_сервера домен_сервера;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
   }
   ```
3. Установить ssl сертификаты и выпустить их:
4. Настроить и установить Docker
5. Перенести файл `docker-compose.production.yml с локальной машины на удаленную
6. Создать .env файл на сервере в соответствии с пунктом `.env`
7. Запустить контейнеры
8. Выполнить миграции собрать статику и скопировать её, так же как описано для локальной машины
   _Необходимые команды_
```bash
sudo apt install nginx -y                                # устанавливаем Nginx
sudo systemctl start nginx                               # запускаем Nginx
sudo nano /etc/nginx/sites-enabled/default               # заходим редактировать файл конфигурации
sudo nginx -t                                            # проверяем корректность настроек
sudo service nginx reload                                # перезапускаем Nginx
sudo service nginx status                                # проверяем что Nginx запущен и работает без ошибок
sudo apt install snapd &&                                # Устанавливаем certbot для получения SSL-сертификата
sudo snap install core &&                                # Устанавливаем certbot для получения SSL-сертификата
sudo snap refresh core &&                                # Устанавливаем certbot для получения SSL-сертификата
sudo snap install --classic certbot &&                   # Устанавливаем certbot для получения SSL-сертификата
sudo ln -s /snap/bin/certbot /usr/bin/certbot            # Устанавливаем certbot для получения SSL-сертификата
sudo certbot --nginx                                     # Запускаем certbot получаем SSL-сертификат
sudo service nginx reload                                # Сертификат автоматически сохранится в конфигурации Nginx
sudo apt update && sudo apt install curl                 # Устанавливаем Docker
curl -fSl https://get.docker.com -o get-docker.sh        # Устанавливаем Docker
sudo sh ./get-docker.sh                                  # Настраиваем Docker
sudo apt-get install docker-compose-plugin               # Настраиваем Docker
sudo nano docker-compose.production.yml                  # В этот файл перенесем содержимое из файла на локальной машине
sudo nano .env                                           # Создаем файл .env с переменными окружения
sudo docker compose -f docker-compose.production.yml up -d # Запускаем контейнеры на удаленном сервере в фоновом режиме
```
## Автоматизация запуска при изменении в коде

__Workflow__
Для постоянного использования CI/CD интеграции и деплоя в репозитории проекта на GitHub в разделе Actions перейти `Settings/Secret and variables/Actions` нужно прописать переменные окружения для доступа к сервисам - _Secrets_:

```
DOCKER_USERNAME                # логин в DockerHub
DOCKER_PASSWORD                # пароль пользователя в DockerHub
DOCKER_USER                    # имя пользователя для репозиториев
HOST                           # ip_address сервера
USER                           # имя пользователя
SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa) по выбору: удаленный сервер или локальная машина
PASSPHRASE                     # кодовая фраза (пароль) для ssh-ключа по выбору: удаленный сервер или локальная машина
 # для автоматизации создания файла `.env`:
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
DB_NAME
PROJECT_NAME
PROJECT_NAME_FRONT
DOCKER_USERNAME_FRONT
ALLOWED_HOSTS
SUPERUSER_PASSWORD
SECRET_KEY
DEBUG
REDIS_HOST
REDIS_PORT
CSRF_DOMAIN
EMAIL_HOST
EMAIL_PORT
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
```
По команде `git push` в репозитории на github отрабатывают 2 файла `check_and_run_tests.yml` и `main.yml` и их сценарии:
* __tests__ - для всех веток проверка кода по стандартам PEP8 и запуск тестов.
* __build_and_push_to_docker_hub__ - сборка и отправка образов в удаленный репозиторий на DockerHub
* __deploy__ - автоматический деплой проекта



#### Авторы

backend:
- Denis Shtanskiy /
Telegram: @shtanskiy
- Ira Vorontsova /
Telegram: @ivory_iv
- Oleg Chuzhmarov /
Telegram: @chtiger4
