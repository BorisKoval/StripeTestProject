### Демо версия доступна тут:
    
    http://195.133.197.210:8000/admin/
    http://195.133.197.210:8000/stripe/item/1
    http://195.133.197.210:8000/stripe/all_items/

### Установка и запуск:
- Создание окружения:

      python -m venv <название_среды>

- Активировать окружение. Например:

      source ~/<название_среды>/bin/activate

- Указать в переменных окружения: :

      # Путь до папки с конфигами
      export CONFIG_PATH=~/stripe_conf/
      # Использование настроек продуктива
      export DJANGO_SETTINGS_MODULE=settings.base

- Создать там файл с настройками stripe.conf (содержимое можно скопировать из default.conf)
- Установить зависимости и выполнить миграции:

      pip install -r requirements.txt

- Выполнить действия:

      python manage.py migrate
      python manage.py createsuperuser
      python manage.py collectstatic
      python manage.py runserver

### Использование:

    <address>/admin - Админка сайта
    <address>/stripe/item/<item id> - Покупка Item
    <address>/stripe/all_items - Покупка нескольких Item через Order
