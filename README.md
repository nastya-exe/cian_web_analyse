# Парсер Циана + сайт с аналитикой

### Структура:

#### Парсер (parser):
- main_parser.py - парсер (запуск от сюда)
- functions.py - отдельные функции для парсера

#### Сайт (WEB):
- app.py - запуск сайта от сюда
- static:
  - main.css - стили
  - main.js - графики
- templates - папка с html страниц
- utils:
  - info_from_bd - запросы к БД

#### Общее:
- db_request.py - запросы к БД
- config.py - переменные
- db_cian.db - БД

### Описание:
На сайте представлена основная аналитика по объявлениям с Циана. 
Есть разделы с активными объявлениями и со всеми из БД. 
<img width="959" height="465" alt="image" src="https://github.com/user-attachments/assets/22c4c030-df06-4fea-803e-0ae3a0aa0142" />
Можно использовать фильтры, для уточнения запроса
<img width="959" height="465" alt="image" src="https://github.com/user-attachments/assets/b928c34b-372d-4827-8289-2b2a83644bfe" />
