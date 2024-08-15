from django.core.management.base import BaseCommand
from data_sync.receiver_utils.script import (
    token_verification,
    secret_key_verification,
    schema_verification
)
from data_sync.receiver_utils.cipher import encrypt_data


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # data = token_verification()
        # print('test-output', data)
        schema_verification()
        # pass
        # schema_verification()
        # print(encrypt_data("0d7cabc45ad811efb4fcc91c1b62be3d"))
