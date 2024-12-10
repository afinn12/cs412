from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_account_dbrecipe_friend_image_likes_userrecipe_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Likes',
            new_name='Like',
        ),
    ]
