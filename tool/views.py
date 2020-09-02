from django.http import JsonResponse
from django.shortcuts import render, render_to_response

# Create your views here.

from django.views.decorators.csrf import csrf_exempt


def ToolPage(request):
    return render_to_response("tool.html")






