from django.shortcuts import render

# Swagger
from drf_spectacular.utils import extend_schema
from serializers import UserSerializer
# https://www.youtube.com/watch?v=XBxssKYf5G0    min 17:30
# @extend_schema(responses=UserSerializer)


# Create your views here.
