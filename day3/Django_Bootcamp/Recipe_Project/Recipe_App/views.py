from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .services.authentication import register_user, login_user, logout_user
from .services.recipe_service import save_recipe, get_user_recipes


def index(request):
    logout_user(request)
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user, error = register_user(username, email, password)

        if error:
            return render(request, "register.html", {"error": error})

        return redirect("login")

    return render(request, "register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        success = login_user(request, username, password)

        if success:
            return redirect("home")

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        title = request.POST.get("title")
        ingredients = request.POST.get("ingredients")
        instructions = request.POST.get("instructions")

        save_recipe(request.user, title, ingredients, instructions)
        return redirect("recipe_list")

    return render(request, "home.html")


@login_required(login_url='login')
def recipe_list(request):
    recipes = get_user_recipes(request.user)
    return render(request, "recipe_list.html", {"recipes": recipes})


@login_required(login_url='login')
def generate_recipe(request):
    context = {}
    if request.method == 'POST':
        title = request.POST.get('title', '')
        ingredients = request.POST.get('ingredients', '')
        context['title'] = title
        context['ingredients'] = ingredients

        if not title or not ingredients:
            context['error'] = 'Please fill in both fields.'
            return render(request, 'generate_recipe.html', context)

        # --- Gemini API Call ---
        GEMINI_API_KEY = ''  # <-- Replace with your API key
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}'

        prompt = (
            f"Give me a detailed recipe for '{title}' using these ingredients: {ingredients}. "
            f"Include step-by-step instructions, preparation time, cooking time, and serving size. "
            f"Format it nicely."
            f"Respond only with recipe detailsformattedin HTML,without any additional explanations or text."
        )

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            response = request.POST(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            recipe_text = data['candidates'][0]['content']['parts'][0]['text']
            context['recipe_result'] = recipe_text
        except Exception as e:
            context['error'] = f'Error from Gemini API: {str(e)}'

    return render(request, 'generate_recipe.html', context)

def user_logout(request):
    logout_user(request)
    return redirect("index")