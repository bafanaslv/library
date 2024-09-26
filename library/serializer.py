from rest_framework.serializers import ModelSerializer, SerializerMethodField

from library.models import Authors


class AuthorsSerializer(ModelSerializer):
    class Meta:
        model = Authors
        fields = "__all__"


