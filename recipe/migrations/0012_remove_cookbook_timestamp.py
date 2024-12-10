
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_alter_account_email_alter_account_first_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cookbook',
            name='timestamp',
        ),
    ]
