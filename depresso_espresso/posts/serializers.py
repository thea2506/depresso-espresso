from rest_framework import serializers
from rest_framework.serializers import *

from authentication.serializer import AuthorSerializer
from utils import *
from posts.models import *


class PostSerializer(serializers.ModelSerializer):
    id = SerializerMethodField("get_id_url")
    author = AuthorSerializer(many=False, read_only=True)
    origin = SerializerMethodField("get_origin_url")
    source = SerializerMethodField("get_source_url")
    type = SerializerMethodField("get_type")
    comments = SerializerMethodField("get_comments")
    count = SerializerMethodField("get_count")
    like_count = SerializerMethodField("get_like_count")

    class Meta:
        model = Post
        fields = ("type", "id", "author", "content", "contentType", "description", "title", "source",
                  "origin", "published", "visibility", "count", "comments", "like_count")

    def get_id_url(self, obj):
        return build_default_post_uri(obj=obj, request=self.context["request"])

    def get_comments(self, obj):
        return build_default_comments_uri(obj=obj, request=self.context["request"])

    def get_count(self, obj):
        return Comment.objects.filter(post__id=obj.id).count()

    def get_origin_url(self, obj):
        return obj.origin if obj.origin else build_default_post_uri(obj=obj, request=self.context["request"])

    def get_type(self, _):
        return "post"

    def get_source_url(self, obj):
        return obj.source if obj.source else build_default_post_uri(obj=obj, request=self.context["request"])

    def get_like_count(self, obj):
        return Like.objects.filter(post=obj).count()


class CommentSerializer(serializers.ModelSerializer):
    id = SerializerMethodField("get_id_url")
    author = AuthorSerializer(many=False, read_only=True)
    like_count = SerializerMethodField("get_like_count")

    class Meta:
        model = Comment
        fields = ("type", "id", "author", "comment",
                  "contentType", "published", "like_count")

    def get_id_url(self, obj):
        return build_default_comment_uri(obj=obj, request=self.context["request"])

    def get_like_count(self, obj):
        return Like.objects.filter(comment=obj).count()


class LikeSerializer(serializers.ModelSerializer):
    object = SerializerMethodField("get_object_url")
    summary = SerializerMethodField("get_summary")
    type = SerializerMethodField("get_type")

    class Meta:
        model = Like
        fields = ("summary", "type", "author", "object")

    def to_representation(self, instance):
        return customize_like_representation(self, instance)

    def get_object_url(self, obj):
        if obj.comment:
            return build_default_comment_uri(obj=obj.comment, request=self.context["request"])
        elif obj.post:
            return build_default_post_uri(obj=obj.post, request=self.context["request"])

    def get_summary(self, obj):
        if obj.comment:
            return f"{obj.author['displayName']} likes your comment"
        elif obj.post:
            return f"{obj.author['displayName']} likes your post"

    def get_type(self, _):
        return "Like"
