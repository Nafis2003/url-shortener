from tortoise import fields
from tortoise.models import Model

class URL(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255)
    short_url = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    def to_json(self):
        return {
            "id": self.id,
            "url": self.url,
            "short_url": self.short_url,
            "created_at": str(self.created_at)
        }