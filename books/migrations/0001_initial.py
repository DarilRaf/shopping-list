# Generated by Django 4.2.5 on 2023-11-25 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('author', models.TextField(blank=True, null=True)),
                ('genre', models.TextField(blank=True, null=True)),
                ('pages', models.IntegerField(blank=True, null=True)),
                ('published_year', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('thumbnail', models.TextField(blank=True, null=True)),
                ('ratings_avg', models.FloatField(blank=True, null=True)),
                ('ratings_count', models.IntegerField(blank=True, null=True)),
                ('isbn10', models.TextField(blank=True, null=True)),
                ('isbn13', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
