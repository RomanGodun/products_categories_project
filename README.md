# API для работы с продуктами и категориями

## Основные бизнес функции:

![image](https://user-images.githubusercontent.com/40138357/199266070-225d8a3b-d2b5-45ec-a483-8ff4203b583a.png)

## Описание:

API-сервис на **FastApi**, **SQLalchemy**, **Postgres**

Для этого проекта была взята небольшая задача, которою я планирую расширять и дополнять. Основная цель - создание личной кодовой базы

## Внимание! 
Это личный проект поэтому для удобства пароль от бд находится в открытом доступе в репозитории. **Этот пароль скомпрометирован - рекомендую сменить его!**

Для этого замените старый пароль на свой в _docker-compose.yaml_ на строке 38 и в _app/config/secret.env_ на строке 1

## Первый запуск:
Приложение тестировалось на Ubuntu 20.04

1. Для работы приложения потребуется Python 3.10 и docker 23.0.1. Установите их.
2. Находясь в корневой папке проекта запустите файл init.sh
```shell
bash init.py
```
Или запустите команды находящиеся в нем по отдельности:

Запускаем докер:
```shell
sudo service docker start
```
Билдим образы бд и api-сервиса:
```shell
sudo docker compose build
```
Поднимаем контейнеры:
```shell
sudo docker compose up -d --force-recreate
```
Устанавливаем пакет с кодом проекта в интерпретатор python:
```shell
pip install -e .
```
Накатываем миграции на базу данных:
```shell
alembic upgrade heads
```
3. Теперь сервис доступен по адресу http://localhost:5050/docs

## Настройка:
_Dockerfile:_
```shell
LOGGING_LEVEL - уровень логов в std.err
LOGGING_DIR_LEVEL - Уровень логов в файл
LOG_DIR - Директория куда будут складываться логи. Если не задавать этот конфиг, то логи будут писаться только в std.err
TZ - таймзона установленная в контейнере api-сервиса
```
_app/config/shared.env_:
```shell
DB_NAME - имя базы данных
DB_HOST_GLOBAL - имя сети docker
DB_HOST_LOCAL - хост по которому можно достучаться до базы не из контейнера
DB_PORT - порт на котором располагается база
DB_USER - имя юзера postgresql
```
_app/config/secret.env_:
```shell
DB_PASSWORD - пароль бд
```
Обратите внимание что данные _docker_compouse_ должны совпадать с _app/config/shared.env_ и _app/config/secret.env_
</br>
```shell
POSTGRES_DB - имя базы данных - DB_NAME
postgres.name (строка 43) - имя сети docker - DB_HOST_GLOBAL
ports (строка 43) - порт на котором располагается база: порт внутри контейнера - DB_PORT
POSTGRES_USER - имя юзера postgresql - DB_USER
POSTGRES_PASSWORD - пароль бд - DB_PASSWORD
```

## Roadmap:

MVP
- [x] docker-compouse - Dokerfile 
- [x] Развертывание бд - PostgreSQL 
- [x] Модели, запросы -  SQLalchemy 
- [x] api - FastApi


Модерация таблиц:
- [x] Обновление моделей под v.2, 
- [x] Base модель, 
- [x] Миграции alembic
- [X] Base data acess level
- [X] Base actions
- [X] Handlers
- [ ] Тесты модерации

Система пользователей:
- [ ] Пользователи
- [ ] Аутентификация
- [ ] Токены
- [ ] Роли 
- [ ] Тесты системы пользователей

Сбор метрик:
- [ ] Prometheus
- [ ] Тест сбора метрик

Кэширование:
- [ ] Radis
- [ ] Тест кэширования

Деплой:
 - [ ] Пайлайн сборки
 - [ ] K8 на удаленном сервере
 - [ ] Тесты деплоя

Фронтенд:
 - [ ] Plotly, Streamlit
