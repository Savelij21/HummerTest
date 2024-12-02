
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'phone', 'invite_code', 'foreign_invite_code', 'invited_users')

    def get_invited_users(self, obj):
        return User.objects.filter(foreign_invite_code=obj.invite_code).values_list('phone', flat=True)

