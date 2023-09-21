# hw04_tests

## Добавляем тестирование в проект [социальная сеть Yatube](https://github.com/Olga-Zholudeva/hw03_forms)

## Что тестируем:

- Корректное отображается значение поля __str__ в объектах моделей Post и Group
- Доступность страниц и названия шаблонов приложения, проверка учитывает права доступа
- Корректное отображение запроса к несуществующей странице
- Проверяем, что во view-функциях используются правильные html-шаблоны
- Проверяем, соответствует ли ожиданиям словарь context, передаваемый в шаблон при вызове
- Проверяем, что если при создании поста указать группу, то этот пост появляется:
  - на главной странице сайта
  - на странице выбранной группы
  - в профайле пользователя
- Проверьяем, что этот пост не попал в группу, для которой не был предназначен
- Проверяем, что при отправке валидной формы со страницы создания поста reverse('posts:create_post') создаётся новая запись в базе данных
- Проверяем, что при отправке валидной формы со страницы редактирования поста reverse('posts:post_edit', args=('post_id',)) происходит изменение поста с post_id в базе данных


### Технологии
- Python 3.7
- Django 2.2.19

### Запуск тестов:

- Клонируем репозиторий: **git clone [hw04_tests](https://github.com/Olga-Zholudeva/hw04_tests)**
- Cоздаем и активировируем виртуальное окружение: **python3 -m venv env source env/bin/activate**
- Устанавливаем зависимости из файла requirements.txt: **pip install -r requirements.txt**
- Переходим в папку yatube: **cd yatube**
- Применяем миграции: **python manage.py makemigrations**
- Создаем супер пользователя: **python manage.py createsuperuser**
- Применяем статику: **python manage.py collectstatic**
- Запускаем тесты: **python manage.py test**

### Проект выполнила:

 **Ольга Жолудева**
