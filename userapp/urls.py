from django.urls import path
from .views import (GetUserListView, GetUserDetailView,
                    PutUserDetailView, RegisterView,
                    ObtainTokenView, LogoutView)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('list/', GetUserListView.as_view()),
    path('get_detail/<int:pk>/', GetUserDetailView.as_view()),
    path('put_detail/<int:pk>/', PutUserDetailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', ObtainTokenView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]
