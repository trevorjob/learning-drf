from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.serializers import CurrentUserPostsSerializer

from .models import Post
from .permissions import AuthorOrReadonly, ReadOnly
from .serializers import PostSerializer

# Create your views here.

POSTS = [
    {"id": 1, "message": "Hello this is first post"},
    {"id": 2, "message": "Hello this is second post"},
    {"id": 3, "message": "Hello this is third post"},
]


@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def homepage(request: Request):
    if request.method == "POST":
        data = request.data
        response = {"message": "Hello, World!", "data": data}
        return Response(data=response, status=status.HTTP_201_CREATED)
    response = {"message": "Hello, World!"}
    return Response(data=response, status=status.HTTP_200_OK)


class PostListCreateView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """
    a view for creating and listing posts

    Args:
        APIView (_type_): _description_

    Returns:
        _type_: _description_
    """

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [ReadOnly]
    # def get(self, request: Request, *args, **kwargs):
    #     posts = Post.objects.all()
    #     serializer = self.serializer_class(instance=posts, many=True)

    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

        return super().perform_create(serializer)

    @swagger_auto_schema(
        operation_summary="List all posts",
        operation_description="returns a list of all posts",
    )
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # def post(self, request: Request, *args, **kwargs):
    #     data = request.data
    #     serializer = self.serializer_class(data=data)

    #     if serializer.is_valid():
    #         serializer.save()

    #         response = {"message": "post created successfully", "data": serializer.data}
    #         return Response(data=response, status=status.HTTP_201_CREATED)
    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Create a post", operation_description="creates a new post"
    )
    def post(self, request: Request, *args, **kwargs):

        return self.create(request, *args, **kwargs)


class PostRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AuthorOrReadonly]

    @swagger_auto_schema(
        operation_summary="gets a single post",
        operation_description="retrieve a single post",
    )
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # def get(self, request: Request, post_id: int):
    #     post = get_object_or_404(Post, pk=post_id)

    #     serializer = self.serializer_class(instance=post)

    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_summary="update a post", operation_description="update a post"
    )
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # def put(self, request: Request, *args, **kwargs):
    #     post = get_object_or_404(Post, pk=post_id)

    #     data = request.data

    #     serializer = self.serializer_class(instance=post, data=data)

    #     if serializer.is_valid():
    #         serializer.save()

    #         response = {"message": "post updated successfully", "data": serializer.data}
    #         return Response(data=response, status=status.HTTP_200_OK)

    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="deletes a post", operation_description="deletes a post"
    )
    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    # def delete(self, request: Request, *args, **kwargs):
    #     post = get_object_or_404(Post, pk=post_id)

    #     post.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=["GET"])
@swagger_auto_schema(operation_summary="get current user posts")
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request):
    user = request.user
    serializer = CurrentUserPostsSerializer(instance=user, context={"request": request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListPostsForAuthor(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get("username") or None
        queryset = Post.objects.all()
        if username is not None:
            return Post.objects.filter(author__username=username)
        else:
            return queryset

    @swagger_auto_schema(operation_summary="retreve a list of post by author")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
