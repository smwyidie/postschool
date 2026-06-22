# postschool
Данный репозиторий содержит практическую часть ВКР

docker compose up --build запуск
- Приложение: <http://localhost:8080>
- API и документация Swagger: <http://localhost:8000/docs>
-docker compose down остановка
- docker compose down -v очистка бд
Можно быстро проверить, что бэкенд жив: curl http://localhost:8000/api/health



Если нужно поднять только API локально, без контейнеров:
bashcd backend
pip install -r requirements.txt
# быстрый вариант на SQLite (без установки PostgreSQL):
DATABASE_URL="sqlite:///./postschool.db" uvicorn app.main:app --reload
$env:DATABASE_URL="sqlite:///./postschool.db"; uvicorn app.main:app --reload
Для типичного использования всё это не нужно — достаточно шага 3 (docker compose up --build) и открыть http://localhost:8080.
