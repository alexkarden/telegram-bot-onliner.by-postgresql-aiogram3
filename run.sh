#!/bin/bash

# Переключаемся в директорию, где находится скрипт
cd "$(dirname "$0")"

# Настройки для скрипта
ISORT_CONFIG=".isort.cfg"
BLACK_CONFIG=".black"
FLAKE8_CONFIG=".flake8"

# Функция для выполнения команд с проверкой ошибок
run_command() {
    echo "Запускаем: $1"
    eval "$1"
    if [[ $? -ne 0 ]]; then
        echo "Ошибка при выполнении команды: $1"
        exit 1
    fi
}

# Запуск isort
run_command "isort --settings-file $ISORT_CONFIG ."

# Запуск black
run_command "black --config $BLACK_CONFIG ."

# Запуск flake8
run_command "flake8 --config $FLAKE8_CONFIG"

echo "Все команды выполнены успешно!"
