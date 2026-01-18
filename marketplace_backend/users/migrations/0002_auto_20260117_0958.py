from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_initial_admin(apps, schema_editor):
    User = apps.get_model('users', 'User')
    if not User.objects.filter(email="Aymannk331@gmail.com").exists():
        User.objects.create(
            email="Aymannk331@gmail.com",
            password=make_password("admin1234"),
            role="ADMIN",
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_admin),
    ]
