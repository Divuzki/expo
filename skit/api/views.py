from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .permissions import IsOwnerOrReadOnly
from ..models import Skit
from ..serializers import (
    SkitSerializer,
    SkitActionSerializer,
    SkitCreateSerializer,
)
from django.db.models import Q


from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework import status

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


class SkitAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = SkitSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20

    def get_queryset(self):
        """
        REST API VIEW
        Consume by JavaScript or Swift/Java/iOS/Andriod
        return json data
        """
        user = self.request.user
        qs = Skit.objects.feed(user).order_by("-timestamp")
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(user__username__icontains=query) |
                           Q(content__icontains=query) |
                           Q(caption__icontains=query) |
                           Q(parent__content__icontains=query) |
                           Q(parent__caption__icontains=query) |
                           Q(parent__user__username__icontains=query)
                           ).distinct()
        return qs

    def post(self, request, format=None):
        skits_serializer = SkitCreateSerializer(
            data=request.data, context={'request': request})
        if skits_serializer.is_valid():
            skits_serializer.save(user=request.user)
            return Response(skits_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(skits_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class SkitListView(generics.ListAPIView):
    serializer_class = SkitSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20

    def get_queryset(self):
        qs = Skit.objects.all()
        username = self.request.GET.get('username')
        query = self.request.GET.get("q")
        location = self.request.GET.get("location")
        if username != None:
            qs = qs.by_username(username)
        if location != None:
            qs = qs.by_location(location)
        if query != None:
            qs = qs.filter(Q(user__username__icontains=query) |
                           Q(content__icontains=query) |
                           Q(caption__icontains=query) |
                           Q(parent__content__icontains=query) |
                           Q(parent__caption__icontains=query) |
                           Q(parent__user__username__icontains=query)
                           ).distinct()
        return qs

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


# DetailView, UpdateView And EditView
class SkitDetailUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'  # slug, id | path('<int:pk>\d+')
    serializer_class = SkitSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]
    queryset = Skit.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def skit_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, repost
    '''
    serializer = SkitActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        skit_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        image = data.get("image")
        caption = data.get("caption")
        qs = Skit.objects.filter(id=skit_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            if request.user in obj.likes.all():
                obj.likes.remove(request.user)
            else:
                obj.likes.add(request.user)
            serializer = SkitSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "repost":
            if not obj.parent:
                if content:
                    new_skit = Skit.objects.create(
                        user=request.user,
                        parent=obj,
                        content=content,
                        image=None,
                        caption=None,
                    )
                elif not content and caption:
                        new_skit = Skit.objects.create(
                            user=request.user,
                            parent=obj,
                            content=None,
                            image=None,
                            caption=caption,
                    )
                else:
                    new_skit = Skit.objects.create(
                        user=request.user,
                        parent=obj,
                        content=None,
                        image=None,
                        caption=None,
                    )
                serializer = SkitSerializer(new_skit)
            return Response(serializer.data, status=201)
    return Response({}, status=200)
