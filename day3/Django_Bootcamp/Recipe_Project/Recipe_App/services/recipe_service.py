from ..models import Recipe

def save_recipe(user, title, ingredients, instructions):
    if not (title and ingredients and instructions):
        return None

    return Recipe.objects.create(
        user=user,
        title=title,
        ingredients=ingredients,
        instructions=instructions
    )


def get_user_recipes(user):
    return Recipe.objects.filter(user=user)