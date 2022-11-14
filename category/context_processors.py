from .models import Category
def menu_links(request):
    links=Category.objects.all()
    return dict(multiple_links=links)