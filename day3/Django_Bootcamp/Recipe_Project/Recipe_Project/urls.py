"""
URL configuration for Recipe_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Recipe_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),           # Landing page (base route)
    path('register/', views.register, name='register'),  # Register page
    path('login/', views.user_login, name='login'),
    path('generate_recipe/', views.generate_recipe, name='generate_recipe'),   # Generate Recipe page
    path('home/', views.home, name='home'),              # Recipe input page (protected)
    path('list/', views.recipe_list, name='recipe_list'), # Recipe list page
    path('logout/', views.user_logout, name='logout'),   # Logout
]
