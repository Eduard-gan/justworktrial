from django.db import migrations
from justworktrial.settings import ADMIN_USERNAME, ADMIN_PASSWORD
from django.contrib.auth.models import User


class Migration(migrations.Migration):

    def create_superuser(apps, schema_editor):
        superuser = User.objects.create_superuser(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, email=None)
        superuser.save()

    operations = [
        migrations.RunPython(create_superuser),
    ]
