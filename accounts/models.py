from django.db import models
from django.contrib.auth.models import User
import uuid
from cart.models import Listing

import random
import string

def generate_custom_id():
    while True:
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if not AgentCode.objects.filter(id=new_id).exists():
            return new_id


class AgentCode(models.Model):
    id = models.CharField(
    max_length=10, 
    primary_key=True, 
    unique=True, 
    default=generate_custom_id
)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)  # Ensures unique codes
    approved = models.BooleanField(default=False)
