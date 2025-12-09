from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin(apps, schema_editor):
    User = apps.get_model('user', 'User')
    if not User.objects.filter(email="admin@gmail.com").exists():
        User.objects.create(
            email="admin@gmail.com",
            password=make_password("Admin@123"),
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_admin=True
        )

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_reset_admin'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
