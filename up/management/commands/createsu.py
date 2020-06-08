from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
	def handle(self, *args, **options):
		if not User.objects.filter(username="tkz").exists():
			User.objects.create_superuser(username="tkz", email="takuzen0430@gmail.com", password="19960430")
			self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
		if not User.objects.filter(username="ReishiMitani").exists():
			User.objects.create_superuser(username="ReishiMitani", email="reishim0731@gmail.com", password="xihu@npiNgguo")
			self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
