# api_user_feedback

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/) [![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/) [![Django REST framework](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/) [![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://djoser.readthedocs.io/en/latest/introduction.html)
___
## Описание  <a id="Content"></a> 
Сервис собирает отзывы пользователей на произведения: "Фильмы", "Музыка", "Книги". Стек: Python, Django, Django REST Framework, JWT
___
##  Установка
### Как запустить проект:

1.Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ShunyaBo/api_user_feedback.git
```

```
cd api_user_feedback
```

2.Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
# для OS Lunix и MacOS
source venv/bin/activate

# для OS Windows
source venv/Scripts/activate
```

3.Обновить pip:

```
python3 -m pip install --upgrade pip
```

4.Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

5.Выполнить миграции на уровне проекта:

```
python3 manage.py makemigrations
python3 manage.py migrate
```
6.Запустить проект, находясь в директории, где расположен файл manage.py
```
python3 manage.py runserver
```
___
## Авторы
[Антон Шапиро](https://github.com/antonshapiro)
[Василий Фролов](https://github.com/Vas0017)
[Мария - ShunyaBo](https://github.com/ShunyaBo)
___
[*Вверх*](#Content)