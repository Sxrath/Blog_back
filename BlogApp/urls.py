from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import BlogListView, CreateListBlog, CustomLoginView, CreateProfile,RegisterView,BlogDetailView,BlogUpdateView,DeleteBlogView,TagListView, UpdateProfile

urlpatterns=[
    #authentification-----------------------------------------------------
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
  
    #userData---------------------------------------------------------------

    #User-Profile------------------------------------------------------------
path('create-profile/', CreateProfile.as_view(), name='create-profile'),    #path('updateProfile/<int:id>/', ProfileUpdateView.as_view(), name='profile_update'),
 path('profile/update/<int:pk>/', UpdateProfile.as_view(), name='update-profile'),
    #Blog-------------------------------------------------------------------
    path('createBlog/', CreateListBlog.as_view(), name='create_blog'),
    path('ownBlog/', CreateListBlog.as_view(), name='list_own_blogs'),
    path('detail/<int:id>/', BlogDetailView.as_view(), name='detailview_blog'),
    path('updateBlog/<int:id>/', BlogUpdateView.as_view(), name='update_blog'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('deleteBlogs/<int:id>/', DeleteBlogView.as_view(), name='blog-delete'),

    path('getTag/', TagListView.as_view(), name='all Tag'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)