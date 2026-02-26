from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def register_user(username, email, password):
    if User.objects.filter(username=username).exists():
        return None, "Username already exists"

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    return user, None


def login_user(request, username, password):
    user = authenticate(request, username=username, password=password)
    
    if user:
        login(request, user)
        return True
    
    return False


def logout_user(request):
    logout(request)
