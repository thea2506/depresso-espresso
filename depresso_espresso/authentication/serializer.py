# https://uofa-cmput404.github.io/labsignments/heroku.html#serializing-and-deserializing-queries-optional-but-highly-recommended-to-do
from rest_framework import serializers
from rest_framework.serializers import *

from utils import *
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    host = SerializerMethodField("get_host_url")
    id = SerializerMethodField("get_id_url")
    url = SerializerMethodField("get_id_url")

    class Meta:
        model = Author
        fields = ("type", "id", "displayName", "github",
                  "host", "profileImage", "url")

    def get_host_url(self, _):
        return f"{self.context['request'].build_absolute_uri('/')}"

    def get_id_url(self, obj):
        return build_default_author_uri(obj=obj, request=self.context["request"], source="author")


class FollowSerializer(serializers.ModelSerializer):
    actor = serializers.JSONField()
    object = SerializerMethodField("get_object")
    summary = SerializerMethodField("get_summary")
    type = SerializerMethodField("get_type")

    class Meta:
        model = Follow
        fields = ("type", "summary", "actor", "object")

    def get_object(self, obj):
        return AuthorSerializer(obj.object, context=self.context).data

    def get_summary(self, obj):
        actor_display_name = obj.actor["displayName"]
        return f"{actor_display_name} wants to follow {obj.object.displayName}"

    def get_type(self, _):
        return "Follow"


class FollowerSerializer(serializers.ModelSerializer):
    author = serializers.JSONField()

    class Meta:
        model = Follower
        fields = ("type", "actor", "object")

    def get_object(self, obj):
        return AuthorSerializer(obj.author, context=self.context).data
