# from django.contrib.auth.models import User
# from rest_framework import viewsets
# from api2.serializers import UserSerializer, PostSerializer, CommentSerializer
# from blog.models import Post, Comment

# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
    
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

from collections import OrderedDict
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.utils import obj_to_comment, obj_to_post, prev_next_post
from blog.models import *
from rest_framework.pagination import PageNumberPagination
# from api2.serializers import PostListSerializer, PostRetrieveSerializer, CommentSerializer, PostLikeSerializer, CateTagSerializer
from api2.serializers import PostListSerializer, CommentSerializer, CateTagSerializer, PostSerializerDetail


# class CommentCreateAPIView(CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

    
class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()
        data = {
            'cateList' : cateList,
            'tagList' : tagList,
        }
        
        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)
        

class PostPageNumberPagination(PageNumberPagination):
    page_size = 3
    # page_size_query_param = 'page_size'
    # max_page_size = 1000
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))
        
        
# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     pagination_class = PostPageNumberPagination
    
#     def get_serializer_context(self):
#         """
#         Extra context provided to the serializer class.
#         """
#         return {
#             'request': None,
#             'format': self.format_kwarg,
#             'view': self
#         }
        
        
# # serializer 사용 안하고 Dictionary를 만들어 사용      
# class PostRetrieveAPIView(RetrieveAPIView):
#     def get_queryset(self):
#         return Post.objects.all().select_related('category').prefetch_related('tags', 'comment_set')
    
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         commentList = instance.comment_set.all()
        
#         postDict = obj_to_post(instance)
#         prevDict, nextDict = prev_next_post(instance)
#         commentDict = [obj_to_comment(c) for c in commentList]
        
#         dataDict = {
#             'post' : postDict,
#             'prevPost' : prevDict,
#             'nextPost' : nextDict,
#             'commentList' : commentDict
#         }
        
#         return Response(dataDict)
    
# class PostLikeAPIView(GenericAPIView):
#     queryset = Post.objects.all()
#     # serializer_class = PostLikeSerializer
    
#     #GET method
#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.like += 1        
#         instance.save()

#         # return Response(serializer.data)
        
        
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination
    
    #PostList
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }
    
    #PostRetrive
    def get_queryset(self):
        return Post.objects.all().select_related('category').prefetch_related('tags', 'comment_set')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        commentList = instance.comment_set.all()
        
        postDict = obj_to_post(instance)
        prevDict, nextDict = prev_next_post(instance)
        commentDict = [obj_to_comment(c) for c in commentList]
        
        dataDict = {
            'post' : postDict,
            'prevPost' : prevDict,
            'nextPost' : nextDict,
            'commentList' : commentDict
        }
        
        return Response(dataDict)
    
    #PostLike
    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1        
        instance.save()
        return Response(instance.like)   #숫자만 보내고 싶을 때
        
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer