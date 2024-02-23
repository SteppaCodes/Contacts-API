from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel
from apps.groups.models import Group


class Contact(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country_code = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    contact_picture = models.URLField(null=True, blank=True)
    is_favourite = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="group_contacts")

    def __str__(self):
        return f"{self.first_name}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
