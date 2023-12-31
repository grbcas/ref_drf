# Generated by Django 5.0 on 2023-12-12 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_alien_invite_key_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='alien_invite_key',
            new_name='related_user',
        ),
        migrations.AddField(
            model_name='user',
            name='invite_key',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True, verbose_name='Invite_key'),
        ),
    ]
