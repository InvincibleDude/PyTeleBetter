from tortoise import Model, fields


class ChannelLayer(Model):
    id = fields.IntField(pk=True)
    text_id = fields.TextField()
    owner = fields.TextField()


class Account(Model):
    phone_number = fields.TextField(pk=True)
