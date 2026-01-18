from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('digital', 'Digital Asset'), ('physical', 'Physical Product'), ('service', 'Service'), ('other', 'Other')], default='other', max_length=20),
        ),
    ]
