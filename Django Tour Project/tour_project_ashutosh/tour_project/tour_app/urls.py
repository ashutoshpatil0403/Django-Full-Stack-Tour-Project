from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.home,name='home'),
    path('packages/',views.package,name='package'),
    path("about/",views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.register),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout),
    path('search/',views.search.as_view(),name='search'),
    path('packages/<id>',views.select_package.as_view(),name="select_package"),
    path('user_book/',views.user_book,name="user_book"),
    path('delete/<uid>/',views.delete_booking,name="delete_booking"),
    path('confirm/',views.confirm),
    path('success/',views.success,name='success'),
    path('del/<id>/',views.del_conf,name="delete_booking"),
    path('viewticket/',views.view_tickets,name="view_tickets"),
    path('processed/<id>/',views.processed,name="processed"),
    path('imgadd/',views.imgadd.as_view(),name='imgadd'),
    path('search/', views.search_package_view, name='search_package_view'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

