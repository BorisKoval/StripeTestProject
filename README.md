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
