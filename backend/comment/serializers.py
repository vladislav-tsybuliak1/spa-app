from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "text",
            "created_at",
            "updated_at",
            "reply",
        ]


class CommentCreateSerializer(CommentSerializer):
    pass


class CommentListSerializer(CommentSerializer):
    reply = serializers.SerializerMethodField()

    def get_reply(self, obj):
        replies = Comment.objects.filter(reply=obj)
        return CommentListSerializer(replies, many=True).data
