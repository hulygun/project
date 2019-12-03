"""Books service routes"""
import grpc
from fastapi import Header, APIRouter, HTTPException
from google.protobuf.empty_pb2 import Empty
from google.protobuf.json_format import MessageToDict

from gw import gateway_pb2_grpc
from gw import gateway_pb2

channel = grpc.insecure_channel('book:50051')
stub = gateway_pb2_grpc.BookStub(channel)

router = APIRouter()


@router.get('/')
def types(*, accept_language: str = Header(None)) -> list:
    """Return all available data models from book service"""
    response, call = stub.filterDatatype.with_call(Empty(), metadata=(
        ('lang-bin', accept_language.encode()),
    ))
    return [MessageToDict(data) for data in response.results]


@router.get('/{data_type}')
def filtered_data(*, accept_language: str = Header(None), data_type: str, ids: str) -> list:
    request = gateway_pb2.BookIDs()
    request.book_type = data_type.title()
    request.ids.extend(map(int, ids.split(',')))
    try:
        grpc_method = getattr(stub, 'filter{}'.format(request.book_type))
        response, call = grpc_method.with_call(request, metadata=(
            ('lang-bin', accept_language.encode()),
        ))
        return [MessageToDict(data) for data in response.results]
    except AttributeError:
        raise HTTPException(status_code=404, detail='Not exist resource with name {}'.format(data_type))


@router.get('/{data_type}/{data_id}')
def get_data(*, accept_language: str = Header(None), data_type: str, data_id: int) -> dict:
    request = gateway_pb2.BookID()
    request.book_type = data_type.title()
    request.id = data_id
    try:
        grpc_method = getattr(stub, 'get{}'.format(request.book_type))
        response, call = grpc_method.with_call(request, metadata=(
            ('lang-bin', accept_language.encode()),
        ))
        return MessageToDict(response)
    except AttributeError:
        raise HTTPException(status_code=404, detail='Not exist resource with name {}'.format(data_type))