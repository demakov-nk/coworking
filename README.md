# База данных «Коворкинг»

Учебный проект по дисциплине «Базы данных»: схема БД, генерация тестовых данных,
запросы и отчёт. Все команды запускаются через [Poetry](https://python-poetry.org/).

## Структура

```
├── src/coworking/          # исходный код (пакет)
│   ├── db/                 #   подключение, декораторы кэша, применение SQL
│   ├── data/               #   статические данные для заполнения
│   └── cli/                #   команды: fill, reset_db, view_tables
├── sql/
│   ├── schema/             # DDL: сброс и создание схемы
│   └── queries/            # аналитические запросы (предыдущий семестр)
├── tasks/                  # задания текущего семестра
│   ├── 01_views/sql/       #   представления
│   └── 02_triggers/sql/    #   триггеры
├── tests/                  # pytest-тесты заданий (нужна запущенная БД)
├── data/                   # выгрузки, планы выполнения, результаты
├── docs/report/            # отчёт LaTeX и материалы к нему
└── connection_config.json  # параметры подключения (в .gitignore)
```

## Установка

```bash
poetry lock       # пересобрать lock-файл (нужен доступ к PyPI)
poetry install
```

> В текущем окружении `poetry.lock` ещё пустой (в нём `package = []`), поэтому
> перед первым запуском нужно выполнить `poetry lock` там, где есть доступ к PyPI.
> Если пакеты уже стоят в `.venv`, можно работать сразу:
> `PYTHONPATH=src python -m coworking.cli.view_tables`.

Параметры подключения лежат в `connection_config.json` в корне проекта:

```json
{"dbname": "coworking", "user": "postgres", "password": "...", "host": "localhost", "port": 5432}
```

Другой файл можно указать переменной окружения `COWORKING_CONFIG`.

## Команды

```bash
poetry run clear_coworking        # сбросить схему и создать её заново (sql/schema/*.sql)
poetry run fill_coworking         # заполнить БД тестовыми данными
poetry run view_tables_coworking  # показать содержимое всех таблиц (--name client --rows 20)
```

После `clear_coworking` прикладные объекты заданий (представление и триггеры)
создаются применением SQL из `tasks/` по порядку:

1. `tasks/01_views/sql/req1.sql` — представление `client_stats_view`;
2. `tasks/02_triggers/sql/01_create_client_stats.sql` — таблица-копия представления;
3. `tasks/02_triggers/sql/trg_on_client/*.sql`, `trg_on_sub/*.sql`, `trg_on_visit/*.sql` — триггеры.

## Тесты

```bash
poetry run pytest
```

Тесты работают с реальной БД (параметры — из `connection_config.json`) и требуют
заполненной базы; если PostgreSQL недоступен, тесты пропускаются. Любой файл можно
запустить и как скрипт: `poetry run python tests/test_triggers_client.py`.

## Отчёт

Исходник — `docs/report/report.tex`, сборка:

```bash
cd docs/report && pdflatex report.tex
```
