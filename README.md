# Marketing Data Analysis Project

## Введение

Этот проект был создан для демонстрации навыков работы с DBT (Data Build Tool) и анализа данных, используя базу данных SQLite. В проекте используется маркетинговый датасет, который был импортирован из файла `Marketing.csv` и преобразован в базу данных SQLite. Проект включает в себя несколько моделей для анализа данных и тестов для проверки качества данных.

Изначально планировалось использовать Google BigQuery для хранения данных, и установка и настройка этого инструмента была завершена. Однако позже стало известно, что для использования BigQuery требуется платная подписка. Аналогично, инструмент Looker также оказался платным, что повлияло на выбор решений. В итоге, из-за ограничений на использование платных сервисов, было принято решение использовать SQLite в качестве базы данных.

**Источник данных:** Маркетинговый датасет, использованный в проекте, можно найти на Kaggle: [Digital Marketing Metrics & KPIs to Measure](https://www.kaggle.com/datasets/sinderpreet/analyze-the-marketing-spending/data).

## Структура проекта

Проект содержит следующие папки и файлы:

- `models/`: Модели DBT.
- `tests/`: Тесты для моделей DBT.
- `input_data/`: Датасет в формате CSV (`Marketing.csv`), используемый для создания базы данных.
- `create_db.py`: Скрипт для создания базы данных SQLite и загрузки данных из CSV.
- `marketing.db`: SQLite база данных с сырыми данными.
- `dashboard.pdf`: Сохраненная версия дэшборда в формате PDF.

## Создание базы данных SQLite

Данные из файла `Marketing.csv` были импортированы в базу данных SQLite с помощью скрипта `create_db.py`. Этот скрипт создал две таблицы:

- **`channel`**: Содержит информацию о маркетинговых каналах.
- **`marketing_data`**: Основные данные маркетинговых кампаний, включая внешний ключ для связи с таблицей `channel`.

После выполнения скрипта в базе данных SQLite были созданы таблицы `channel` и `marketing_data`.

### Команды для создания базы данных

Выполните следующую команду для создания базы данных:
```bash
python create_db.py
```
После выполнения этой команды будет создан файл `marketing.db`, содержащий таблицы `channel` и `marketing_data`.

## Настройка DBT

Проект был инициализирован с использованием DBT, и для него были настроены соответствующие файлы конфигурации.

### Файл `dbt_project.yml`

В файле `dbt_project.yml` указаны следующие параметры:

```yaml
name: 'my_dbt_project'
version: '1.0.0'
config-version: 2

profile: 'my_dbt_project'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

clean-targets:
  - "target"
  - "dbt_packages"

models:
  my_dbt_project:
    example:
      +materialized: view
```

Этот файл настроен так, чтобы проект использовал профиль `my_dbt_project`, и все модели по умолчанию создавались как представления (views).

### Файл `profiles.yml`

Для подключения к базе данных SQLite был настроен файл `profiles.yml`, который выглядит следующим образом:

```yaml
my_dbt_project:
  target: dev
  outputs:
    dev:
      type: sqlite
      threads: 1
      database: /home/s/Code/dbt/marketing.db
      schema: main
      schema_directory: /home/s/Code/dbt/
      schemas_and_paths:
        main: /home/s/Code/dbt/marketing.db
```

Этот файл конфигурации отвечает за подключение DBT к базе данных SQLite и настройку параметров проекта.

## Модели DBT

### Модель `campaign_summary.sql`

Эта модель агрегирует данные по кампаниям и рассчитывает такие метрики, как общий доход, количество заказов и средняя стоимость клика.

```sql
WITH base_data AS (
    SELECT 
        campaign_name,
        category,
        SUM(revenue) AS total_revenue,
        SUM(orders) AS total_orders,
        SUM(clicks) AS total_clicks,
        SUM(mark_spent) AS total_spent
    FROM marketing_data
    GROUP BY campaign_name, category
)

SELECT 
    campaign_name,
    category,
    total_revenue,
    total_orders,
    total_clicks,
    total_spent,
    total_revenue / total_orders AS avg_order_value,
    total_spent / total_clicks AS avg_cpc
FROM base_data
```

### Модель `daily_summary.sql`

Эта модель агрегирует данные по дням, создавая сводные метрики за каждый день.

```sql
SELECT
    c_date,
    SUM(revenue) AS total_revenue,
    SUM(orders) AS total_orders,
    SUM(clicks) AS total_clicks,
    SUM(mark_spent) AS total_spent
FROM marketing_data
GROUP BY c_date
ORDER BY c_date
```

## Тестирование DBT

DBT включает в себя тесты, которые проверяют корректность данных, создаваемых моделями.

### Тест `unique_campaign_name.yml`

Этот тест проверяет, что поле `campaign_name` в модели `campaign_summary` уникально и не содержит `NULL` значений.

```yaml
version: 2

models:
  - name: campaign_summary
    columns:
      - name: campaign_name
        tests:
          - unique
          - not_null
```

### Важно:

Перед запуском тестов убедитесь, что в таблице `marketing_data` нет пустых значений в колонке `id`, иначе это приведёт к ошибкам в тестировании. Для удаления пустых значений выполните следующие SQL-команды:

```sql
SELECT * FROM marketing_data WHERE id IS NULL;
DELETE FROM marketing_data WHERE id IS NULL;
```

### Запуск тестов

После создания моделей запустите тесты для проверки данных:
```bash
dbt test
```

## Визуализация данных

На основе двух моделей, созданных в DBT, был разработан дэшборд в Metabase. Дэшборд включает визуализации на основе агрегированных данных кампаний и данных за каждый день. Дэшборд был сохранен в формате PDF и добавлен в репозиторий.

### Возможные улучшения

Целью проекта было протестировать инструменты для обработки данных и создания визуализаций. В будущем, при наличии дополнительного времени, можно добавить:

- Интерактивные фильтры.
- Дополнительные визуализации (например, круговые диаграммы).
- Детализированные подписи и пояснения к графикам.
- Анимации и переходы.

## Заключение

Проект демонстрирует использование DBT для обработки и анализа маркетинговых данных с помощью SQLite. Все модели и тесты были успешно выполнены, а данные визуализированы в Metabase. Проект настроен так, чтобы быть доступным и простым для воспроизведения.

Если у вас возникнут вопросы или предложения по улучшению проекта, пожалуйста, откройте Issue или отправьте Pull Request.
