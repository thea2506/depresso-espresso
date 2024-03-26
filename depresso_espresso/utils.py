from depresso_espresso.constants import *
from rest_framework import serializers


def build_default_author_uri(obj, request, source):
    uri = request.build_absolute_uri("/")
    author_id = obj.id if source == "author" else obj.author.id

    return f"{uri}{SERVICE}authors/{author_id}"


def build_default_post_uri(obj, request):
    uri = request.build_absolute_uri("/")
    return f"{uri}{SERVICE}authors/{obj.author.id}/posts/{obj.id}"


def build_default_comment_uri(obj, request):
    uri = request.build_absolute_uri("/")

    return f"{uri}{SERVICE}authors/{obj.post.author.id}/posts/{obj.post.id}/comments/{obj.id}"


def build_default_comments_uri(obj, request):
    uri = request.build_absolute_uri("/")

    return f"{uri}{SERVICE}authors/{obj.author.id}/posts/{obj.id}/comments"


def customize_like_representation(serializer_instance, instance):
    representation = serializers.ModelSerializer.to_representation(
        serializer_instance, instance)

    return representation