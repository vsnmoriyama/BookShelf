from django.shortcuts import render, redirect
import urllib.request as url_request
import json
from .models import User
# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError

clientCode = 'BookShelf'
method = "POST"
headers = {"Content-Type": "application/json"}


def topPage(request):
    return render(request, 'userManage/top.html')


def menu(request):
    try:
        authCode = request.GET['authCode']
        accessToken = authByAuthCode(authCode)
        request.session['accessToken'] = accessToken
    except MultiValueDictKeyError:
        try:
            accessToken = request.session['accessToken']
        except KeyError:
            return redirect('userManagement:top')

    authByAccessToken(request, accessToken)
    message = addOrLogin(request.session['userId'], request.session['userName'])
    userData = {'userName': request.session['userName'], 'message': message}
    return render(request, 'userManage/menu.html', userData)


def authByAuthCode(auth_code):
    urlAuthCode = 'http://localhost:8080/projectStudy/authorization/authCode/'
    obj = {'client_code': clientCode, 'auth_code': auth_code}
    json_data = json.dumps(obj).encode("utf-8")
    authRequest = url_request.Request(urlAuthCode, data=json_data, method=method, headers=headers)
    with url_request.urlopen(authRequest) as response:
        response_body = response.read().decode("utf-8")
        result_obj = json.loads(response_body.split('\n')[0])
        accessToken = result_obj['code']
    return accessToken


def authByAccessToken(request, access_token):
    urlAccessToken = 'http://localhost:8080/projectStudy/authorization/accessToken/getData/'
    obj = {'client_code': clientCode, 'accessToken': access_token}
    json_data = json.dumps(obj).encode("utf-8")
    accessTokenRequest = url_request.Request(urlAccessToken, data=json_data, method=method, headers=headers)
    with url_request.urlopen(accessTokenRequest) as response:
        response_body = response.read().decode("utf-8")
        result_obj = json.loads(response_body.split('\n')[0])
        if result_obj['state'] == 'success':
            request.session['userId'] = result_obj['user_id']
            request.session['userName'] = result_obj['user_name']


def addOrLogin(user_id, user_name):
    user = User.objects.filter(user_id = user_id)
    if user.exists():
        return 'おかえりなさい'
    else:
        addUser = User(user_id=user_id, user_name=user_name)
        addUser.save()
        return 'ようこそ！'
