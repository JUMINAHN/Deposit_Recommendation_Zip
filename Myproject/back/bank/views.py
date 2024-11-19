from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Articles, Comments
from ..articles.serializers import ArticleSerializer, CommentSerializer

