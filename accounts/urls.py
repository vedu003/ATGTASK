from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('home/',views.home,name='home'),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
