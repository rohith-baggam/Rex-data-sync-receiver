from django.core.management.base import BaseCommand
from data_sync.receiver_utils.script import (
    token_verification,
    secret_key_verification,
    schema_verification,
    data_information,
    data_transformation
)
from data_sync.receiver_utils.cipher import encrypt_data


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # data = token_verification()
        # print('test-output', data)
        # print('token_verification', token_verification())
        # print('secret_key_verification', secret_key_verification())
        # print('schema_verification', schema_verification())
        print('data_transformation()', data_transformation())
        # pass
        # schema_verification()
        # print(encrypt_data("0d7cabc45ad811efb4fcc91c1b62be3d"))
