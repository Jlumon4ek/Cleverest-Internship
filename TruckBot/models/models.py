from tortoise.models import Model
from tortoise import fields
import json


class Truck(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    govNumber = fields.CharField(max_length=255)
    driver = fields.CharField(max_length=255)

    def __str__(self):
        return json.dumps({'name': self.name, 'govNumber': self.govNumber, 'driver': self.driver})
