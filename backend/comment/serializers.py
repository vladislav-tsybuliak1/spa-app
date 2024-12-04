from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "text",
            "created_at",
            "updated_at",
            "attached_image",
            "attached_field",
            "parent",
        )
        read_only_fields = (
            "id",
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
            "attached_image",
            "attached_field",
            "replies"
        )

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        return CommentListSerializer(replies, many=True).data
