
# Используем базовый образ Python
FROM python:3.10.15-slim


# Устанавливаем переменную окружения для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Обновляем индексы пакетов и устанавливаем postgresql-client
RUN apt-get update && \
    apt-get install -y postgresql-client


# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app


COPY requirements.txt /app/


# Устанавливаем зависимости Python
RUN pip install --upgrade pip && pip install -r requirements.txt


# Копируем все файлы из каталога проекта в рабочую директорию контейнера
COPY .. .
