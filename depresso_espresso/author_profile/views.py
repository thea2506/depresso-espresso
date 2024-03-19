from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from authentication.serializer import AuthorSerializer
from posts.models import Comment, LikeComment, LikePost, Post
from authentication.models import Author, Following, FollowRequest, Node
from rest_framework.decorators import api_view
from authentication.checkbasic import checkBasic
from django.core import serializers
import requests
from django.contrib.sessions.models import Session
import json
import urllib.request
from urllib.parse import unquote
from django.db.models import Q


@api_view(["GET", "PUT"])
def api_author(request, authorid):
    ''' LOCAL and REMOTE GET ://service/authors/{AUTHOR_ID}: Returns the profile information for authorid
        LOCAL PUT ://service/authors/{AUTHOR_ID}: Updates the profile information for authorid'''
    user = None
    if request.session.session_key is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user = Author.objects.get(id=uid)

    # Update user profile information
    if request.method == "PUT":
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
        return render(request, "index.html")


@api_view(['GET'])
def get_authors(request):
    ''' LOCAL and REMOTE
        Handles getting all LOCAL authors on our server with and without an optional search parameter
        GET ://service/authors/ or GET ://service/authors?page=10&size=5'''

    if request.session.session_key is not None:

        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user = Author.objects.get(id=uid)

    if request.method == "GET":

        if user.is_authenticated == False:
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
                # send get request to node to retrieve external author info
                authors = requests.get(baseUrl + 'authors', auth=(username, password))
                print(baseUrl + 'authors')
                print("BBAAASSEEEEURLLL", baseUrl, username, password, authors)
                for author in authors:
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAUTHOR", author)
                    # Check if the author already exists in our db
                    if not Author.objects.filter(url=author.url).exists():
                        # if author does not exist, create a new one
                        new_author = Author.objects.create()
                        if not new_author:
                            return JsonResponse({"message": "Error creating new author"})
                        new_author.host = author.host
                        new_author.displayName = author.displayName
                        new_author.url = author.url
                        new_author.username = author.username
                        new_author.isExternalAuthor = True

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

        res = serializers.serialize("json", items, fields=[
                                    "profileImage", "username", "github", "displayName", "url"])
        return HttpResponse(res, content_type="application/json")


@api_view(['GET'])
def get_followers(request, authorid):
    ''' LOCAL and REMOTE   
        GET ://service/authors/{AUTHOR_ID}/followers: Get all followers of an author'''
    if request.method == "GET":
        if not Author.objects.filter(id=authorid).exists():
            return JsonResponse({"message": "Author not found"}, status=404)

        followers = Following.objects.filter(followingid=authorid)
        items = []
        data = {}

        for follower in followers:
            user = Author.objects.get(id=follower.authorid)
            items.append({
                "type": user.type,
                "id": user.id,
                "url": user.url,
                "host": user.host,
                "displayName": user.displayName,
                "username": user.username,
                "github": user.github,
                "profileImage": user.profileImage
            })

            data = {"type": "followers", "items": items}

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


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


@api_view(['POST'])
def create_follow_request(request, foreignid):
    '''LOCAL + REMOTE'''

    if request.method == 'POST':
        author = request.data["actor"]
        foreign_author = request.data["object"]

        # follow logic
        if Following.objects.filter(authorid=author["id"], followingid=foreignid).exists():
            message = "You are already following this author"
            return JsonResponse({"message": message, "success": False}, status=405)

        elif FollowRequest.objects.filter(requester=author["id"], receiver=foreignid).exists():
            message = author["displayName"], "has already sent a follow request to", foreign_author["displayName"]
            return JsonResponse({"message": message, "success": False}, status=405)

        elif not FollowRequest.objects.filter(requester=author["id"], receiver=foreignid).exists():
            FollowRequest.objects.create(
                requester=author["id"], receiver=foreignid)
            message = author["displayName"], "has successfully sent a follow request to", foreign_author["displayName"]
            return JsonResponse({"message": message, "success": True})


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

            res = serializers.serialize("json", requesters, fields=[
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
    data = {"type": "followers"}
    follower_list = []

    if request.method == "GET":
        if not Author.objects.filter(id=authorid).exists():
            return JsonResponse({"message": "Author not found"}, status=404)

        followers = Following.objects.filter(followingid=authorid)

        for follower in followers:
            author = Author.objects.get(id=follower.authorid)
            follower_list.append({
                "type": author.type,
                "id": author.id,
                "url": author.url,
                "host": author.host,
                "displayName": author.displayName,
                "github": author.github,
                "profileImage": author.profileImage
            })
        data["items"] = follower_list
        return JsonResponse(data)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def api_get_likes(request, authorid, postid):
    if request.method != "GET":
        return HttpResponse(status=405)
    if not Author.objects.filter(id=authorid).exists():
        return HttpResponse(status=404)
    if not Post.objects.filter(id=postid).exists():
        return HttpResponse(status=404)
    post = Post.objects.get(id=postid, author=Author.objects.get(id=authorid))
    likes = LikePost.objects.filter(Q(post=post), ~Q(
        author=Author.objects.get(id=authorid)))
    data = []
    for like in likes:
        item = {
            "summary": f"{like.author.displayName} liked your post",
            "type": "Like",
            "author": {
                "type": "author",
                "id": like.author.url,
                "host": like.author.host,
                "displayName": like.author.displayName,
                "url": like.author.url,
                "github": like.author.github,
                "profileImage": like.author.profileImage
            },
            "object": like.post.source
        }
        data.append(item)
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
    comment = Comment.objects.get(id=commentid, postid=Post.objects.get(
        id=postid, author=Author.objects.get(id=authorid)))
    likes = LikeComment.objects.filter(
        Q(comment=comment), ~Q(author=Author.objects.get(id=authorid)))
    data = []
    for like in likes:
        item = {
            "summary": f"{like.author.displayName} liked your comment",
            "type": "Like",
            "author": {
                "type": "author",
                "id": like.author.url,
                "host": like.author.host,
                "displayName": like.author.displayName,
                "url": like.author.url,
                "github": like.author.github,
                "profileImage": like.author.profileImage
            },
            "object": comment.comment
        }
        data.append(item)
    return JsonResponse(data, safe=False, status=200)


def api_get_author_liked(request, authorid):
    if request.method != "GET":
        return HttpResponse(status=405)
    if not Author.objects.filter(id=authorid).exists():
        return HttpResponse(status=404)
    author = Author.objects.get(id=authorid)
    liked_posts = LikePost.objects.filter(author=author)
    liked_comments = LikeComment.objects.filter(author=author)
    data = []
    for like in liked_posts:
        item = {
            "summary": f"{like.author.displayName} liked your post",
            "type": "like_post",
            "author": {
                "type": "author",
                "id": like.author.url,
                "host": like.author.host,
                "displayName": like.author.displayName,
                "url": like.author.url,
                "github": like.author.github,
                "profileImage": like.author.profileImage
            },
            "object": like.post.source
        }
        data.append(item)
    for like in liked_comments:
        item = {
            "summary": f"{like.author.displayName} liked your comment",
            "type": "like_comment",
            "author": {
                "type": "author",
                "id": like.author.url,
                "host": like.author.host,
                "displayName": like.author.displayName,
                "url": like.author.url,
                "github": like.author.github,
                "profileImage": like.author.profileImage
            },
            "object": like.comment.postid.origin + "/comments/" + str(like.comment.id)
        }
        data.append(item)
    return JsonResponse({"type": "liked", "items": data}, safe=False, status=200)
