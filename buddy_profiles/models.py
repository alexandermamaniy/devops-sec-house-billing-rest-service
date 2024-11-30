from django.db import models
import uuid
from users.models import User
from core.models import TimeStampedModel

def upload_to(instance, filename):
    return f'profiles/{filename}'

class BuddyProfile(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Buddy Profile')
    full_name = models.CharField('Fullname', max_length=255, blank=True, null=False)
    picture_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        verbose_name = 'Buddy Profile'
        verbose_name_plural = 'Buddy Profiles'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} - {self.user}'