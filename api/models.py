from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Movie(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(default='')
    year = models.SmallIntegerField(default=1990)
    released = models.BooleanField(default=False)
    premiere = models.DateField(null=True, blank=True)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2, default=2.22)
    additional_info = models.OneToOneField("AdditionalInfo", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.title} ({self.year})'


class AdditionalInfo(models.Model):
    duration = models.IntegerField(default=120)

    GENRE = [
        (0, 'Horror'),
        (1, 'Comedy'),
        (2, 'Action'),
        (3, 'Drama'),
        (4, 'Other'),
    ]
    genre = models.IntegerField(choices=GENRE, default=4)


class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField(default='')
    stars = models.IntegerField(default=3)


class Actor(models.Model):
    movies = models.ManyToManyField(Movie, related_name='actors')
    name = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
