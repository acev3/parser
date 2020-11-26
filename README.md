# Проект парсер библиотеки tululu.org
Парсер научной фантастики.
## Инструкция по установке.
 Скопируйте код в свою директорию.
 Cоздать виртуальное окружение в директории с проектом:
 ```bash 
 python3 -m venv <your env>
 ```
 Активировать виртульное окружение:
  ```bash 
  source <your env>/bin/activate
  ```
 Установить зависимости
 ```bash 
 pip install -r requirements.txt
 ```
 Запустить парсер
 ```bash 
 python parse_tululu_category.py
 ```
## Аргументы
***
### --start_page
```bash
python parse_tululu_category.py --start_page <n>
```
, n - номер страницы, с который начинается парсинг
***
### --end_page
```bash
python parse_tululu_category.py --end_page <n>
```
, n - номер страницы, до которой будет идти парсинг
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.


