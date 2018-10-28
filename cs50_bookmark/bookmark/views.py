from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from bookmark.models import Bookmark, Comment

from django.contrib.auth.models import User

import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin


class Object(CsrfExemptMixin, APIView):
    authentication_classes = []

    def post(self, request, format=None):
        return Response({'received data': request.data})
# views.py


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>it is now %s. </body></html>" % now
    return HttpResponse(html)

def hello(request, user_name):
    html = "<html><body>Hello %s. </body></html>" % user_name
    return HttpResponse(html)

def new_time(request):
    sequence = list("Hello yonggeol. I'm tired")
    return render(request,"hello.html")

def index(request):
    try:
        email = request.session["username"]
    except KeyError:
        email = None
    return render(request,"index.html",{"email":email})

def test_index(request):
    return render(request, "test_index.html")


def bookmark_list(request):
    if request.method == "GET":
        all_bookmark = Bookmark.objects.all()
        email = request.session['username']
        print(all_bookmark)

        result = {"login_id": email,
                  "all_bookmark": all_bookmark
                  }

        return render(request, 'bookmark_list.html', result)

def bookmark_detail(request, id):

    bookmark = Bookmark.objects.get(bookmark_id=id)
    email = request.session["login_id"]
    user = User.objects.get(username=email)
    comments = Comment.objects.filter(bookmark=bookmark)
    return render(request, 'bookmark_detail.html', {'bookmark': bookmark, 'comments': comments})

def bookmark(request):

    print('hello')
    all_bookmark = None
    if request.method == "POST":
        bookmark = Bookmark(bookmark_name=request.POST["bookmark_name"], bookmark_url=request.POST["bookmark_url"],created_time = datetime.datetime.now(),
                            bookmark_desc = request.POST["bookmark_desc"])

        # db에 저장
        bookmark.save()

        # db에 있는 모든 값 불러옴
        all_bookmark = Bookmark.objects.all()

        try:
            email = request.session["username"]
        except KeyError:
            email= None

        result = {
            "email":email,
            # "all_bookmark": all_bookmark,
            "bookmark_name": request.POST["bookmark_name"],
            "bookmark_url": request.POST["bookmark_url"]
        }
        return render(request,  "bookmark.html", result)

    if request.method == 'GET':
        email = request.session["email"]

        if email == None:
            return render(request,'login_form.html')

        try:
            email = request.session["email"]
        except KeyError:
            email= None

        all_bookmark = Bookmark.objects.all()
        print(all_bookmark.values())
        result = {"email":email, "all_bookmark" : all_bookmark}
        return render(request, "bookmark.html", result)

def login(request):

    try:
        email = request.session["username"]
    except KeyError:
        email = None

    return render(request,'login_form.html',{'email':email})

def login_check(request):
    if request.method == "POST":
        email = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username = email)
            print(password)
            print(user)

            if user.check_password(password):
                request.session['email'] = email
                return render(request,'index.html',{'email':email})

            else:
                status = '비밀번호가 틀렸습니다.'
                request.session["username"] = email
                return render(request, 'login_form.html',{'status':status})

        except User.DoesNotExist:
            status = '존재하지 않는 아이디 입니다.'
            return render(request,'login_form.html',{'status':status})

    return render(request, 'index.html',{'email':email})

def logout(request):
    email = request.session["username"]
    return render(request,'logout_form.html',{'email':email})

def logout_process(request):
    request.session['username'] = None
    return render(request,'index.html')

def user_registeration(request):
    email = request.POST["email"]

    try:
        user = User.objects.get( username = email )
        status = "이미 저장된 아이디입니다."
        return render(request,'login_form.html',{'status':status})

    except User.DoesNotExist:
        registeration = {'registeration':1}
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["passwd"]

        user = User.objects.create_user(email,email,password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        request.session["login_id"] = email
        return render(request, 'index.html',registeration)


def post_comment(request):


    bookmark_id = request.POST['bookmark_id']
    comment_contents = request.POST['comment']

    bookmark = Bookmark.objects.get(bookmark_id=bookmark_id)
    email = request.session["login_id"]
    user = User.objects.get(username=email)

    comment = Comment(comment_contents=comment_contents,bookmark=bookmark,
            user=user)

    comment.save()
    comments = Comment.objects.filter(bookmark=bookmark)

    return redirect('bookmark_detail/' + bookmark_id)