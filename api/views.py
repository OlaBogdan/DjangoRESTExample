from django.contrib.auth.models import User
from django.http.response import HttpResponseNotAllowed
from rest_framework import viewsets, filters
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication

from api.serializers import UserSerializer, MovieSerializer, ReviewSerializer, ActorSerializer
from api.models import Movie, Review, Actor


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('title', 'year')
    search_fields = ('title', 'year')
    ordering_fields = ('title', 'year')
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        qs = Movie.objects.all()

        return qs

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = MovieSerializer(queryset, many=True)
    #
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MovieSerializer(instance)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # if request.user.is_staff:
        movie = Movie.objects.create(title=request.data.get('title', ''),
                                     year=request.data.get('year', 1990),
                                     released=request.data.get('released', False))

        serializer = MovieSerializer(movie, many=False)

        return Response(serializer.data)

        # else:
        #     return HttpResponseNotAllowed("method not allowed")

    def update(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.title = request.data.get('title', '')
        movie.year = request.data.get('year', 1990)
        movie.released = request.data.get('released', False)
        movie.save()
        serializer = MovieSerializer(movie, many=False)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.delete()

        return Response('Movie was deleted')

    @action(detail=True)
    def premiere(self, request, **kwargs):
        movie = self.get_object()
        movie.released = True
        movie.save()

        serializer = MovieSerializer(movie, many=False)

        return Response(serializer.data)

    @action(detail=False, methods=['post', ])
    def premiere_all(self, request, **kwargs):
        movies = self.get_queryset()
        movies.update(released=request.data.get('released', True))

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    @action(detail=True, methods=['post', ])
    def add_movie(self, request, **kwargs):
        actor = self.get_object()
        movie = Movie.objects.get(id=request.data.get('movie'))

        actor.movies.add(movie)
        actor.save()

        serializer = ActorSerializer(actor, many=False)

        return Response(serializer.data)
