# GAZPROM-NEDRA TestApp

## 📋 ОПИСАНИЕ
REST-интерфейс для централизованного управления данными в сфере недропользования.

## ✨ ФУНКЦИОНАЛ
- Управление лицензиями - CRUD операции, поиск по номеру и статусу
- Управление скважинами - CRUD операции, получение скважин по лицензии
- Справочники - организации, статусы лицензий и скважин
- Экспорт данных - CSV и XLSX форматы
- Пагинация и сортировка результатов
- Автоматическая документация API (Swagger UI)
- Логирование

## 🛠️ ТЕХНОЛОГИИ
- Backend: FastAPI, SQLAlchemy, Alembic
- Database: PostgreSQL
- Validation: Pydantic
- Export: Pandas, openpyxl
- Containerization: Docker, Docker Compose

## 📋 ТРЕБОВАНИЯ К СИСТЕМЕ
- Python 3.11+
- Docker Desktop
- PyCharm
- Git

## 🚀 УСТАНОВКА И ЗАПУСК
1. Клонирование репозитория

```bash
git clone https://github.com/SPinigin/GazpromNedra_TestApp
```
```bash
cd GazpromNedra_TestApp
```

2. Установка зависимостей

```bash
pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

3. Docker

```bash
docker --version
```
```bash
docker-compose --version
```

4. Настройка окружения

```bash
cp .env.example .env
```

5. Запуск БД для разработки

```bash
docker-compose -f docker-compose.dev.yml up -d db # Запуск PostgreSQL в контейнере
```
```bash
docker-compose -f docker-compose.dev.yml ps # Проверка запуска БД
```

6. Создание миграций

```bash
alembic revision --autogenerate -m "Initial migration" # Создание миграции
```
```bash
alembic upgrade head # Применение миграции
```
```bash
docker-compose -f docker-compose.dev.yml exec db psql -U postgres -d license_db -c "\dt" # Проверка таблиц в БД
```

7. Инициализация данных
```bash
python init_data.py # Скрипт инициализации
```

8. Запуск приложения

```bash
docker-compose -f docker-compose.dev.yml down # Остановка dev БД
```
```bash
docker-compose up --build # Запуск приложения
```
```bash
docker-compose exec app python init_data.py # Инициализация данных
```

## 🧪 ТЕСТИРОВАНИЕ
Swagger UI доступен по адресу: [localhost](http://localhost:8000/docs)

## 📈 СПРАВОЧНЫЕ ДАННЫЕ
1. Предприятия:

- ОАО Газпром (ID: 1)
- ОАО Роснефть (ID: 2)
- ПАО ЛУКОЙЛ (ID: 3)
- ОАО Сургутнефтегаз (ID: 4)
- ОАО Башнефть (ID: 5)

2. Статусы лицензий:

- действующая (ID: 1)
- переоформленная (ID: 2)
- архивная (ID: 3)

3. Статусы скважин:

- в бурении (ID: 1)
- в эксплуатации (ID: 2)
- в консервации (ID: 3)
- ликвидирована (ID: 4)
- в испытании (ID: 5)

## 🧪 ТЕСТОВЫЕ ДАННЫЕ

## 📈 Лицензии

```json
{
  "license_number": "ГС 12345 МО",
  "issue_date": "2023-01-15",
  "expire_date": "2028-01-15",
  "org_id": 1,
  "status_id": 1
}
```
```json
{
  "license_number": "НФ 67890 ТТ",
  "issue_date": "2022-06-10",
  "expire_date": "2027-06-10",
  "org_id": 2,
  "status_id": 1
}
```
```json
{
  "license_number": "РЗ 11111 СП",
  "issue_date": "2021-03-20",
  "expire_date": "2031-03-20",
  "org_id": 3,
  "status_id": 2
}
```
```json
{
  "license_number": "РЗ 11111 СП",
  "issue_date": "2021-03-20",
  "expire_date": "2031-03-20",
  "org_id": 3,
  "status_id": 2
}
```
```json
{
  "license_number": "АР 99999 КМ",
  "issue_date": "2018-12-01",
  "expire_date": "2023-12-01",
  "org_id": 4,
  "status_id": 3
}
```
```json
{
  "license_number": "ЛК 55555 БШ",
  "issue_date": "2024-02-14",
  "expire_date": "2034-02-14",
  "org_id": 3,
  "status_id": 1
}
```

## 📈 Скважины

```json
{
  "name": "86П",
  "depth": 3500.75,
  "drilling_date": "2023-05-15",
  "license_id": 1,
  "status_id": 2
}
```
```json
{
  "name": "70Р",
  "depth": 1250.0,
  "drilling_date": "2024-01-10",
  "license_id": 2,
  "status_id": 1
}
```
```json
{
  "name": "1222БИС",
  "depth": 4200.5,
  "drilling_date": "2022-08-22",
  "license_id": 1,
  "status_id": 2
}
```
```json
{
  "name": "202",
  "depth": 2800.25,
  "drilling_date": "2021-11-05",
  "license_id": 3,
  "status_id": 3
}
```
```json
{
  "name": "605Г",
  "depth": 1500.0,
  "drilling_date": "2019-03-15",
  "license_id": 4,
  "status_id": 4
}
```
```json
{
  "name": "Тест",
  "depth": 5000.0,
  "drilling_date": "2024-03-01",
  "license_id": 2,
  "status_id": 5
}
```
