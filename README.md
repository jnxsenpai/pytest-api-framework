# 🧪 Pytest API Framework

[**English**](#english) · [**Русский**](#russian)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-9.1-0A9EDC?logo=pytest&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.13-E92063?logo=pydantic&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-FF6B6B)
![License](https://img.shields.io/badge/License-MIT-blue)

---

<a name="english"></a>

## 🇬🇧 English

A layered **API test automation framework** built on **Pytest**, **requests**, and **Pydantic**. Every response is validated against a schema, every request is generated with Faker, and every step is reported in Allure — no more manual assertions on raw JSON.

### ✨ Features

- 🧱 **Layered architecture** — service clients, config, utils, and tests are cleanly separated
- 🛡 **Pydantic response validation** — status code + schema + field constraints in one place
- 📊 **Allure reporting** — steps, titles, and automatic JSON attachments
- 🎲 **Faker-based payloads** — valid data out of the box, with override support
- 🔌 **Fixture-based dependency injection** — `BaseTest` injects `products_api` into every test
- 🏷 **Pytest markers** — `smoke`, `regression`, `negative` for flexible selection
- 🌍 **Multi-stage support** — switch environments via the `STAGE` variable

### 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| **Pytest 9.1** | Test runner and fixtures |
| **requests** | HTTP client |
| **Pydantic 2.13** | Response schema validation |
| **Allure-pytest** | Reporting |
| **Faker** | Test data generation |
| **python-dotenv** | Environment configuration |

### 🏗 Project Structure

```
pytest-api-framework/
├── config/                  # Configuration layer
│   ├── base_test.py         # BaseTest with autouse fixture injection
│   ├── headers.py           # Auth headers
│   └── stages.py            # Stage selection via STAGE env var
├── services/                # Service clients (API layer)
│   └── products/
│       ├── api.py           # Products client (get, create, etc.)
│       ├── endpoints.py     # URL builders per stage
│       ├── payloads.py      # Faker-based request payloads
│       └── models/
│           └── model_products.py  # Pydantic response models
├── tests/                   # Test suites
│   └── test_products.py     # Product API tests
├── utils/                   # Utilities
│   └── helper.py            # validate_response + Allure attachment
├── conftest.py              # Session and function fixtures
├── pytest.ini               # Markers configuration
└── requirements.txt
```

### 🔍 How It Works

**1. Service layer.** `services/products/api.py` defines a `Products` client that builds requests, calls the API, and hands the response to `validate_response`. Each service lives in its own folder — add a new one by copying the structure.

**2. Response validation.** `utils/helper.py` contains `validate_response`, which:
- asserts the expected status code,
- parses JSON and attaches it to the Allure report,
- instantiates the given Pydantic model,
- returns a typed object (e.g. `ProductsResponse`), so tests work with attributes, not dict keys.

**3. Fixture injection.** `BaseTest` uses an `autouse` fixture to set `self.products_api` — every test method can immediately call `self.products_api.get_products()`. The `products` fixture is session-scoped: one client instance per run.

**4. Data generation.** `Payloads.create_product` uses Faker for required fields (`name`, `price`, `category`) and includes optional fields only if explicitly passed — no more hardcoded test data.

### 🧪 Example Test

```python
class TestProducts(BaseTest):

    @allure.title("Get products with default parameters")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_products(self):
        response = self.products_api.get_products()
        assert response.meta.page == 1
        assert response.meta.per_page == 20
        assert len(response.data) <= response.meta.per_page
```

The test reads as a business assertion: call the service, then check the typed response. The heavy lifting — HTTP, status assertion, schema validation, Allure attachment — is handled by the framework.

### 🚀 Installation and Run

**1. Clone the repository:**

```bash
git clone https://github.com/jnxsenpai/pytest-api-framework.git
cd pytest-api-framework
```

**2. Create and activate a virtual environment:**

```bash
python -m venv .venv

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. Configure the environment.** Set the stage (and, ideally, the API token) via `.env`:

```env
STAGE=dev
# API_TOKEN=your_token_here
```

> ⚠️ Currently the token is read from `config/headers.py`. To avoid hardcoding, replace it with `os.getenv("API_TOKEN")` and put the real value in `.env`.

**5. Run tests:**

```bash
# All tests
pytest

# Smoke only
pytest -m smoke

# Regression only
pytest -m regression

# With verbose output
pytest -sv
```

**6. Generate an Allure report:**

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### 🧭 Markers

Defined in `pytest.ini`:

- `smoke` — critical happy-path checks
- `regression` — full regression suite
- `negative` — negative scenarios

---

<a name="russian"></a>

## 🇷🇺 Русский

Многослойный **фреймворк для тестирования API** на **Pytest**, **requests** и **Pydantic**. Каждый ответ валидируется по схеме, каждое тело запроса генерируется через Faker, а каждый шаг попадает в Allure — больше не нужно вручную проверять сырой JSON.

### ✨ Возможности

- 🧱 **Слоистая архитектура** — клиенты сервисов, конфигурация, утилиты и тесты разделены
- 🛡 **Валидация ответов через Pydantic** — статус-код, схема и ограничения полей в одном месте
- 📊 **Allure-отчётность** — шаги, заголовки и автоматическое прикрепление JSON
- 🎲 **Payload'ы на Faker** — валидные данные «из коробки» с возможностью переопределения
- 🔌 **Инъекция зависимостей через фикстуры** — `BaseTest` внедряет `products_api` в каждый тест
- 🏷 **Маркеры Pytest** — `smoke`, `regression`, `negative` для гибкой выборки
- 🌍 **Поддержка стендов** — переключение через переменную `STAGE`

### 🛠 Стек

| Инструмент | Назначение |
|---|---|
| **Pytest 9.1** | Раннер тестов и фикстуры |
| **requests** | HTTP-клиент |
| **Pydantic 2.13** | Валидация схемы ответов |
| **Allure-pytest** | Отчётность |
| **Faker** | Генерация тестовых данных |
| **python-dotenv** | Конфигурация окружения |

### 🏗 Структура проекта

```
pytest-api-framework/
├── config/                  # Конфигурация
│   ├── base_test.py         # BaseTest с autouse-фикстурой
│   ├── headers.py           # Заголовки авторизации
│   └── stages.py            # Выбор стенда через STAGE
├── services/                # Клиенты сервисов (API-слой)
│   └── products/
│       ├── api.py           # Клиент Products (get, create и т.д.)
│       ├── endpoints.py     # Построение URL для стенда
│       ├── payloads.py      # Payload'ы на Faker
│       └── models/
│           └── model_products.py  # Pydantic-модели ответов
├── tests/                   # Тесты
│   └── test_products.py     # Тесты продуктов
├── utils/                   # Утилиты
│   └── helper.py            # validate_response + вложение в Allure
├── conftest.py              # Сессионные и функциональные фикстуры
├── pytest.ini               # Настройка маркеров
└── requirements.txt
```

### 🔍 Как это работает

**1. Слой сервисов.** `services/products/api.py` описывает клиент `Products`, который собирает запрос, вызывает API и передаёт ответ в `validate_response`. Каждый сервис живёт в своей папке — новый добавляется копированием структуры.

**2. Валидация ответов.** `utils/helper.py` содержит `validate_response`, который:
- проверяет ожидаемый статус-код,
- парсит JSON и прикрепляет его к Allure-отчёту,
- создаёт объект указанной Pydantic-модели,
- возвращает типизированный объект (например, `ProductsResponse`), поэтому тесты работают с атрибутами, а не с ключами словаря.

**3. Инъекция через фикстуры.** `BaseTest` использует `autouse`-фикстуру, которая устанавливает `self.products_api` — каждый тест сразу может вызвать `self.products_api.get_products()`. Фикстура `products` сессионная: один экземпляр клиента на прогон.

**4. Генерация данных.** `Payloads.create_product` использует Faker для обязательных полей (`name`, `price`, `category`) и добавляет опциональные только если они явно переданы — никаких захардкоженных тестовых данных.

### 🧪 Пример теста

```python
class TestProducts(BaseTest):

    @allure.title("Get products with default parameters")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_products(self):
        response = self.products_api.get_products()
        assert response.meta.page == 1
        assert response.meta.per_page == 20
        assert len(response.data) <= response.meta.per_page
```

Тест читается как бизнес-проверка: вызвать сервис, проверить типизированный ответ. Вся тяжёлая работа — HTTP, проверка статуса, валидация схемы, вложение в Allure — скрыта во фреймворке.

### 🚀 Установка и запуск

**1. Клонировать репозиторий:**

```bash
git clone https://github.com/jnxsenpai/pytest-api-framework.git
cd pytest-api-framework
```

**2. Создать и активировать виртуальное окружение:**

```bash
python -m venv .venv

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate
```

**3. Установить зависимости:**

```bash
pip install -r requirements.txt
```

**4. Настроить окружение.** Укажи стенд (и, в идеале, токен) через `.env`:

```env
STAGE=dev
# API_TOKEN=your_token_here
```

> ⚠️ Сейчас токен читается из `config/headers.py`. Чтобы избежать хардкода, замени его на `os.getenv("API_TOKEN")`, а реальное значение положи в `.env`.

**5. Запустить тесты:**

```bash
# Все тесты
pytest

# Только smoke
pytest -m smoke

# Только regression
pytest -m regression

# С подробным выводом
pytest -sv
```

**6. Сгенерировать Allure-отчёт:**

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### 🧭 Маркеры

Определены в `pytest.ini`:

- `smoke` — критичные проверки happy path
- `regression` — полный регрессионный набор
- `negative` — негативные сценарии
