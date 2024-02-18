# https://uofa-cmput404.github.io/labsignments/heroku.html#serializing-and-deserializing-queries-optional-but-highly-recommended-to-do
from rest_framework import serializers
from .models import *

class AuthorSerializer(serializers.Serializer):
    github_link = serializers.URLField()
    profile_image = serializers.URLField()
    follows = serializers.CharField() # This may be the incorrect field type for a many to many field
    friends = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Register` instance, given the validated data
        """
        return Author.object.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Register` instance, given the validated data
        """
        instance.github_link = validated_data.get('github_link', instance.github_link)
        instance.profile_image = validated_data.get('profile_image', instance.pub_date)
        instance.save()
        return instance