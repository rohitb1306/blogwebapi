from blog.api.serializer import BlogSerializer, CommentSerializer
from blog.models import Blog,Comment
from rest_framework import viewsets

class BlogViewSets(viewsets.ModelViewSet):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer

# class CommentViewSets(viewsets.ReadOnlyModelViewSet):
#     queryset=Comment.objects.all()
#     serializer_class=CommentSerializer

class CommentViewSets(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer