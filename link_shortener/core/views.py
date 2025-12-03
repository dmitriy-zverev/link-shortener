from django.shortcuts import redirect

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Link,
    LinkStatistic,
)

from .serializers import (
    LinkSerializer, )


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.prefetch_related('linkstatistic').all()
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'short_code'

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Link.objects.none()

        if self.request.user.is_staff:
            return super().get_queryset()

        return Link.objects.filter(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        target_url = instance.url
        LinkStatistic.objects.create(link=instance, user=request.user)

        return redirect(target_url, status=status.HTTP_307_TEMPORARY_REDIRECT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['get'],
            url_path='details',
            permission_classes=[permissions.IsAuthenticated])
    def details(self, request, short_code=None):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'detail': 'Not authorized'},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
