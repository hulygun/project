"""
Catalog models
"""

from pydantic import BaseModel

from . import BaseDataModel, TranslatableStr


class DataModel(BaseModel):
    """Data model"""
    id: int
    name: TranslatableStr


class Data(BaseDataModel):
    """Test Data model"""
    _model = DataModel
