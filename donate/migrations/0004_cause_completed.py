# Generated by Django 3.1.7 on 2021-03-21 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0003_cause_date_needed'),
    ]

    operations = [
        migrations.AddField(
            model_name='cause',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
