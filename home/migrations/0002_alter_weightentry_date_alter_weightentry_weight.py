# Generated by Django 5.0.6 on 2024-07-31 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weightentry',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='weightentry',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
