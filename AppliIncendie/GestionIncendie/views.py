from django.shortcuts import render
from django.core.serializers import serialize

from .models import DirectionProvinciale, Ccdrf, SecteurForestier, Incendie, PosteVigie, TracheeParFeu, PointEau


# Create your views here.
def page_accueil(request):
    """La page d'accueil du site web"""
    return render(request, "GestionIncendie/index.html", {})


def map(request):
    """Retourne la liste des incendies au format Json"""

    context = {
        "incendies": serialize('geojson', Incendie.objects.all()),
        'directionsP': serialize('geojson', DirectionProvinciale.objects.all()),
        'ccdrf': serialize('geojson',Ccdrf.objects.all()),
        'secteursF': serialize('geojson', SecteurForestier.objects.all()),
        'pointsEaux': serialize('geojson', PointEau.objects.all()),
        'postesVigies': serialize('geojson', PosteVigie.objects.all()),
        'tranchePF': serialize('geojson', TracheeParFeu.objects.all())
    }

    # Retour du résultat au client
    return render(request, 'GestionIncendie/index.html', context=context)
