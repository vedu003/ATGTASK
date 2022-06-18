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
    path('createblog/',views.createblog,name='createblog'),
    path('displayblogs/',views.displayblogs,name='displayblogs'),
    path('draft/',views.draft,name='draft'),
    path('editdraft/<int:id>/',views.editdraft,name='editdraft'),
    path('mycurrblog/',views.mycurrblog,name='mycurrblog'),
    path('delblog/<int:id>/',views.delblog,name='delblog'),
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
