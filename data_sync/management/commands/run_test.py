from django.core.management.base import BaseCommand
from data_sync.receiver_utils.script import (
    token_verification,
    secret_key_verification,
    schema_verification,
    data_information,
    data_transformation,
    loaddata_from_response
)
from data_sync.receiver_utils.cipher import encrypt_data
from data_sync.receiver_utils.utils import convert_string_to_json

class Command(BaseCommand):

    def run_data_transformation(self):
        token_verification_data = convert_string_to_json(token_verification())
        print('token_verification', token_verification_data)
        if token_verification_data['data']['status_code']==200:
            print('verified')
            secret_key_verification_data = convert_string_to_json(secret_key_verification())
            if secret_key_verification_data['data']['status_code']==200:
                print('verified')
                schema_verification_data = schema_verification()
                print('schema_verification_data output',schema_verification_data, type(schema_verification_data))
                # print('schema_verification_data statuscode', schema_verification_data)
                # schema_verification_data = convert_string_to_json(schema_verification_data)
                print('schema_verification_data status code', schema_verification_data['data'], )
                print("type(schema_verification_data['data'])", type(schema_verification_data['data']))
                if secret_key_verification_data['data']['status_code']==200:
                    print('schema is verified')
                    if data_transformation():
                        print("Data transformation is done")
                    else:
                        print("Data transformation is failed")

            else:
                print('Secret key not verified')
        else:
            print('Token not verified')
        return 

    def handle(self, *args, **kwargs):
        # data = token_verification()
        # print('test-output', data)
        # loaddata_from_response(10, socket_type="data_transformation")
        self.run_data_transformation()
        # print('secret_key_verification', secret_key_verification())
        # print('data_transformation', data_transformation())
        # print('data_transformation()', data_transformation())
        # pass
        # schema_verification()
        # print(encrypt_data("0d7cabc45ad811efb4fcc91c1b62be3d"))
