from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('stored-videos/',views.storedvideo,name="stored-videos"),
    path('multiple-stream/',views.multiplestream,name="multiple-stream"),
    path('live-stream/',views.livestream,name="live-stream"),
    path('admin_das/',views.admin_das,name="admin_das"),
    path('login/',views.loginPage,name="login"),
    path('signup/',views.signupPage,name="signup"),
    path('logout/',views.logoutPage,name="logout"),
]