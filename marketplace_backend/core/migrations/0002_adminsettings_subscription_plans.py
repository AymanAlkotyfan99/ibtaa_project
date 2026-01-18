# Generated migration for subscription_plans field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminsettings',
            name='subscription_plans',
            field=models.TextField(
                default='[{"name":"Basic","price":9.99,"duration_days":30,"max_products":10,"description":"Perfect for starters"},{"name":"Pro","price":29.99,"duration_days":30,"max_products":50,"description":"For growing businesses"},{"name":"Enterprise","price":99.99,"duration_days":30,"max_products":1000,"description":"For large scale operations"}]',
                help_text='JSON array of subscription plans'
            ),
        ),
    ]
