# Generated by Django 5.0.6 on 2024-05-30 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
