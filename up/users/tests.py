from django.test import TestCase
from .models import User, FriendShip

# Create your tests here.
class ModelObjectTest(TestCase):

    def test_able_to_create_user_object(self):
        User.objects.create(username="randomusername", email="example@gmail.com", bio="great bio")
        object_len = len(User.objects.all())
        self.assertIs(1, object_len)


    def test_able_to_create_friendship_object(self):
        followee_user = User.objects.create(username="randomuser1", email="example1@gmail.com", bio="great bio")
        follower_user = User.objects.create(username="randomuser2", email="example2@gmail.com", bio="great bio")
        FriendShip.objects.create(follower=follower_user, followee=followee_user)
        friendship_len = len(FriendShip.objects.all())
        self.assertIs(1, friendship_len)
