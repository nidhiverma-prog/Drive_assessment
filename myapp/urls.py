from django.conf.urls import url
from myapp.views import LoginView,LogoutView,movies_list
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    url('api/movies$',movies_list),
    url('api/vl/auth/login/', LoginView.as_view()),
    url('api/vl/auth/logout/', LogoutView.as_view()),
    url('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]    