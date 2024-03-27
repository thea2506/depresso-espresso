# https://uofa-cmput404.github.io/labsignments/heroku.html#serializing-and-deserializing-queries-optional-but-highly-recommended-to-do
from rest_framework import serializers
from rest_framework.serializers import *

from utils import *
from .models import *

from requests.auth import HTTPBasicAuth
import requests
from depresso_espresso.constants import *


class AuthorSerializer(serializers.ModelSerializer):
    # host = SerializerMethodField("get_host_url")
    id = SerializerMethodField("get_id_url")
    # url = SerializerMethodField("get_id_url")

    class Meta:
        model = Author
        fields = ("type", "id", "displayName", "github",
                  "host", "profileImage", "url")

    def get_host_url(self, _):
        return f"{self.context['request'].build_absolute_uri('/')}"

    def get_id_url(self, obj):
        return build_default_author_uri(obj=obj, request=self.context["request"], source="author")

    def update(self, instance, validated_data):
        instance.displayName = validated_data.get(
            'displayName', instance.displayName)
        instance.github = validated_data.get(
            'github', instance.github)
        instance.profileImage = validated_data.get(
            'profileImage', instance.profileImage)
        instance.save()
        return instance


class FollowRequestSerializer(serializers.ModelSerializer):
    actor = SerializerMethodField("get_actor")
    object = SerializerMethodField("get_object")
    type = SerializerMethodField("get_type")
    summary = SerializerMethodField("get_summary")

    class Meta:
        model = FollowRequest
        fields = ("type", "actor", "object", "summary")

    def get_actor(self, obj):
        actor_obj = Author.objects.get(id=obj.requester.id)
        if actor_obj.isExternalAuthor:
            node_obj = Node.objects.get(
                baseUrl=actor_obj.host.rstrip("/") + "/")
            auth = HTTPBasicAuth(node_obj.ourUsername,
                                 node_obj.ourPassword)
            response = requests.get(actor_obj.url.rstrip("/") + "/", auth=auth)
            print(">>>>>", response.text, response.status_code, response.reason)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Could not retrieve external author"}

        else:
            serializer = AuthorSerializer(
                instance=actor_obj, context=self.context)
            return serializer.data

    def get_object(self, obj):
        return AuthorSerializer(obj.receiver, context=self.context).data

    def get_type(self, _):
        return "Follow"

    def get_summary(self, obj):
        return f"{obj.requester.displayName} wants to follow {obj.receiver.displayName}"
