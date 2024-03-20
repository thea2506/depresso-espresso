from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from authentication.serializer import AuthorSerializer
from posts.models import Comment, Post, Like
from authentication.models import Author, Following, FollowRequest, Node, Follow, Follower
from rest_framework.decorators import api_view
from authentication.checkbasic import checkBasic, my_authenticate
from django.core import serializers as serial
from django.contrib.sessions.models import Session
import json
import urllib.request
from urllib.parse import unquote
from authentication.serializer import *
from inbox.models import Notification, NotificationItem
from http.client import HTTPSConnection
from base64 import b64encode
from posts.serializers import *


@api_view(["GET", "PUT"])
def api_author(request, authorid):
    ''' LOCAL and REMOTE GET ://service/authors/{AUTHOR_ID}: Returns the profile information for authorid
        LOCAL PUT ://service/authors/{AUTHOR_ID}: Updates the profile information for authorid'''

    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    # Update user profile information
    if request.method == "PUT":
        if not isinstance(user, Author) or str(user.id) != str(authorid):
            return JsonResponse({"message": "Local Users Only"}, status=404)

        if user.is_authenticated == True:
            author = get_object_or_404(Author, pk=authorid)
            data = json.loads(request.body)
            if user == author:
                if data.get('displayName') != None:
                    author.displayName = data['displayName']
                if data.get('github') != None:
                    author.github = data['github']
                if data.get('profileImage') != None:
                    author.profileImage = data['profileImage']
                author.save()
                return JsonResponse({"message": "Profile updated successfully"})

    # Gets user profile information
    elif request.method == "GET":
        if not Author.objects.filter(id=authorid).exists():
            return JsonResponse({"message": "Author not found"}, status=404)

        author = Author.objects.get(id=authorid)

        data = AuthorSerializer(instance=author, context={
                                "request": request}).data

        return JsonResponse(data)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


@api_view(['GET'])
def get_authors(request):
    ''' LOCAL and REMOTE
        Handles getting all LOCAL authors on our server with and without an optional search parameter
        GET ://service/authors/ or GET ://service/authors?page=10&size=5'''
    user = None
    if request.session.session_key is not None:

        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user = Author.objects.get(id=uid)

    if request.method == "GET":

        if user == None:
            # This part of the function is meant to be used by remote servers only
            # handles retreiving authors for an external server (only retreive our LOCALLY CREATED authors)
            node = checkBasic(request)
            if not node:
                return JsonResponse({"message:" "External Auth Failed"}, status=401)

            # Only send the external server our locally created authors
            authors = Author.objects.filter(isExternalAuthor=False)

            items = []
            for author in authors:
                items.append({

                    "type": author.type,
                    "id": author.id,
                    "url": author.url,
                    "host": author.host,
                    "displayName": author.displayName,
                    "username": author.username,
                    "github": author.github,
                    "profileImage": author.profileImage

                })

                data = {
                    "type": "author",
                    "items": items
                }

            return JsonResponse(data, safe=False)

        else:

            # Poll all external nodes for their authors
            nodes = Node.objects.all()
            for node in nodes:
                username = node.theirUsername
                password = node.theirPassword
                baseUrl = node.baseUrl

                # Code taken from https://stackoverflow.com/a/7000784
                host = str(baseUrl).replace("https://", "")
                host = host[:-1]
                client = HTTPSConnection(host)

                headers = {"Authorization": "Basic {}".format(
                    b64encode(bytes(f"{username}:{password}", "utf-8")).decode("ascii"))}
                client.request('GET', '/authors', headers=headers)
                response = client.getresponse()
                authorsBytes = response.read()
                author_data = json.loads(authorsBytes)

                for author in author_data["items"]:
                    # Check if the author already exists in our db
                    if not Author.objects.filter(url=author["url"]).exists():
                        # if author does not exist, create a new one
                        host = author["host"]
                        displayName = author["displayName"]
                        url = author["url"]
                        username = author["username"]

                        Author.objects.create(
                            host=host, displayName=displayName, url=url, username=username, isExternalAuthor=True)

            search_terms = request.GET.get('search')

            # Get authors on our db
            if search_terms:
                authors = Author.objects.filter(
                    displayName__icontains=search_terms)
                print(authors)

            else:
                authors = Author.objects.all()

            items = []
            for author in authors:
                items.append(author)

        res = serial.serialize("json", items, fields=[
            "profileImage", "username", "github", "displayName", "url"])
        return HttpResponse(res, content_type="application/json")


@api_view(['GET', 'DELETE', 'PUT'])
def handle_follow(request, authorid, foreignid):
    ''' LOCAL AND REMOTE GET ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}: check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        LOCAL PUT ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
        LOCAL DELETE ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}: Unfollow another author'''

    if request.session.session_key is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user = Author.objects.get(id=uid)

    if Author.objects.filter(id=foreignid).exists():
        foreign_author = Author.objects.get(id=foreignid)
    else:
        response = urllib.request.urlopen(unquote(foreignid))
        if response.status != 200:
            return JsonResponse({"message": "Foreign author not found", "success": False}, status=404)
        foreign_author = json.loads(response.read())
        foreign_author = {
            "type": foreign_author["type"],
            "id": foreign_author["id"],
            "url": foreign_author["url"],
            "host": foreign_author["host"],
            "displayName": foreign_author["displayName"],
            "github": foreign_author["github"],
            "profileImage": foreign_author["profileImage"]
        }

    author = Author.objects.get(id=authorid)

    # check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
    if request.method == "GET":
        if Following.objects.filter(authorid=foreignid, followingid=authorid).exists():
            items = []

            # append our author
            items.append({
                "type": author.type,
                "id": author.id,
                "url": author.url,
                "host": author.host,
                "displayName": author.displayName,
                "github": author.github,
                "profileImage": author.profileImage
            })

            # append the foreign author
            items.append({
                "type": foreign_author.type,
                "id": foreign_author.id,
                "url": foreign_author.url,
                "host": foreign_author.host,
                "displayName": foreign_author.displayName,
                "github": foreign_author.github,
                "profileImage": foreign_author.profileImage,
            })

            data = {"type": "followers", "items": items}
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"message": "Author not found"}, status=404)

    # Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
    if request.method == "PUT":
        if user.is_authenticated == False:
            return JsonResponse({"message": "User not authenticated"}, status=401)

        # foreign author has not followed author yet
        if not Following.objects.filter(authorid=foreignid, followingid=authorid).exists():
            Following.objects.create(
                authorid=foreignid, followingid=authorid, areFriends=False)

        # LOCAL
        if Author.objects.filter(id=foreignid).exists():
            if Following.objects.filter(authorid=authorid, followingid=foreignid).exists():
                Following.objects.filter(
                    authorid=foreignid, followingid=authorid).update(areFriends=True)
                Following.objects.filter(
                    authorid=authorid, followingid=foreignid).update(areFriends=True)
                message = "Follow request from", foreign_author.id, "accepted by", author.displayName, "and they are now friends"
            else:
                message = "Follow request from", foreign_author.id, "accepted by", author.displayName

        # REMOTE
        else:
            response = urllib.request.urlopen(
                foreign_author.url + '/followers/' + authorid)
            if response.status == 200:
                Following.objects.filter(
                    authorid=foreignid, followingid=authorid).update(areFriends=True)
                message = "Follow request from a foreign", foreignid, "accepted by", author.displayName, "and they are now friends"
            else:
                message = "Follow request from a foreign", foreign_author.id, "accepted by", author.displayName
        return JsonResponse({"message": message, "success": True})

    #  remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    if request.method == "DELETE":

        if Following.objects.filter(authorid=foreignid, followingid=authorid).exists():
            message = foreign_author.displayName, "unfollowed", author.displayName

            if Following.objects.filter(authorid=authorid, followingid=foreignid).exists() and Following.objects.filter(authorid=foreignid, followingid=authorid)[0].areFriends:
                Following.objects.filter(
                    authorid=authorid, followingid=foreignid).update(areFriends=False)
                message = foreign_author.displayName, "unfollowed", author.displayName, "and they are no longer friends"

            Following.objects.filter(
                authorid=authorid, followingid=foreignid).delete()

            return JsonResponse({"message": message, "success": True})


@api_view(['GET', 'DELETE', 'PUT'])
def api_add_follower(request, authorid, foreignid):
    ''' GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
    PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
    DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    '''
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    # LOCAL
    if request.method == 'PUT':
        if not isinstance(user, Author) or str(user.id) != str(authorid):
            return JsonResponse({"message": "Local Users Only"}, status=404)

        foreign_author = request.data["actor"]
        # author = request.data["object"]
        if user.is_authenticated == False:
            return JsonResponse({"message": "User not authenticated"}, status=401)
        if str(user.id) != authorid:
            return JsonResponse({"message": "User not authorized"}, status=401)

        decision = request.data["decision"]

        if not (decision == "decline"):
            Follower.objects.create(author=Author.objects.get(
                id=authorid), follower_author=foreign_author)

        notification_object = Notification.objects.get(
            author=Author.objects.get(id=authorid))

        notification_items = NotificationItem.objects.filter(
            notification=notification_object)

        for item in notification_items:
            if str(item.content_type) == "Authentication | follow" and str(item.content_object.object.id) == authorid:
                item.delete()
                break

        follow_object = Follow.objects.filter(
            object=Author.objects.get(id=authorid))
        for follow in follow_object:
            if str(follow.actor["id"]) == unquote(foreignid):
                follow.delete()
                break
        return JsonResponse({"success": True, "decision": decision}, status=201)

    # LOCAL + REMOTE
    elif request.method == 'GET':
        author_object = Author.objects.get(id=authorid)
        followers = Follower.objects.filter(author=author_object)

        for follower in followers:
            follower_object = follower.follower_author
            if str(follower_object["id"]) == unquote(foreignid):

                return JsonResponse({
                    "type": "Follow",
                    "summary": follower_object["displayName"] + f" is following {author_object.displayName}",
                    "actor": follower_object,
                    "object": AuthorSerializer(instance=author_object, context={
                        "request": request}).data
                }, status=200)

        if Follow.objects.filter(object=author_object).exists():
            follow_object = Follow.objects.filter(object=author_object)
            for follow in follow_object:
                if follow.actor["id"] == unquote(foreignid):
                    return JsonResponse({"status": "pending"}, status=404)
            return JsonResponse({"message": "Follower does not exist", "success": False}, status=404)

        return JsonResponse({"message": "Follower does not exist", "success": False}, status=404)

    # LOCAL
    elif request.method == 'DELETE':
        if not isinstance(user, Author) or str(user.id) != str(authorid):
            return JsonResponse({"message": "Local Users Only"}, status=404)

        author_object = Author.objects.get(id=authorid)
        followers = Follower.objects.filter(author=author_object)
        for follower in followers:
            if str(follower_object["id"]) == unquote(foreignid):
                follower.delete()
                return JsonResponse({"message": "Follower removed successfully", "success": True}, status=200)
        return JsonResponse({"message": "Follower does not exist", "success": False}, status=404)


@api_view(['PUT'])
def respond_to_follow_request(request, foreignid):
    ''' LOCAL/REMOTE 
        Respond to a follow request from another author'''

    # Foreign author should exist in our database, since we created it when the follow request was sent
    foreign_author = Author.objects.get(id=foreignid)

    if request.session.session_key is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user = Author.objects.get(id=uid)

    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        if data["decision"] == "accept":
            FollowRequest.objects.filter(
                requester=foreign_author.id, receiver=user.id).delete()

            if Following.objects.filter(authorid=user.id, followingid=foreignid).exists():
                Following.objects.filter(
                    authorid=user.id, followingid=foreignid).update(areFriends=True)
                Following.objects.create(
                    authorid=foreignid, followingid=user.id, areFriends=True)
            else:
                Following.objects.create(
                    authorid=foreignid, followingid=user.id, areFriends=False)
            message = "Follow request accepted"
            # foreign_author_follow(request, authorid, foreignid)

        elif data["decision"] == "decline":
            FollowRequest.objects.filter(
                requester=foreignid, receiver=user.id).delete()
            message = "Follow request declined"
        return JsonResponse({"message": message, "success": True})

    return JsonResponse({"message": "Error responding to follow request", })


@api_view(['GET'])
def get_friends(request, authorid):
    ''' LOCAL
        Get all friends of an author'''

    if request.method == "GET":
        friends = Following.objects.filter(authorid=authorid, areFriends=True)
        data = []
        for friend in friends:
            user = Author.objects.get(id=friend.authorid)
            data.append({
                "type": user.type,
                "id": user.id,
                "url": user.url,
                "host": user.host,
                "displayName": user.displayName,
                "username": user.username,
                "github": user.github,
                "profileImage": user.profileImage
            })
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def get_follow_list(request):
    ''' LOCAL
        Get all authors that an author is following'''

    if request.method == "GET":
        following = Following.objects.filter(authorid=request.user.id)
        data = []
        for follow in following:
            user = Author.objects.get(id=follow.followingid)
            data.append({
                "type": "author",
                "id": user.id,
                "url": user.url,
                "host": user.host,
                "displayName": user.displayName,
                "username": user.username,
                "github": user.github,
                "profileImage": user.profileImage,
                "friend": follow.areFriends,
                "followedFrom": follow.created_at,
            })
        return JsonResponse({"data": data, "success": True}, safe=False)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def check_follow_status(request):
    '''Check the follow status between two authors'''

    data = request.GET
    authorid = data["id"]
    author = Author.objects.get(id=authorid)

    result = {}

    if request.method == "GET":
        # follow
        if Following.objects.filter(authorid=request.user.id, followingid=author.id).exists():
            if Following.objects.filter(authorid=request.user.id, followingid=author.id)[0].areFriends:
                result["status"] = "friend"
            else:
                result["status"] = "follower"

        # follow pending
        elif FollowRequest.objects.filter(requester=request.user.id, receiver=author.id).exists():
            result["status"] = "pending"

        # not following
        else:
            result["status"] = "stranger"
        result["success"] = True
        return JsonResponse(result)
    else:
        return JsonResponse({"success": False})


def front_end_inbox(request, authorid):
    return render(request, 'index.html')


def get_follow_requests(request):  # Can this be extended to be inbox?
    '''Get all follow requests for an author'''

    if request.method == "GET":
        authorid = request.GET.get("id")
        if authorid:
            follow_requests = FollowRequest.objects.filter(receiver=authorid)
            requesters = []
            for follow_request in follow_requests:
                # include logic here that checks if requester has an external host
                requester = Author.objects.get(id=follow_request.requester)
                requesters.append(requester)

            res = serial.serialize("json", requesters, fields=[
                "profileImage", "username", "github", "displayName", "url"])

            return HttpResponse(res, content_type="application/json")
        return JsonResponse({"message": "No new requests"})


def user_posts(request, username):
    user_posts = Post.objects.filter(authorid__username=username)
    return render(request, 'author_profile/user_posts.html', {'user_posts': user_posts})


def front_end(request, authorid):
    return render(request, 'index.html')


def get_image(request, image_file):
    return redirect(f'/images/{image_file}')


# Required API Endpoints
@api_view(['GET'])
def api_get_authors(request):
    ''' GET [local, remote]: retrieve all profiles on the server (paginated)
    '''
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    page = request.GET.get("page")
    size = request.GET.get("size")
    data = {"type": "author"}
    author_list = []

    if request.method == "GET":
        authors = Author.objects.all()
        if page and size:
            page = int(page)
            size = int(size)

            start_index = size * (page - 1)
            end_index = size * page

            if end_index > len(authors):
                end_index = len(authors)
            if start_index < 0:
                start_index = 0

            if start_index > len(authors) or end_index < 0:
                author_list = []
            else:
                authors = authors[start_index: end_index]
                for author in authors:
                    author_list.append({
                        "type": author.type,
                        "id": author.id,
                        "url": author.url,
                        "host": author.host,
                        "displayName": author.displayName,
                        "username": author.username,
                        "github": author.github,
                        "profileImage": author.profileImage
                    })
        else:
            for author in authors:
                author_list.append({
                    "type": author.type,
                    "id": author.id,
                    "url": author.url,
                    "host": author.host,
                    "displayName": author.displayName,
                    "username": author.username,
                    "github": author.github,
                    "profileImage": author.profileImage
                })
        data["items"] = author_list
        return JsonResponse(data)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@api_view(['GET'])
def api_get_followers(request, authorid):
    '''GET [local, remote]: get a list of authors who are AUTHOR_ID's followers'''

    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    data = {"type": "followers", "items": []}

    if request.method == "GET":
        if not Author.objects.filter(id=authorid).exists():
            return JsonResponse({"message": "Author not found"}, status=404)
        author_object = Author.objects.get(id=authorid)
        followers = Follower.objects.filter(author=author_object)
        for follower in followers:
            data["items"].append(follower.follower_author)
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def api_get_likes(request, authorid, postid):
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    # LOCAL + REMOTE
    if request.method != "GET":
        return HttpResponse(status=405)
    if not Author.objects.filter(id=authorid).exists():
        return HttpResponse(status=404)
    if not Post.objects.filter(id=postid).exists():
        return HttpResponse(status=404)
    author = Author.objects.get(id=authorid)
    post = Post.objects.get(id=postid, author=author)
    likes = Like.objects.filter(post=post)
    data = {"types": "Like", "items": []}
    data["items"] = LikeSerializer(instance=likes, many=True, context={
                                   "request": request}).data
    return JsonResponse(data, safe=False, status=200)


def api_get_likes_comment(request, authorid, postid, commentid):
    if request.method != "GET":
        return HttpResponse(status=405)
    if not Author.objects.filter(id=authorid).exists():
        return HttpResponse(status=404)
    if not Post.objects.filter(id=postid).exists():
        return HttpResponse(status=404)
    if not Comment.objects.filter(id=commentid).exists():
        return HttpResponse(status=404)

    author = Author.objects.get(id=authorid)
    comment = Comment.objects.get(id=commentid, post=Post.objects.get(
        id=postid, author=author))

    data = {"types": "Like", "items": []}
    data["items"] = CommentSerializer(instance=comment, context={
        "request": request}).data

    return JsonResponse(data, safe=False, status=200)


def api_get_author_liked(request, authorid):
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    if request.method != "GET":
        return HttpResponse(status=405)
    if not Author.objects.filter(id=authorid).exists():
        return HttpResponse(status=404)
    author = Author.objects.get(id=authorid)
    author_json = AuthorSerializer(instance=author, context={
                                   "request": request}).data
    print(author_json)
    liked_objects = Like.objects.filter(author__id__endswith=authorid)

    data = {"type": "liked", "items": []}

    print(liked_objects)

    data["items"] = LikeSerializer(instance=liked_objects, many=True, context={
                                   "request": request}).data

    return JsonResponse(data, safe=False, status=200)
