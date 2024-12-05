from rest_framework import serializers

from comment.models import Comment
from user.serializers import UserReadSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "text",
            "created_at",
            "updated_at",
            "home_page",
            "attached_image",
            "attached_file",
            "parent",
        )
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "updated_at",
        )


class CommentCreateSerializer(CommentSerializer):
    pass


class CommentListSerializer(CommentSerializer):
    replies = serializers.SerializerMethodField()

    class Meta(CommentSerializer.Meta):
        fields = (
            "id",
            "user",
            "text",
            "created_at",
            "updated_at",
            "home_page",
            "attached_image",
            "attached_file",
            "replies"
        )

    def get_replies(self, comment):
        replies = comment.replies.all()
        return CommentListSerializer(replies, many=True).data
