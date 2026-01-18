from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchantsubscription',
            name='plan',
        ),
        migrations.AddField(
            model_name='merchantsubscription',
            name='plan',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='merchantsubscription',
            name='plan_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='merchantsubscription',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='merchantsubscription',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
