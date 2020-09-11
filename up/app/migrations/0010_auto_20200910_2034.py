# Generated by Django 3.1 on 2020-09-10 11:34

from django.db import migrations, models
import django.db.models.deletion
import up.app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200905_2225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=up.app.models.user_portfolio_directory_path)),
                ('item', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.item')),
            ],
        ),
    ]
