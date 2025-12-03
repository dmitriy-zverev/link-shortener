from rest_framework import serializers

from .models import (
    Link, )

from users.serializers import (
    UserSerializer, )

from .utils import generate_unique_shortcode


class LinkSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    short_code = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Link
        fields = ('id', 'url', 'short_code', 'author', 'created_at',
                  'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def get_short_code(self, obj):
        return obj.short_code

    def create(self, validated_data):
        validated_data['short_code'] = generate_unique_shortcode()
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['total_views'] = instance.linkstatistic.count()

        return data
