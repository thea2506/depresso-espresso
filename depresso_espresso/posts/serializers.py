from rest_framework import serializers
from rest_framework.serializers import *

from authentication.serializers import AuthorSerializer
from utils import *
from posts.models import *


class AuthorField(serializers.RelatedField):
    def get_queryset(self):
        return Author.objects.all()

    def to_internal_value(self, data):
        if (self.get_queryset().filter(url=data.get("url")).exists()):
            return self.get_queryset().get(url=data.get("url"))

    def to_representation(self, value):
        return AuthorSerializer(value, context=self.context).data


class PostSerializer(serializers.ModelSerializer):
    id = SerializerMethodField("get_id_url")
    author = AuthorField()
    origin = SerializerMethodField("get_origin_url")
    source = SerializerMethodField("get_source_url")
    comments = SerializerMethodField("get_comments")
    count = SerializerMethodField("get_count")
    likecount = SerializerMethodField("get_like_count")
    contentType = serializers.CharField(source="contenttype")

    class Meta:
        model = Post
        fields = ("type", "id", "author", "content", "contentType", "description", "title", "source",
                  "origin", "published", "visibility", "count", "comments", "likecount")

    def get_id_url(self, obj):
        return build_default_post_uri(obj=obj, request=self.context["request"])

    def get_comments(self, obj):
        return build_default_comments_uri(obj=obj, request=self.context["request"])

    def get_count(self, obj):
        return Comment.objects.filter(post__id=obj.id).count()

    def get_origin_url(self, obj):
        return obj.origin if obj.origin else build_default_post_uri(obj=obj, request=self.context["request"])

    def get_source_url(self, obj):
        return obj.source if obj.source else build_default_post_uri(obj=obj, request=self.context["request"])

    def get_like_count(self, obj):
        return LikePost.objects.filter(post=obj).count()

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class PostField(serializers.RelatedField):
    def get_queryset(self):
        return Post.objects.all()

    def to_internal_value(self, data):
        url_id = data.get("id").split("/")[-1]
        return self.get_queryset().get(id=url_id)

    def to_representation(self, value):
        return AuthorSerializer(value, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    id = SerializerMethodField("get_id_url")
    author = AuthorField()
    contentType = serializers.CharField(source="contenttype")
    type = SerializerMethodField("get_type")
    likecount = SerializerMethodField("get_like_count")

    class Meta:
        model = Comment
        fields = ("type", "id", "author", "comment",
                  "contentType", "published", "likecount", "post")

    def get_id_url(self, obj):
        return build_default_comment_uri(obj=obj, request=self.context["request"])

    def get_like_count(self, obj):
        return LikeComment.objects.filter(comment=obj).count()

    def get_type(self, _):
        return "comment"

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class LikePostSerializer(serializers.ModelSerializer):
    author = AuthorField()
    object = SerializerMethodField("get_object")
    type = SerializerMethodField("get_type")
    summary = SerializerMethodField("get_summary")

    class Meta:
        model = LikePost
        fields = ("type", "author", "object", "summary")

    def get_type(self, _):
        return "Like"

    def get_object(self, obj):
        return build_default_post_uri(obj=obj.post, request=self.context["request"])

    def get_summary(self, obj):
        return f"{obj.author.displayName} liked your post"
    

class LikeCommentSerializer(serializers.ModelSerializer):
    author = AuthorField()
    object = SerializerMethodField("get_object")
    type = SerializerMethodField("get_type")
    summary = SerializerMethodField("get_summary")

    class Meta:
        model = LikePost
        fields = ("type", "author", "object", "summary")

    def get_type(self, _):
        return "Like"

    def get_object(self, obj):
        return build_default_comments_uri(obj=obj.comment, request=self.context["request"])

    def get_summary(self, obj):
        return f"{obj.author.displayName} liked your comment"
