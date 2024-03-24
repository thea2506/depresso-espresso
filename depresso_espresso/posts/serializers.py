from rest_framework import serializers
from rest_framework.serializers import *

from authentication.serializer import AuthorSerializer
from utils import *
from posts.models import *


class AuthorField(serializers.RelatedField):
    def get_queryset(self):
        return Author.objects.all()

    def to_internal_value(self, data):
        url_id = data.get("id").split("/")[-1]
        data["id"] = url_id
        return self.get_queryset().get(**data)

    def to_representation(self, value):
        return AuthorSerializer(value, context=self.context).data


class PostSerializer(serializers.ModelSerializer):
    id = SerializerMethodField("get_id_url")
    author = AuthorField()
    origin = SerializerMethodField("get_origin_url")
    source = SerializerMethodField("get_source_url")
    type = SerializerMethodField("get_type")
    comments = SerializerMethodField("get_comments")
    count = SerializerMethodField("get_count")
    like_count = SerializerMethodField("get_like_count")
    contentType = serializers.CharField(source="contenttype")

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
        return LikePost.objects.filter(post=obj).count()

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    id = SerializerMethodField("get_id_url")
    author = AuthorSerializer(many=False, read_only=True)
    contentType = SerializerMethodField("get_content_type")

    class Meta:
        model = Comment
        fields = ("type", "id", "author", "comment",
                  "contentType", "published", "likecount")

    def get_id_url(self, obj):
        return build_default_comment_uri(obj=obj, request=self.context["request"])

    def get_like_count(self, obj):
        return LikeComment.objects.filter(comment=obj).count()

    def get_content_type(self, obj):
        return obj.contenttype
