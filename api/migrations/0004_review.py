# Generated by Django 4.1.1 on 2022-09-23 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_additionalinfo_movie_additional_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='')),
                ('stars', models.IntegerField(default=3)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='api.movie')),
            ],
        ),
    ]
