from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.contrib.staticfiles.views import serve
from config import settings
from . import MNISTpredict
from django.views.decorators.csrf import csrf_exempt

from django.contrib.staticfiles.storage import staticfiles_storage

import os
BUILD_DIR = 'draw' 

#from fancy import wrapper

# Create your views here.

def index(request):
    path = os.path.join(BUILD_DIR, request.path.lstrip(os.path.sep))
    if path is 'draw' or not staticfiles_storage.exists(path):
        path = os.path.join(BUILD_DIR, "index.html")
    
    return serve(request, path)

count = 0

@csrf_exempt
def api(request):
    global count

    ok = True
    message = "no error"
    result = ""
    try:
        next_name = "image_" + str(count) + ".png"
        count += 1
        MNISTpredict.save(request.FILES['file[]'], next_name)
        result = MNISTpredict.evaluate(next_name)
    except Exception as e:
        ok = False
        message = str(type(e)) + str(e)
    
    if ok:
        return JsonResponse({
            'ok' : True,
            'content' : { 'letter': result },
        })
    else:
        return JsonResponse({
            'ok' : False,
            'error' : 'noooooo',
            'message' : message,
        })


