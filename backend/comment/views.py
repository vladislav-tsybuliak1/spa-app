from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from comment.models import Comment
from comment.serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    CommentListSerializer,
)


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> type[CommentSerializer]:
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentListSerializer

    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(parent=None)

    def perform_create(self, serializer: CommentCreateSerializer):
        serializer.save(user=self.request.user)
