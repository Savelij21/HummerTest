from django.urls import path
from . import views


urlpatterns = [

    path('auth/phone/', views.AuthViewSet.as_view({'post': 'phone_auth'})),
    path('auth/code/', views.AuthViewSet.as_view({'post': 'code_auth'})),

    path('profile/', views.UserViewSet.as_view({'get': 'get_profile'})),
    path('profile/foreign_invite_code/', views.UserViewSet.as_view({'post': 'set_foreign_invite_code'})),

    path('logout/', views.UserViewSet.as_view({'post': 'user_logout'})),
]
