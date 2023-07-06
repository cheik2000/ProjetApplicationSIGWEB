from django.db.models import Sum, Count
from django.db.models.functions import ExtractYear
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.gis.db import models
from django.core.serializers import serialize

from .models import DirectionProvinciale, Ccdrf, SecteurForestier, Incendie, PosteVigie, TracheeParFeu, PointEau


# Create your views here.
def page_accueil(request):
    """La page d'accueil du site web"""
    return render(request, "GestionIncendie/index.html", {})


def map(request):
    """Retourne la liste des incendies au format Json"""

    context = {
        'directionsP': serialize('geojson', DirectionProvinciale.objects.all()),
        'ccdrf': serialize('geojson', Ccdrf.objects.all()),
        'secteursF': serialize('geojson', SecteurForestier.objects.all()),
        'pointsEaux': serialize('geojson', PointEau.objects.all()),
        'postesVigies': serialize('geojson', PosteVigie.objects.all()),
        'tranchePF': serialize('geojson', TracheeParFeu.objects.all())
    }

    # Retour du résultat au client
    return render(request, 'GestionIncendie/index.html', context=context)


def details_dp(request, id_dp):
    dp = DirectionProvinciale.objects.get(nom_dp=id_dp)

    # --------- Sous directions -----------------
    nbr_ccdrf = dp.ccdrf.all().count()
    nbr_sf = SecteurForestier.objects.filter(geometrie_sf__contained=dp.geometry_dp).count()

    # --------- Infrastructures ------------------
    nbr_pe = dp.points_eaux.all().count()
    nbr_pv = dp.postes_vigies.all().count()
    nbr_tpf = dp.tpf.all().count()

    # --------- Stats sur les incendies ------------
    nbr_total_incendies = dp.incendies.all().count()
    surface_total_brl = round(dp.incendies.aggregate(surf_total=models.Sum('surface_brulee'))['surf_total'], 2)
    if nbr_total_incendies > 0:
        surf_par_incendie = round(surface_total_brl / nbr_total_incendies, 2)
    else:
        surf_par_incendie = " - "

    surface_grp_year = dp.incendies.values('date_eclosion__year').annotate(surface=Sum('surface_brulee'),
                                nbr_incendies=Count('dp_icd')).order_by('date_eclosion__year')
    print(surface_grp_year)
    context = {
        'nom_dp': id_dp, 'nbr_ccdrf': nbr_ccdrf, 'nbr_sf': nbr_sf, 'nbr_pe': nbr_pe, 'nbr_pv': nbr_pv,
        'nbr_tpf': nbr_tpf,
        'nbr_total_icd': nbr_total_incendies, 'surface_total_brl': surface_total_brl, 'surf_per_icd': surf_par_incendie,
        'surface_par_an': surface_grp_year
    }

    return render(request, 'GestionIncendie/details_dp.html', context=context)
