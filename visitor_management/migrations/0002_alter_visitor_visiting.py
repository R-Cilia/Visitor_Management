# Generated by Django 3.2.9 on 2021-11-05 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='visiting',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='visitor_management.employee'),
        ),
    ]
