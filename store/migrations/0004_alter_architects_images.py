# Generated by Django 3.2.14 on 2022-12-02 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_architects_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='architects',
            name='images',
            field=models.ImageField(upload_to=''),
        ),
    ]