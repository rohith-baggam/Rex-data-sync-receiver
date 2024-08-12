from data_sync.models import DataSyncTestForeignKeyModel
from django.db import models
from django.apps import apps


def get_model_details(model: models.Model) -> dict:
    models = {}
    model_name = model._meta.object_name
    fields = [{
        'title': field.name,
        'internal_type': field.get_internal_type()
    }
        for field in model._meta.fields]
    models[model_name] = fields

    return models
