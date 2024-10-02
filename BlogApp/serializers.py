from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from  . import models
from rest_framework.validators import UniqueValidator

#auth---------------------------------------------------------------------------
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text="Username or email")
    password = serializers.CharField(required=True, write_only=True, help_text="Your password")

    def validate(self, attrs):
        # This method can be used for any additional validation if needed
        return attrs


#Profile-------------------------------------------------------------------------    
# class CreateUpdateProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Profile
#         fields=["profile_picture","bio"]
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['profile_picture', 'bio']

#blog-------------------------------------------------------------------------
class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogPost
        fields = ['title','image', 'content', 'tags']

    def create(self, validated_data):
        # Extract tags from validated data
        tags_data = validated_data.pop('tags', None)  # Remove 'tags' from validated_data
        
        # Create the BlogPost instance
        blog_post = models.BlogPost.objects.create(**validated_data)
        
        # Add the tags to the blog_post using set()
        if tags_data:
            blog_post.tags.set(tags_data)  # Use set() to assign the many-to-many field
        
        return blog_post

    def validate(self, data):
        if 'title' not in data or len(data['title']) == 0:
            raise serializers.ValidationError("Title is required.")
        return data
class GetAllTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields=["id","tag_name"]

from rest_framework import serializers
from .models import BlogPost, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_name']  # Include the ID if needed for updates

class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)  # Use this to serialize/deserialize tags
    username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', "username",'image', 'created_at', 'tags']


    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        # Clear existing tags and add the new ones
        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            instance.tags.add(tag)

        return instance

        

class RetrieveBlogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username', read_only=True)
    tag_name=serializers.CharField(source='tag.tag_name',read_only=True)
    class Meta:
        model = models.BlogPost
        fields = ['id', 'title', 'content', 'author','username', 'tags','tag_name','image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class UpdateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogPost
        fields=['title','content']
        read_only_fields = ['author', 'created_at', 'updated_at']


       
