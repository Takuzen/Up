from django.db import models

# Create your models here.
from ..users.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',
                              upload_to='images/user_profile_images')

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        context_data.update({'form': PostForm})
        context_data["show_profile_icon"] = False
        context_data["show_left"] = True
        context_data["show_right"] = True
