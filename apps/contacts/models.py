from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel

class Contact(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country_code = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    contact_picture = models.URLField(null=True)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Favourite(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, related_name='favourites', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.contact.full_name()) 