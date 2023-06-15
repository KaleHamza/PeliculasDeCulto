# Generated by Django 4.2.2 on 2023-06-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('slug', models.SlugField(default='', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PeliculasDeCulto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('imageUrl', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('isActive', models.BooleanField(default=False)),
                ('isHome', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, default='', unique=True)),
                ('categories', models.ManyToManyField(to='PeliculasDeCulto.category')),
            ],
        ),
    ]
