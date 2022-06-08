from django.conf import settings
from django.urls import path, include
from . import views
from django.conf.urls.static import static



urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login", views.login_user, name="login"),
    path("profile/", views.profile, name="profile"),
    path("profile_update/", views.profile_update, name="profile_update"),
    path('search/', views.search_results, name='search_results'),
    path('upload_image/', views.upload_image, name= 'upload_image'),
    path('comment/<int:image_id>', views.add_comment, name='comment'),
    path('like/<int:image_id>', views.like_image,name='like'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
