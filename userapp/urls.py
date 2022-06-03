from django.urls import path
from .views import (GetUserListView, GetUserDetailView,
                    PutUserDetailView, RegisterView,
                    ObtainTokenView, LogoutView)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('user/list/', GetUserListView.as_view()),
    path('user/get_detail/<int:pk>/', GetUserDetailView.as_view()),
    path('user/put_detail/<int:pk>/', PutUserDetailView.as_view()),
    path('user/register/', RegisterView.as_view()),
    path('user/login/', ObtainTokenView.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/logout/', LogoutView.as_view(), name='auth_logout'),
]
