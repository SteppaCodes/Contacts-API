from django.db import models

from apps.accounts.models import User
from apps.contacts.models import Contact
from apps.common.models import BaseModel

class Favourite(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, related_name='favourites', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.contact.full_name()) 
