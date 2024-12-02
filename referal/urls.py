from django.urls import path
from . import views


urlpatterns = [
    path('', views.ReferalTemplateView.as_view()),

    path('api/auth/phone/', views.AuthViewSet.as_view({'post': 'phone_auth'})),
    path('api/auth/code/', views.AuthViewSet.as_view({'post': 'code_auth'})),

    path('api/profile/', views.UserViewSet.as_view({'get': 'get_profile'})),
    path('api/profile/foreign_invite_code/', views.UserViewSet.as_view({'post': 'set_foreign_invite_code'})),

    path('api/logout/', views.UserViewSet.as_view({'post': 'user_logout'})),
]
