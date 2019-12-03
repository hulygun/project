#!/usr/bin/env python
"""
grpc books server
"""
import locale
import logging
from concurrent import futures

import grpc
from google.protobuf.empty_pb2 import Empty

from books import all_data, DataMeta
from gw import gateway_pb2
from gw import gateway_pb2_grpc
from google.protobuf.message import Message
from books import models


class BookService(gateway_pb2_grpc.BookServicer):
    """
    Books data grpc service
    """

    def __getattribute__(self, item):
        if item in ['apply_locale', 'data2model', 'get_data', 'filtered_data']:
            return super().__getattribute__(item)
        elif item.startswith('get'):
            return self.get_data
        elif item.startswith('filter'):
            return self.filtered_data

    def get_data(self, request, context):
        self.apply_locale(context)
        data = getattr(models, request.book_type, None)
        model = getattr(gateway_pb2, request.book_type)
        result = self.data2model(data.get(request.id), model())
        return result

    def filtered_data(self, request, context):
        self.apply_locale(context)
        book_type = 'Datatype'
        data = all_data()
        if not isinstance(request, Empty):
            book_type = request.book_type
            data = getattr(models, book_type, None).filter(request.ids)

        model = getattr(gateway_pb2, book_type)

        result = [self.data2model(obj, model()) for obj in data]
        return getattr(gateway_pb2, 'Filtered{}'.format(book_type))(results=result)

    @staticmethod
    def apply_locale(context) -> None:
        """
        Apply locale from request context
        """
        loc = filter(lambda metadata: metadata.key == 'lang-bin', context.invocation_metadata()).__next__().value
        loc = loc.decode('utf8').replace('-', '_').split(',')[0]
        loc = '{}.UTF-8'.format(loc)
        locale.setlocale(locale.LC_MESSAGES, loc)

    @staticmethod
    def data2model(data: DataMeta, model: Message) -> Message:
        """
        Convert dict like data to protobuf message Model
        """
        for k, v in data.dict().items():
            setattr(model, k, v)
        return model


def serve():
    """

    :return:
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gateway_pb2_grpc.add_BookServicer_to_server(BookService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
