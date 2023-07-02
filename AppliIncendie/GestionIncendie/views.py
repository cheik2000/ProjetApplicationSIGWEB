from django.shortcuts import render


# Create your views here.
def page_accueil(request):
    """La page d'accueil du site web"""
    return render(request, "GestionIncendie/index.html", {})