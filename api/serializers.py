from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Movie, AdditionalInfo, Review, Actor


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'password']
        extra_kwargs = {
            'password': {
                'required': True,
                'write_only': True,

            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ['duration', 'genre']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # depth = 1
        # read_only_fields = ('movie', )

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.stars = validated_data.get('stars', instance.stars)
        instance.save()

        return instance


class MovieSerializer(serializers.ModelSerializer):
    additional_info = AdditionalInfoSerializer(many=False)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['title', 'year', 'released', 'premiere', 'description', 'imdb_rating', 'additional_info', 'reviews']
        read_only_fields = ('additional_info', 'reviews')


class MovieMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'year', 'released', 'premiere', 'description', 'imdb_rating']


class ActorSerializer(serializers.ModelSerializer):
    movies = MovieMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ['id', 'name', 'lastname', 'movies']

    # def create(self, validated_data):
    #     movies = validated_data.get('movies')
    #     del validated_data['movies']
    #
    #     actor = Actor.objects.create(**validated_data)
    #
    #     for m in movies:
    #         movie = Movie.objects.create(**m)
    #         actor.movies.add(movie)
    #
    #     actor.save()
    #
    #     return actor
