# Generated by Django 2.0.4 on 2018-04-25 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instrumentation', '0005_schemaattributemodel_data_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.TextField(blank=True, default=None, max_length=5000, null=True, verbose_name='Source')),
            ],
            options={
                'verbose_name': 'Operation',
            },
        ),
        migrations.CreateModel(
            name='ParameterModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_type', models.CharField(choices=[('date', 'Date'), ('number', 'Number'), ('text', 'Text')], default='text', max_length=20, verbose_name='Representation type')),
                ('representation_precision', models.IntegerField(default=3, verbose_name='Representation precision')),
                ('distinguished_name', models.CharField(max_length=100, verbose_name='Distinguished name')),
                ('display_name', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Display name')),
                ('description', models.TextField(blank=True, default=None, max_length=5000, null=True, verbose_name='Description')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instrumentation.OperationModel', verbose_name='Operation')),
            ],
            options={
                'verbose_name': 'Parameter',
            },
        ),
    ]
