from rest_framework import generics

from comment.models import Comment
from comment.serializers import CommentSerializer


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
