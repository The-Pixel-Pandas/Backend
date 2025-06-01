from django.shortcuts import render
from django.db import connections
from django.http import HttpResponse

# Create your views here.

def check_postgresql_connection(request):
    try:
        connection = connections['default']
        connection.ensure_connection()
        return HttpResponse("PostgreSQL connection successful")
    except Exception as e:
        return HttpResponse(f"PostgreSQL connection failed: {e}")
