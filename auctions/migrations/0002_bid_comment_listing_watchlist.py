# Generated by Django 3.1.4 on 2021-01-24 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('comment', models.TextField()),
                ('listingid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('category', models.CharField(blank=True, max_length=64)),
                ('image', models.URLField(blank=True, default=None, null=True)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
            ],
        ),
    ]
