from tortoise import fields
from tortoise.models import Model

class URL(Model):
    id = fields.IntField(primary_key=True)
    url = fields.CharField(max_length=255)
    short_code = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    def to_json(self,base_url):
        return {
            "id": self.id,
            "url": self.url,
            "short_code": self.short_code,
            "short_url": base_url + "/" + self.short_code,
            "created_at": str(self.created_at)
        }