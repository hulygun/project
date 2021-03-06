Сервис Book
===========

.. csv-table::
   :header: "Редакция", "Автор", "Основание"

   "2019-11-08", "hulygun", "Cоздание документа"

.. contents:: Содержание
   :depth: 2
   :local:

Описание сервиса
----------------

Сервис предоставляет доступ к справочным данным проекта. Это наборы неизменяемых объектов, содержащие собственные
идентификаторы для построения отношений между остальными сервисами проекта. Текстовые значения полей объекта могут
быть переводимыми на разные языки. Для интернационализации объектов используется системный **gettext**

.. warning:: **Идентификаторы объектов не должны меняться!** Только их описания и свойства

Справочники
-----------

Формат хранения справочных данных
.................................

- Справочники хранятся в директории ```data``` в формате JSON
- Название файла должно соответствовать названию модели представления этих данных
- Каждый объект справочника должен иметь уникальный идентификатор в рамках текущего справочника
- Для интернационализации справочников некоторые поля могут быть переводимыми. Для этого используется префикс ```_```
- В качестве значений переводимых полей используется английский вариант значения

:Пример объекта:

.. code-block::

    [
      # ...
      {
        "id": 2,  # Идентификатор объекта
        "one": "Непереводимая строка",
        "two": "_Строка с переводом"
      }
      # ...
    ]


.. note:: Смена локали на стороне сервера происходит по ```locale.setlocale(locale.LC_MESSAGES, '{locale}')```
         Локаль в запросах должна передаваться в формате **xx_YY** или **xx-YY**

Формат представления справочных данных
......................................

- Каждой модели представления объектов справочника должен соответствовать инстанс :class:`pydantic.BaseModel`
- Для описания переводимых полей используется тип поля :class:`TranslatableStr`

:Пример объектов:

.. code-block::

    from pydantic import BaseModel


    class DataModel(BaseModel):
        """Инстанс pydantic.BaseModel"""
        id: int
        name: TranslatableStr
        slug: str


    class TestData(BaseDataModel):
        """
        Модель представления справочных данных.
        Ресурсом будет являться data/testdata.json
        """
        _model = DataModel

.. note:: Смена локали на стороне сервера происходит по ```locale.setlocale(locale.LC_MESSAGES, '{locale}')```
         Локаль в запросах должна передаваться в формате **xx_YY** или *xx-YY*

Функционал сервиса
------------------

.. autofunction:: books.all_data

.. automethod:: books.BaseDataModel.get

.. automethod:: books.BaseDataModel.filter

Интернационализация
-------------------

Контейнер использует локализацию системы. Все доступные локали описываются в файле ```books/locale.gen```

:Пример файла:

.. code-block::

   en_US.UTF-8 UTF-8
   ru_RU.UTF-8 UTF-8

На основе этого файла генерируются шаблон и файлы переводов переводимых данных справочника. Генерация и компиляция
переводов представлена двумя утилитами **makemessages** и **compilemessages**

:Создание/обновление шаблона и файлов перевода:

```./services/books/bin/makemessages```

:Компиляция переводов:

```./services/books/bin/compilemessages```


FEATURES
--------

- получить список доступных ресурсов с описанием


