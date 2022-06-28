from .models import Category


# Using context preprocessor to get all the category name and can pass it to any of the template by calling it in settings
def menu(request):
    link = Category.objects.all()
    return dict(link=link)