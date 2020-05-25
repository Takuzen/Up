from django.db import models
from users.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='images/user_profile_images')

    def __str__(self):
        return f'{self.user.username} Profile'