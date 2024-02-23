from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel


class Group(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_groups')
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.name

    