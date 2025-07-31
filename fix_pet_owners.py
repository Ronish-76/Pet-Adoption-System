import random
from pets.models import Pet
from django.contrib.auth.models import User

users = list(User.objects.all())
if not users:
    print('No users found. Cannot assign owners.')
else:
    pets = Pet.objects.all()
    for pet in pets:
        if not pet.owner_id or pet.owner_id not in [u.id for u in users]:
            pet.owner = random.choice(users)
            pet.save()
    print('Pet owners fixed.')