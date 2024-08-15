from django.core.management.base import BaseCommand
from data_sync.receiver_utils.script import token_verification


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        token_verification()
