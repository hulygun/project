"""
Catalog
"""
import gettext
import inspect
import json
import locale
import os
from typing import Optional, Iterator

from pydantic import BaseModel, ValidationError


class TranslatableStr(ValidationError):
    """
    Translatable string
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> str:
        """
        Validate translate
        :param v:
        :return:
        """
        lang = locale.getlocale(locale.LC_MESSAGES)[0]
        if not lang:
            lang = locale.getdefaultlocale()[0]
        lang = lang.split('_')[0]

        translation = gettext.translation(
            'book',
            os.path.join(os.path.dirname(__file__), 'i18n'),
            languages=[lang],
            fallback=True
        )
        translation.install()

        return translation.gettext(v).lstrip('_')


class DataMeta(BaseModel):
    """meta info for data model"""
    name: str
    author: str
    version: float
    description: TranslatableStr


class BaseDataModel:
    """
    Base Abstract model to implement json data
    """
    _model = None
    DATA_PATH = os.getenv('DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))

    @classmethod
    def objects(cls) -> list:
        """List of object of book"""
        return cls.get_resource().get('objects')

    @classmethod
    def meta(cls) -> DataMeta:
        """meta object of instance"""
        return DataMeta(name=cls.__name__.lower(), ** cls.get_resource().get('_meta'))

    @classmethod
    def get_resource(cls) -> dict:
        """
        Get resource
        :return:
        """
        resource_path = '{path}/{name}.json'.format(
            path=cls.DATA_PATH,
            name=cls.__name__.lower()
        )
        with open(resource_path) as data:
            return json.loads(data.read())

    @classmethod
    def get(cls, obj_id: int) -> Optional[BaseModel]:
        """Возвращает один объект справочника по его ID"""
        try:
            return cls.to_obj(
                filter(lambda obj: obj['id'] == obj_id, cls.objects()).__next__()
            )
        except StopIteration:
            return None

    @classmethod
    def filter(cls, ids: list) -> Optional[Iterator[BaseModel]]:
        """Возвращает список объектов справочника по их ID"""
        return map(cls.to_obj, filter(lambda obj: obj['id'] in ids, cls.objects()))

    @classmethod
    def to_obj(cls, data: dict) -> BaseModel:
        """
        Convert dict data
        :param data:
        :return:
        """
        if cls._model:
            return cls._model(**data)


def all_data() -> Iterator[DataMeta]:
    """Возвращает список всех ресурсов сервиса"""
    from . import models
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and BaseDataModel in obj.__bases__:
            yield obj.meta()
