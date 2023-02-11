import collections
from configparser import ConfigParser
from configparser import NoOptionError
from configparser import NoSectionError

from django.core.exceptions import ImproperlyConfigured


class ProjectConfig:

    """Обертка над парсером параметров конфигурации."""

    def __init__(self, filenames=None, defaults=None):
        self.parser = ConfigParser()
        if filenames:
            self.parser.read(filenames)
        self.defaults = defaults

    def read(self, filenames):
        """Загружает конфигурацию из файла(ов) filenames."""
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(filenames)

    def set_defaults(self, defaults):
        """Устанавливает параметры проекта по умолчанию."""
        self.defaults = defaults

    def items(self, section):
        """Возвращает список кортежей (key, value) из указанной секции.

        В случае, если такой секции нет, то возвращается пустой список.
        """
        if self.parser.has_section(section):
            result = self.parser.items(section)
        else:
            result = []

        return result

    def get(self, section, option, quiet=True, validation=None, raw=False):
        """Возвращает значение параметра в виде строки.

        :param str section: Название раздела.
        :param str option: Название параметра.
        :param bool quiet: Флаг, определяющий необходимость генерации
            исключения django.core.exceptions.ImproperlyConfigured в случае,
            если запрашиваемого параметра нет ни в файлах конфигурации, ни в
            словаре дефолтных значений.
        :param lambda|None validation: Функция валидирующая значение,
            например lambda v: True.
        :return str: Полученое значение

        :raises django.core.exceptions.ImproperlyConfigured: если аргумент
            *quiet* равен *False* и указанного параметра нет ни в файлах
            конфигурации, ни в словаре дефолтных значений.
        """
        key = (section, option)

        try:
            result = self.parser.get(section, option, raw=raw).strip()
        except (NoSectionError, NoOptionError):
            result = None

        if not result:
            # В конфигурационных файлах запрашиваемый параметр отсутствует,
            # пробуем вернуть дефолтное значение.
            if key not in self.defaults:
                if quiet:
                    result = ''
                else:
                    raise ImproperlyConfigured(
                        'Configuration parameter {0}.{1} not found'.format(
                            section, option
                        )
                    )
            else:
                result = self.defaults[key]

        if validation and isinstance(validation, collections.Callable) and not validation(result):
            raise ImproperlyConfigured(
                'Configuration parameter `{0}.{1} = {2}` is invalid'.format(
                    section, option, result
                )
            )

        return result

    def get_bool(self, section, option, allow_none=False, quiet=True):
        """Возвращает значение параметра в виде булевого значения.

        Если значение параметра равно (без учета регистра символов) True, то
        метод возвращает истинное значение (True), иначе - ложь (False).

        :param str section: Название раздела.
        :param str option: Название параметра.
        :param bool allow_none: Флаг, разрешающий 3-ую логику с возвратом None.
        :param bool quiet: Флаг, определяющий необходимость генерации
            исключения django.core.exceptions.ImproperlyConfigured в случае,
            если запрашиваемого параметра нет ни в файлах конфигурации, ни в
            словаре дефолтных значений.

        :rtype: bool

        :raises django.core.exceptions.ImproperlyConfigured: если аргумент
            *quiet* равен *False* и указанного параметра нет ни в файлах
            конфигурации, ни в словаре дефолтных значений.
        """
        value = self.get(section, option, quiet)
        # из конфига приходят строковые значения, а из KINDER_DEFAULT_CONFIG
        # булевые или None
        value = str(value).upper()
        if value not in ['TRUE', 'FALSE', '', 'NONE', None]:
            raise ImproperlyConfigured(
                f'Параметр настроек [{section}] {option} '
                f'Должен иметь значения True, False или ""'
            )

        result = (value == 'TRUE')

        if allow_none and not result:
            result = False if (value == 'FALSE') else None

        return result

    def get_int(self, section, option, default=None, quiet=True,
                min_value=None, max_value=None):
        """Возвращает значение параметра в виде целого числа.

        Если значение отсутствует в конфигурации системы и в словаре дефольных
        значений, а также параметр quiet равен True, возвращает 0 (ноль).

        :param str section: Название раздела.
        :param str option: Название параметра.
        :param bool quiet: Флаг, определяющий необходимость генерации
            исключения django.core.exceptions.ImproperlyConfigured в случае,
            если запрашиваемого параметра нет ни в файлах конфигурации, ни в
            словаре дефолтных значений.
        :param default: Значение по умолчанию для параметра. Проставляется,
            если quiet=True и параметр не указан в конфигурации
        :param default: Optional[int]
        :param min_value: Минимально допустимое значение
        :type min_value: Optional[Union[int, float]]
        :param max_value: Максимально допустимое значение
        :type max_value: Optional[Union[int, float]]

        :rtype: int

        :raises django.core.exceptions.ImproperlyConfigured: если аргумент
            *quiet* равен *False* и указанного параметра нет ни в файлах
            конфигурации, ни в словаре дефолтных значений, или если указаны
            min_value и/или max_value и значение не удовлетворяет указанным
            условиям.
        """
        value = self.get(section, option, quiet)
        # Если параметр не задан и параметр не обязателен (quiet=True),
        # то проставляем default, если он задан
        if not value and default is not None:
            value = default

        try:
            result = int(value)
        except:
            result = 0

        # Проверка принадлежности числа интервалу
        if not self.is_number_in_interval(result, min_value, max_value):
            raise ImproperlyConfigured(
                f'Параметр [{section}] {option} не удовлетворяет условиям')

        return result

    def get_uint(self, section, option, quiet=True):
        """Возвращает значение параметра в виде беззнакового целого числа.

        Если значение отсутствует в конфигурации системы и в словаре дефольных
        значений, а также параметр quiet равен True, либо значение параметра
        является отрицательным числом, возвращает 0 (ноль).

        :param str section: Название раздела.
        :param str option: Название параметра.
        :param bool quiet: Флаг, определяющий необходимость генерации
            исключения django.core.exceptions.ImproperlyConfigured в случае,
            если запрашиваемого параметра нет ни в файлах конфигурации, ни в
            словаре дефолтных значений.

        :rtype: int

        :raises django.core.exceptions.ImproperlyConfigured: если аргумент
            *quiet* равен *False* и указанного параметра нет ни в файлах
            конфигурации, ни в словаре дефолтных значений.
        """
        result = self.get_int(section, option)
        if result < 0:
            result = 0

        return result

    def get_list(self, section, option, quiet=True):
        """Возвращает список значений параметра.

        Принимает параметр в виде строки элементов разделенных запятой.
        Если значение отсутствует в конфигурации системы и в словаре дефолтных
        значений, а также параметр quiet равен True возвращает пустой список.

        :param str section: Название раздела.
        :param str option: Название параметра.
        :param bool quiet: Флаг, определяющий необходимость генерации
            исключения django.core.exceptions.ImproperlyConfigured в случае,
            если запрашиваемого параметра нет ни в файлах конфигурации, ни в
            словаре дефолтных значений.

        :raises django.core.exceptions.ImproperlyConfigured: если аргумент
            *quiet* равен *False* и указанного параметра нет ни в файлах
            конфигурации, ни в словаре дефолтных значений.
        """
        items = self.get(section, option)

        if isinstance(items, str):
            items = items.split(',')

        result = [i.strip() for i in items]
        if not quiet and not result:
            raise ImproperlyConfigured(
                'Configuration parameter {0}.{1} not found'.format(
                            section, option)
                )

        return result

    def get_tuple(self, section, option):
        """
        Возвращает кортеж из опции @option конфига секции @section
        Разделитель в конфиге - запятая
        Допускается разделение по строкам
        :param str section: секция настроек
        :param str option: опция секции
        :rtype: tuple
        """
        sep = ','
        return tuple([
            i.strip() for i in self.get(section, option).split(sep) if i
        ])

    @staticmethod
    def is_number_in_interval(value, min_value=None, max_value=None):
        """Проверка принадлежности числа определённому интервалу.

        :param value: Проверяемое число
        :type value: Union[int, float]
        :param min_value: Минимально допустимое значение или None
        :type min_value: Optional[Union[int, float]]
        :param max_value: Максимально допустимое значение или None
        :type max_value: Optional[Union[int, float]]

        :return: Принадлежность числа интервалу
        :rtype: bool
        """
        return ((min_value is None or min_value <= value) and
                (max_value is None or value <= max_value))
