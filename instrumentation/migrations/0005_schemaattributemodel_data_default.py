# Generated by Django 2.0.4 on 2018-04-25 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrumentation', '0004_equipmentmodel_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='schemaattributemodel',
            name='data_default',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Default value'),
        ),
    ]
