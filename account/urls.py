from django.urls import path
from django.contrib.auth import views
from account.views import SigninView, SignoutView, Profile

urlpatterns = [
    path('signup/', SigninView.as_view(), name='signup'),
    path('signin/', views.LoginView.as_view(), name='login'),
    path('signout/', SignoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('profile/', Profile.as_view(), name='profile'),
]