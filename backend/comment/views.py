from django.db.models import QuerySet, Prefetch
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter

from comment.models import Comment
from comment.serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    CommentListSerializer,
)


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["user__username", "user__email", "created_at"]

    def get_serializer_class(self) -> type[CommentSerializer]:
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentListSerializer

    def get_queryset(self) -> QuerySet:
        return (
            Comment.objects.filter(parent=None)
            .select_related("user")
            .prefetch_related(
                Prefetch("replies", queryset=Comment.objects.select_related("user"))
            )
        )

    def perform_create(self, serializer: CommentCreateSerializer):
        serializer.save(user=self.request.user)
