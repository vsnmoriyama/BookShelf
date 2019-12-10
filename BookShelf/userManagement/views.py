from django.shortcuts import render, redirect
import urllib.request as url_request
import json
# Create your views here.
clientCode = 'BookShelf'
method = "POST"
headers = {"Content-Type": "application/json"}


def topPage(request):
    return render(request, 'userManage/top.html')


def menu(request):
    if request.GET['authCode']:
        authCode = request.GET['authCode']
        accessToken = authByAuthCode(authCode)
        request.session['accessToken'] = accessToken
    elif request.session['accessToken']:
        accessToken = request.session['accessToken']
    else:
        return redirect('userManage:top')

    authByAccessToken(request, accessToken)
    userData = {'userName': request.session['userName']}
    return render(request, 'userManage/menu.html', userData)


def authByAuthCode(auth_code):
    urlAuthCode = 'http://10.33.32.40:8080/projectStudy/authorization/authCode/'
    obj = {'client_code': clientCode, 'auth_code': auth_code}
    json_data = json.dumps(obj).encode("utf-8")
    authRequest = url_request.Request(urlAuthCode, data=json_data, method=method, headers=headers)
    with url_request.urlopen(authRequest) as response:
        response_body = response.read().decode("utf-8")
        result_obj = json.loads(response_body.split('\n')[0])
        accessToken = result_obj['code']
    return accessToken


def authByAccessToken(request, access_token):
    urlAccessToken = 'http://10.33.32.40:8080/projectStudy/authorization/accessToken/getData/'
    obj = {'client_code': clientCode, 'accessToken': access_token}
    json_data = json.dumps(obj).encode("utf-8")
    accessTokenRequest = url_request.Request(urlAccessToken, data=json_data, method=method, headers=headers)
    with url_request.urlopen(accessTokenRequest) as response:
        response_body = response.read().decode("utf-8")
        result_obj = json.loads(response_body.split('\n')[0])
        if result_obj['state'] == 'success':
            request.session['userId'] = result_obj['user_id']
            request.session['userName'] = result_obj['user_name']
