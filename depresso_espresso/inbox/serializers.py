from rest_framework import serializers

from .models import NotificationItem, Notification
from posts.serializers import *
from authentication.serializer import *


class NotificationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationItem
        fields = '__all__'

    def to_representation(self, obj):

        if isinstance(obj.content_object, Post):
            return PostSerializer(instance=obj.content_object, context=self.context).data
        elif isinstance(obj.content_object, Comment):
            return CommentSerializer(instance=obj.content_object, context=self.context).data
        elif isinstance(obj.content_object, Like):
            return LikeSerializer(instance=obj.content_object, context=self.context).data
        elif obj.json_data is not None:
            return obj.json_data
        elif isinstance(obj.content_object, Follow):
            return FollowSerializer(instance=obj.content_object, context=self.context).data


class NotificationSerializer(serializers.ModelSerializer):
    author = SerializerMethodField("get_author_url")
    items = SerializerMethodField("get_items")
    type = SerializerMethodField("get_type")

    class Meta:
        model = Notification
        fields = ("type", "author", "items")

    def get_author_url(self, obj):
        return build_default_author_uri(obj=obj, request=self.context["request"], source="inbox")

    def get_items(self, obj):
        return NotificationItemSerializer(obj.items.all().order_by("-id"), many=True, context=self.context).data

    def get_type(self, _):
        return "inbox"
