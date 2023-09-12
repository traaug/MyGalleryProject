from django.urls import path, include
from django.contrib.auth import views as auth_views
from gallery import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
    path('photoview/<int:pk>', views.photoview, name='photoview'),
    path('add_photo/', views.add_photo, name='add_photo'),
    path('/delete_photo/<int:pk>', views.delete_photo, name='delete_photo'),
    path('update_photo/<int:pk>', views.UpdatePhoto.as_view(), name='update_photo'),
    path('search/', views.search_photos, name='search_photos'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


