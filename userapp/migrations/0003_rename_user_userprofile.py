# Generated by Django 4.0.4 on 2022-06-09 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('vote', '0001_initial'),
        ('question', '0004_rename_username_answer_user_and_more'),
        ('userapp', '0002_rename_userprofile_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserProfile',
        ),
    ]
