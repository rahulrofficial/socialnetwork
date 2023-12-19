from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.views.generic import ListView
import json
from .models import User,Posts
import datetime

class ContactListView(ListView):
    paginate_by = 2
    model = Posts


def index(request):
    
    return render(request, "network/index.html")




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def compose(request,item):

    # Composing a new msg must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
        
    data = json.loads(request.body) 
    if item=='post':   

    
        content = data.get("content", "")
    
        post = Posts(            
                owner=request.user,            
                content=content,
                timestamp=datetime.datetime.now()
                        
            )
        post.save()
        

        return JsonResponse({"message": "Post submitted successfully."}, status=201)
   
    elif item=='edit':
        content = data.get("content", "")
        id=int(data.get("id", ""))
        try:
            post = Posts.objects.get(pk=id)
        except Posts.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        if not post.owner==request.user:
            return JsonResponse({"error": "Unauthorized edit"}, status=404)

        post.content=content
        post.save()

        return JsonResponse({"message": "Post edited successfully."}, status=201)


@csrf_exempt
@login_required
def post(request, post_id):

    # Query for requested post
    
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether post get liked
    elif request.method == "PUT":
        if request.user not in post.liker.all():
            post.likes+=1
            post.liker.add(request.user)

        
            post.save()
            return HttpResponse(status=201)
        else:
            post.likes-=1
            post.liker.remove(request.user)

        
            post.save()
            return HttpResponse(status=201)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt

def postbox(request,**postbox):
    
    if postbox['postbox']=='all':
        posts=Posts.objects.all()
    elif postbox['postbox']=='following':
        
        user=User.objects.get(username=request.user)
        
        posts=Posts.objects.filter(owner__in=user.following.all())
    elif postbox['postbox']=='profile':
        user=postbox['user']
        user=User.objects.get(username=user)
        
        posts=Posts.objects.filter(owner=user)

    else:
        return JsonResponse({"error": "Invalid Post Request."}, status=400)
    
    page=postbox['page']
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    if paginator.num_pages<page:
        return JsonResponse({'error':'invalid Page'},status=404)
    page_obj = paginator.get_page(page)
    previous=None
    next=None
    if page_obj.has_previous():
        previous=page_obj.previous_page_number()
    if page_obj.has_next():
        next=page_obj.next_page_number()
    
    
    return JsonResponse({'posts':[post.serialize() for post in page_obj],
                         'is_signin':isinstance(request.user,User),'username':request.user.username,
                         'has_previous':page_obj.has_previous(),'has_next':page_obj.has_next(),
                         'page_num':page_obj.number,'previous_page_no':previous,
                         'next_page_number':next,'total_pages':paginator.num_pages}, safe=False)

@csrf_exempt
def profile(request,id):
    try:
        user=User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("follow") is not None:

            try:
                follower=User.objects.get(username=request.user)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found."}, status=404)
            if data['follow']:

                follower.following.add(user)
                return JsonResponse({"Success": "followed successfully."}, status=204)
            else:
                follower.following.remove(user)
                return JsonResponse({"Success": "unfollowed successfully."}, status=204)



    
    is_follower=request.user in user.followers.all()
    
    is_owner=True
    if isinstance(request.user,User):
        is_owner=user==request.user

    
    return JsonResponse({'user':user.serialize(),
                         'followers':user.followers.count(),'following':user.following.count(),
                                                   "is_owner":is_owner,'is_follower':is_follower}, safe=False)


    



def paginator(request,page):
    objects = Posts.objects.all()
    
    paginator = Paginator(objects, 10)
    if paginator.num_pages<page:
        return JsonResponse({'error':'invalid Page'},status=404)
    page_obj = paginator.get_page(page)
    previous=None
    next=None
    if page_obj.has_previous():
        previous=page_obj.previous_page_number()
    if page_obj.has_next():
        next=page_obj.next_page_number()
    
    return JsonResponse({'has_previous':page_obj.has_previous(),'has_next':page_obj.has_next(),
                         'page_num':page_obj.number,'previous_page_no':previous,
                         'next_page_number':next,'total_pages':paginator.num_pages}, safe=False)