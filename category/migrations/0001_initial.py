# Generated by Django 3.1 on 2022-06-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200, unique=True)),
                ('category_img', models.ImageField(blank=True, upload_to='photos/categories')),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
    ]
