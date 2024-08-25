from django.test import TestCase
from django.core.management import call_command
from data_sync.receiver_utils.script import (
    token_verification,
    secret_key_verification,
    schema_verification,
    data_information,
    data_transformation
)
from core.settings import SENDER_HOST, DATA_SYNC_SENDER_TOKEN
from data_sync.receiver_utils.cipher import (
    encrypt_data,
    decrypt_data
)
from django_data_seed.utils.colorama_theme import StdoutTextTheme
# Create your tests here.


class DataSyncSenderTestCase(TestCase, StdoutTextTheme):
    def setUp(self):
        # Seeding data with 10 objects
        call_command(
            'seeddata',
            '--no-of-objects',
            '10'
        )
        self.script_info = {
            'token_verification': {
                'function': token_verification,
                'success_message': 'Token verification passed: Token is verified successfully.',
                'error_message': 'Token verification failed: Incorrect token provided.',
                'args': {}
            },
            'secret_key_verification': {
                'function': secret_key_verification,
                'success_message': 'Secret key verification passed: Secret key is verified successfully.',
                'error_message': 'Secret key verification failed: Incorrect Secret key provided.',
                'args': {}
            },
            'schema_verification': {
                'function': schema_verification,
                'success_message': 'Schema verification passed: Schema is matched successfully.',
                'error_message': 'Schema verification failed: Schema does not match the expected structure.',
                'args': {}
            },
            'data_information': {
                'function': data_information,
                'success_message': 'Data information retrieved successfully: Number of data packets to transfer received.',
                'error_message': 'Data information retrieval failed: Error while extracting size of data packets to transfer.',
                'args': {}
            },
            'data_transformation': {
                'function': data_transformation,
                'success_message': 'Data transformation passed: Data transformed successfully.',
                'error_message': 'Data transformation failed: Error occurred while transforming data.',
            }
        }

    def test_script_data(self):
        # ? Verify the sender host and token configuration
        self.assertEqual(bool(SENDER_HOST), True,
                         "Sender host configuration is missing.")
        self.stdout_info('Configuration check passed: Sender host found.')

        self.assertEqual(bool(DATA_SYNC_SENDER_TOKEN), True,
                         "Sender token configuration is missing.")
        self.stdout_info('Configuration check passed: Sender token found.')

        # ? Test encryption and decryption consistency
        data = 'Test data to encrypt'
        test_1_encrypt_data = encrypt_data(data)
        test_2_encrypt_data = encrypt_data(data)

        # ? Ensure the encryption generates unique hashes
        self.assertNotEqual(
            test_1_encrypt_data,
            test_2_encrypt_data,
            "Encryption check failed: Identical data should not produce the same hash."
        )
        self.stdout_success(
            'Encryption check passed: Unique hashes generated for identical data.')

        # ? Ensure that even with different hashes, decryption results are the same
        self.assertEqual(
            decrypt_data(test_1_encrypt_data),
            decrypt_data(test_2_encrypt_data),
            "Decryption consistency check failed: Decrypted results should be identical despite different hashes."
        )
        self.stdout_success(
            'Decryption consistency check passed: Identical results obtained after decrypting different hashes.')

        # ? Ensure the decrypted data matches the original input
        self.assertEqual(
            data,
            decrypt_data(test_1_encrypt_data),
            "Final decryption check failed: Decrypted data does not match the original input."
        )
        self.stdout_success(
            'Final decryption check passed: Data decrypted successfully.')

        for script_key in self.script_info.keys():
            is_schema_verified = False
            script_function = self.script_info[script_key]['function']
            try:
                # ? Execute the script function
                script_function()
                is_schema_verified = True
                print(self.script_info[script_key]['success_message'])
            except Exception:
                is_schema_verified = False
                print(self.script_info[script_key]['error_message'])
            # ? Assert that the script function executed successfully
            self.assertEqual(is_schema_verified, True)
