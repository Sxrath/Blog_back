from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics, status
from . import models,serializers
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import BlogPostSerializer, CreateBlogSerializer, LoginSerializer, ProfileSerializer, RegistrationSerializer, RetrieveBlogSerializer, UpdateBlogSerializer
User = get_user_model()

#auth------------------------------------------------------------------------------------------------
#Registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email,
            'id':user.id,
      })


#Login

class CustomLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Use the LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the input

        username = serializer.validated_data['username']  # This can be username or email
        password = serializer.validated_data['password']

        # Attempt to authenticate with the username
        user = authenticate(username=username, password=password)

        # If authentication fails, try with email
        if user is None:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    pass  # Authentication successful, do nothing
                else:
                    user = None  # Invalid password
            except User.DoesNotExist:
                user = None  # User not found

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'id': user.id,
                'message': 'Login successful'
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

#profile------------------------------------------------------------------------------------------------
#Create-User Profile
class CreateProfile(generics.CreateAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user  # Retrieve the authenticated user
        if not user or not user.is_authenticated:
            # If user is not authenticated, return a 401 Unauthorized response
            return Response({"detail": "User not found", "code": "user_not_found"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Save the profile and associate it with the authenticated user
        serializer.save(user=user)
        super().perform_create(serializer)

#update User-Profile
# views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import serializers
from . import models


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import models

class UpdateProfile(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure we get the profile for the authenticated user
        user = self.request.user
        if not user or not user.is_authenticated:
            raise Response({"detail": "User not found", "code": "user_not_found"}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the profile associated with the authenticated user
        try:
            profile = models.Profile.objects.get(user=user)
        except models.Profile.DoesNotExist:
            raise Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return profile

    def update(self, request, *args, **kwargs):
        # The update logic can be handled by the parent class
        return super().update(request, *args, **kwargs)


#blog---------------------------------------------------------------------------------------------
#Create Blog
class CreateListBlog(generics.ListCreateAPIView):
    serializer_class = CreateBlogSerializer
    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):#List Blog created by user
        user = self.request.user
        return models.BlogPost.objects.filter(author=user)

#List All blogs
class BlogListView(generics.ListAPIView):
    queryset = models.BlogPost.objects.all()
    serializer_class = BlogPostSerializer


#Detail view of blogs
class BlogDetailView(generics.RetrieveAPIView):
    queryset = models.BlogPost.objects.all()
    serializer_class = RetrieveBlogSerializer
    lookup_field = 'id'

    def get_object(self):
        blog_id = self.kwargs.get('id')
        try:
            return models.BlogPost.objects.get(id=blog_id)
        except models.BlogPost.DoesNotExist:
            raise Http404("Blog post not found.")
#Update Blog
class BlogUpdateView(generics.RetrieveUpdateAPIView):
    queryset = models.BlogPost.objects.all()
    serializer_class = UpdateBlogSerializer
    lookup_field = 'id'

    def get_object(self):
        blog_id = self.kwargs.get('id')
        try:
            return models.BlogPost.objects.get(id=blog_id)
        except models.BlogPost.DoesNotExist:
            raise Http404("Blog post not found.")

#delete Blog
class DeleteBlogView(generics.DestroyAPIView):
    queryset = models.BlogPost.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response({"detail": "Blog post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

#get ALl Tags----------------------------------------
class TagListView(generics.ListAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.GetAllTagSerializer
    