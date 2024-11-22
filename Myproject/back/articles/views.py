from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Articles, Comments
from .serializers import ArticleSerializer, CommentSerializer



# 게시글 관련 API는 인증이 필요하므로 데코레이터 순서 중요
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def article_list_create(request):
    if request.method == "GET":  #게시글 조회
        articles = Articles.objects.all()
        serializers = ArticleSerializer(articles, many=True)
        return Response(serializers.data) 
    elif request.method == "POST": #게시글 생성
        serializer = ArticleSerializer(data=request.data) #data값으로 post받은 값 전달
        if serializer.is_valid(raise_exception=True): #예외 처리 진행
            # 정우수정부분ㅋ.ㅋ
            serializer.save(user=request.user) 
            print('request', request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE', 'PUT']) #항상 최상단
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def article_detail(request, pk): 
    article = get_object_or_404(Articles, pk=pk) #해당 데이터 request.method에서 많이 사용되기 때문에 공통 요소로 할당함
    if request.method == "GET":
        serializer = ArticleSerializer(article) #게시글 단일 항목 조회
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE": #게시글 단일 항목 제거
        article.delete()
        data= {
            'delete' : '게시글이 삭제 되었습니다.'
        }
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == "PUT": #단일 게시글 업데이트
        serializer = ArticleSerializer(instance=article, data=request.data) #기존 article 데이터 전달
        #게시글 수정시, 1번 게시글을 수정했어요라고 입력하지 않기 떄문에 instance로 기본 값 전달후 data로 request로 
        #요청한 값 input
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            data= {
                'delete' : '게시글이 업데이트 되었습니다.'
            }
            return Response(data, status=status.HTTP_200_OK)
        
@api_view(['GET']) #항상 최상단
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def article_comment(request, pk):
    if request.method == "GET": #댓글 조회
        comments = Comments.objects.filter(article_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication]) #통
@permission_classes([IsAuthenticated])
def comment_create(request, pk): #댓글 생성 => 어떤 게시글에 있는 댓글인지에 대한 내용 : pk
    article = Articles.objects.get(pk=pk)
    serializer = CommentSerializer(data=request.data) #data 정보에 POST로 전달한 정보 담음
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article) # 어떠한 게시글에 대한 내용인지에 대한 내용 전달 => article 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'DELETE', 'PUT', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def article_comment_detail(request, comment_pk): #단일 댓글 조회
    comment = Comments.objects.get(pk=comment_pk)
    if request.method == "GET":
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == "DELETE": #단일 댓글 삭제
        comment.delete()
        data= {
            'delete' :f'댓글 {comment_pk}번이 삭제 되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT": #단일 댓글 수정
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True) :
            serializer.save()
            return Response(serializer.data)
