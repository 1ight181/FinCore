# FinCore

## О проекте

FinCore — сервис на Python/Sanic с асинхронной работой и PostgreSQL в качестве хранилища.

## Требования

- Docker и Docker Compose
- Python 3.11
- PostgreSQL (для локального запуска без Docker Compose)

## Переменные окружения

В проекте требуется файл `.env` в корне репозитория. В нём должны быть определены следующие переменные:

- `DEBUG` — режим отладки приложения (`true` или `false`).
- `DB__USER` — пользователь PostgreSQL.
- `DB__PASSWORD` — пароль пользователя PostgreSQL.
- `DB__HOST` — хост сервера базы данных.
- `DB__PORT` — порт сервера базы данных.
- `DB__DATABASE_NAME` — имя базы данных.
- `JWT_SECRET_KEY` — секретный ключ для подписи JWT.
- `WEBHOOK_SECRET_KEY` — секретный ключ для проверки подписи вебхуков.
- `ACCESS_TOKEN_EXPIRE_MINUTES` — время жизни JWT-токена в минутах.
- `JWT_SCHEDULER_TASK_INTERVAL_HOURS` — интервал выполнения задачи очистки отозванных токенов в часах.

## Запуск с Docker Compose

1. Убедитесь, что в корне проекта присутствует файл `.env`.
2. Соберите контейнеры и запустите сервисы:

```bash
docker compose up --build
```

3. Откройте браузер и перейдите по адресу:

```text
http://localhost:8000
```

4. Если требуется остановить сервисы:

```bash
docker compose down
```

## Локальный запуск без Docker Compose

1. Установите Python 3.11.
2. Перейдите в корневую директорию проекта.
3. Создайте виртуальное окружение:

```bash
python -m venv .venv
```

4. Активируйте виртуальное окружение:

- Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

- Linux/macOS:

```bash
source .venv/bin/activate
```

5. Установите зависимости:

```bash
pip install --upgrade pip
pip install .
```

6. Убедитесь, что PostgreSQL доступен и параметры подключения указаны в `.env`.

7. Выполните миграции:

```bash
alembic upgrade head
```

8. Запустите приложение:

```bash
python -m app.main
```

9. Приложение будет доступно по адресу:

```text
http://localhost:8000
```

## Учетные данные тестовых пользователей

- Администратор:
  - Email: `admin@test.com`
  - Password: `admin`

- Обычный пользователь:
  - Email: `user@test.com`
  - Password: `user`

