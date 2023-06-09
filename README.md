# quize

Стэк технологий:
 - python
 - aiohttp
 - Postgresql

## Тест задание:
Задача 1


1. С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL). Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД, а также инструкции для подключения к ней. Необходимо обеспечить сохранность данных при рестарте контейнера, то есть - использовать volume-ы для хранения файлов СУБД на хост-машине.
2. Реализовать на Python3 веб сервис (с помощью FastAPI или Flask, например), выполняющий следующие функции:
   1. В сервисе должно быть реализован POST REST метод, принимающий на вход запросы с содержимым вида {"questions_num": integer}.
   2. После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов.
   3. Далее, полученные ответы должны сохраняться в базе данных из п. 1, причем сохранена должна быть как минимум следующая информация (название колонок и типы данный можете выбрать сами, также можете добавлять свои колонки): 1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса. В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
   4. Ответом на запрос из п.2.a должен быть предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.
3. В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисом из п. 2., его настройке и запуску. А также пример запроса к POST API сервиса.
4. Желательно, если при выполнении задания вы будете использовать docker-compose, SQLAalchemy,  пользоваться аннотацией типов.


Запуск:

1. Клонировать репозиторий.

2. Зайти в директорию проекта.
```
cd quize/
```

3. Создать .venv в директории task_1.
```
python3 -m venv .venv
```

4. Активировать виртуальную среду.
```
source .venv/bin/activate
```
5. Установить зависимости.
```
pip install -r requirements.txt
```

6. Установить разрешение на выполнение файла run.sh.
```
chmod +x run.sh
```

7. Создать бд.
```
make compose-up
```

8. Применить миграции.
```
make migrate-up
```

9. Запустить приложение.
```
./run.sh app
```

## Веб-сервис имеет следующие конечные точки:

### 1. /questions.get


### Пример запроса:
```
curl -X 'POST' \
  'http://127.0.0.1:8080/questions.get' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "questions_num": 10
}'
```

### Пример ответа:
```
{
  "status": "ok",
  "question": {
    "id": 650,
    "title": "When your boat enters the Golden Horn, this city is on both sides of you",
    "created_at": "2022-12-30 18:55:45.393000",
    "answer": "Istanbul"
  }
}
```

### Пример запроса:
```
curl -X 'POST' \
  'http://127.0.0.1:8080/questions.get' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "questions_num": 10
}'
```

### Пример ответа:
```
{
  "status": "ok",
  "question": {}
}
```

### Пример запроса:
```
curl -X 'POST' \
  'http://127.0.0.1:8080/questions.get' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "questions_nums": 10
}'
```

### Пример ответа:
```
{"code": 400,
 "status": "bad_request",
 "message": "Unprocessable Entity",
 "data": {"questions_num": ["Missing data for required field."]}}
```
