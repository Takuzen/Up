from django.test import TestCase

# Create your tests here.
class EqualTests(TestCase):

    def test_1_equals_1(self):
        self.assertIs(1, 1)

    def test_1_equals_to_0(self):
        self.assertIs(1, 0)
