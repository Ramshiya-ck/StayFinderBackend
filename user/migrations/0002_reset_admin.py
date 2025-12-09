from django.db import migrations

def delete_old_admins(apps, schema_editor):
    User = apps.get_model('user', 'User')
    User.objects.filter(is_superuser=True).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(delete_old_admins),
    ]
