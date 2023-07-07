from django.db.models import Sum, Count
from django.shortcuts import render
from django.contrib.gis.db import models
from django.core.serializers import serialize
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

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


def details_dref(request):

    # --------- Sous directions -----------------
    nbr_dp = DirectionProvinciale.objects.all().count()
    nbr_ccdrf = Ccdrf.objects.all().count()
    nbr_sf = SecteurForestier.objects.all().count()

    # --------- Infrastructures ------------------
    nbr_pe = PointEau.objects.all().count()
    nbr_pv = PosteVigie.objects.all().count()
    nbr_tpf = TracheeParFeu.objects.all().count()

    # ---- Incendies cette année ----------
    nbr_icd_curent_year = Incendie.objects.filter(date_eclosion__year=datetime.today().year).count()
    srf_current_year = Incendie.objects.filter(date_eclosion__year=datetime.today().year).aggregate(surf_total=models.Sum('surface_brulee'))['surf_total']
    if nbr_icd_curent_year > 0:
        surf_par_icd_current = srf_current_year/nbr_icd_curent_year
    else:
        surf_par_icd_current = 0

        # --------- Stats sur les incendies ------------
    nbr_total_incendies = Incendie.objects.all().count()
    surface_total_brl = Incendie.objects.aggregate(surf_total=models.Sum('surface_brulee'))['surf_total']
    if nbr_total_incendies > 0:
        surf_par_incendie = surface_total_brl / nbr_total_incendies
    else:
        surf_par_incendie = 0

    surface_grp_year = Incendie.objects.values('date_eclosion__year').annotate(surface=Sum('surface_brulee'),
                                nbr_incendies=Count('dp_icd')).order_by('date_eclosion__year')
    years = [e['date_eclosion__year'] for e in surface_grp_year]
    surfaces = [e['surface'] for e in surface_grp_year]
    nbrs = [e['nbr_incendies'] for e in surface_grp_year]

    # Graphique des surfaces brûlées au cours du temps
    fig_surface = go.Figure(data=go.Bar(x=years, y=surfaces))
    fig_surface.update_layout(
        title={
            'text': 'Évolution des surfaces brûlées par an', 'xanchor': 'center', 'x': 0.5
        }, xaxis_title='Année', yaxis_title='Surface brûlée (ha)')

    # Graphique du nombre d'incendies au cours du temps
    fig_nbr_icd = go.Figure(data=go.Bar(x=years, y=nbrs))
    fig_nbr_icd.update_layout(
        title={
            'text': 'Évolution du nombre d\'incendie par an', 'xanchor': 'center', 'x': 0.5
        }, xaxis_title='Année', yaxis_title='Nombre d\'incendies')

    context = {
        'nbr_dp': nbr_dp, 'nbr_ccdrf': nbr_ccdrf, 'nbr_sf': nbr_sf, 'nbr_pe': nbr_pe, 'nbr_pv': nbr_pv,
        'nbr_tpf': nbr_tpf,
        'nbr_total_icd': nbr_total_incendies, 'surface_total_brl': surface_total_brl, 'surf_per_icd': surf_par_incendie,
        'surface_par_an': surface_grp_year,
        'nbr_current': nbr_icd_curent_year, 'surface_ccurent': srf_current_year, 'srf_par_icd_current': surf_par_icd_current,
        'div_graph_surface': fig_surface.to_html(full_html=False),
        'div_graph_nbr_icd': fig_nbr_icd.to_html(full_html=False)
    }

    return render(request, 'GestionIncendie/details_global.html', context=context)


def details_dp(request, id_dp):
    dp = DirectionProvinciale.objects.get(nom_dp=id_dp)

    # --------- Sous directions -----------------
    nbr_ccdrf = dp.ccdrf.all().count()
    nbr_sf = SecteurForestier.objects.filter(geometrie_sf__contained=dp.geometry_dp).count()

    # --------- Infrastructures ------------------
    nbr_pe = dp.points_eaux.all().count()
    nbr_pv = dp.postes_vigies.all().count()
    nbr_tpf = dp.tpf.all().count()

    # ---- Incendies cette année ----------
    nbr_icd_curent_year = dp.incendies.filter(date_eclosion__year=datetime.today().year).count()
    srf_current_year = dp.incendies.filter(date_eclosion__year=datetime.today().year).aggregate(surf_total=models.Sum('surface_brulee'))['surf_total']
    if nbr_icd_curent_year > 0:
        surf_par_icd_current = srf_current_year/nbr_icd_curent_year
    else:
        surf_par_icd_current = 0

        # --------- Stats sur les incendies ------------
    nbr_total_incendies = dp.incendies.all().count()
    surface_total_brl = dp.incendies.aggregate(surf_total=models.Sum('surface_brulee'))['surf_total']
    if nbr_total_incendies > 0:
        surf_par_incendie = surface_total_brl / nbr_total_incendies
    else:
        surf_par_incendie = 0

    surface_grp_year = dp.incendies.values('date_eclosion__year').annotate(surface=Sum('surface_brulee'),
                                nbr_incendies=Count('dp_icd')).order_by('date_eclosion__year')

    years = [e['date_eclosion__year'] for e in surface_grp_year]
    surfaces = [e['surface'] for e in surface_grp_year]
    nbrs = [e['nbr_incendies'] for e in surface_grp_year]

    # Graphique des surfaces brûlées au cours du temps
    fig_surface = go.Figure(data=go.Bar(x=years, y=surfaces))
    fig_surface.update_layout(
        title={
            'text': 'Évolution des surfaces brûlées par an', 'xanchor': 'center', 'x': 0.5
        }, xaxis_title='Année', yaxis_title='Surface brûlée (ha)')

    # Graphique du nombre d'incendies au cours du temps
    fig_nbr_icd = go.Figure(data=go.Bar(x=years, y=nbrs))
    fig_nbr_icd.update_layout(
        title={
            'text': 'Évolution du nombre d\'incendie par an', 'xanchor': 'center', 'x': 0.5
        }, xaxis_title='Année', yaxis_title='Nombre d\'incendies')

    context = {
        'nom_dp': id_dp, 'nbr_ccdrf': nbr_ccdrf, 'nbr_sf': nbr_sf, 'nbr_pe': nbr_pe, 'nbr_pv': nbr_pv,
        'nbr_tpf': nbr_tpf,
        'nbr_total_icd': nbr_total_incendies, 'surface_total_brl': surface_total_brl, 'surf_per_icd': surf_par_incendie,
        'surface_par_an': surface_grp_year,
        'nbr_current': nbr_icd_curent_year, 'surface_ccurent': srf_current_year, 'srf_par_icd_current': surf_par_icd_current,
        'div_graph_surface': fig_surface.to_html(full_html=False),
        'div_graph_nbr_icd': fig_nbr_icd.to_html(full_html=False)
    }

    return render(request, 'GestionIncendie/details_dp.html', context=context)


def details_ccdrf(request, id_ccdrf):
    ccdrf = Ccdrf.objects.get(nom_ccdrf=id_ccdrf)

    # --------- Sous directions -----------------
    nbr_sf = SecteurForestier.objects.filter(geometrie_sf__contained=ccdrf.geometry_ccdrf).count()

    # --------- Infrastructures ------------------
    nbr_pe = PointEau.objects.filter(geometrie_pe__within=ccdrf.geometry_ccdrf).count()
    nbr_pv = PosteVigie.objects.filter(geometrie_pv__within=ccdrf.geometry_ccdrf).count()
    nbr_tpf = TracheeParFeu.objects.filter(geometrie_tpf__within=ccdrf.geometry_ccdrf).count()

    # ------------ Incendies cette année --------
    nbr_icd_curent_year = Incendie.objects.filter(geometrie_incendie__within=ccdrf.geometry_ccdrf)\
        .filter(date_eclosion__year=datetime.today().year).count()
    srf_current_year = Incendie.objects.filter(geometrie_incendie__within=ccdrf.geometry_ccdrf) \
        .filter(date_eclosion__year=datetime.today().year)\
        .aggregate(surf_total=models.Sum('surface_brulee'))['surf_total']
    if nbr_icd_curent_year > 0:
        surf_par_icd_current = srf_current_year/nbr_icd_curent_year
    else:
        surf_par_icd_current = 0

    # --------- Stats sur les incendies ------------
    nbr_total_incendies = Incendie.objects.filter(geometrie_incendie__within=ccdrf.geometry_ccdrf).count()
    surface_total_brl = Incendie.objects.filter(geometrie_incendie__within=ccdrf.geometry_ccdrf).aggregate(surf_total=models.Sum('surface_brulee'))['surf_total']
    if nbr_total_incendies > 0:
        surf_par_incendie = surface_total_brl / nbr_total_incendies
    else:
        surf_par_incendie = " - "

    surface_grp_year = Incendie.objects.values('date_eclosion__year')\
        .filter(geometrie_incendie__within=ccdrf.geometry_ccdrf)\
        .annotate(surface=Sum('surface_brulee'), nbr_incendies=Count('dp_icd')).order_by('date_eclosion__year')

    years = [e['date_eclosion__year'] for e in surface_grp_year]
    surfaces = [e['surface'] for e in surface_grp_year]
    nbrs = [e['nbr_incendies'] for e in surface_grp_year]

    # Graphique des surfaces brûlées au cours du temps
    fig_surface = go.Figure(data=go.Bar(x=years, y=surfaces))
    fig_surface.update_layout(
        title={
            'text': 'Évolution des surfaces brûlées par an', 'xanchor': 'center', 'x': 0.5
        }, xaxis_title='Année', yaxis_title='Surface brûlée (ha)')

    # Graphique du nombre d'incendies au cours du temps
    fig_nbr_icd = go.Figure(data=go.Bar(x=years, y=nbrs))
    fig_nbr_icd.update_layout(
        title={
            'text': 'Évolution du nombre d\'incendie par an', 'xanchor': 'center', 'x': 0.5
        }, xaxis_title='Année', yaxis_title='Nombre d\'incendies')

    context = {
        'nom_ccdrf': id_ccdrf, 'nbr_sf': nbr_sf, 'nbr_pe': nbr_pe, 'nbr_pv': nbr_pv,
        'nbr_tpf': nbr_tpf, 'nom_dp': ccdrf.dp_ccdrf,
        'nbr_total_icd': nbr_total_incendies, 'surface_total_brl': surface_total_brl, 'surf_per_icd': surf_par_incendie,
        'surface_par_an': surface_grp_year,
        'nbr_current': nbr_icd_curent_year, 'surface_ccurent': srf_current_year,
        'srf_par_icd_current': surf_par_icd_current,
        'div_graph_surface': fig_surface.to_html(full_html=False),
        'div_graph_nbr_icd': fig_nbr_icd.to_html(full_html=False)
    }

    return render(request, 'GestionIncendie/details_ccdrf.html', context=context)


def details_sf(request, id_sf):
    sf = SecteurForestier.objects.get(nom_sf=id_sf)

    # --------- Directions hierarchique -----------------
    nom_ccdrf = sf.ccdrf
    nom_dp = Ccdrf.objects.get(nom_ccdrf=nom_ccdrf).dp_ccdrf

    # --------- Infrastructures ------------------
    nbr_pe = PointEau.objects.filter(geometrie_pe__within=sf.geometrie_sf).count()
    nbr_pv = PosteVigie.objects.filter(geometrie_pv__within=sf.geometrie_sf).count()

    # ------------ Incendies cette année --------
    nbr_icd_curent_year = Incendie.objects.filter(geometrie_incendie__within=sf.geometrie_sf) \
        .filter(date_eclosion__year=datetime.today().year).count()
    srf_current_year = Incendie.objects.filter(geometrie_incendie__within=sf.geometrie_sf) \
        .filter(date_eclosion__year=datetime.today().year) \
        .aggregate(surf_total=models.Sum('surface_brulee'))['surf_total']
    if nbr_icd_curent_year > 0:
        surf_par_icd_current = srf_current_year / nbr_icd_curent_year
    else:
        surf_par_icd_current = 0

    # --------- Stats sur les incendies ------------
    nbr_total_incendies = Incendie.objects.filter(geometrie_incendie__within=sf.geometrie_sf).count()
    surface_total_brl = Incendie.objects.filter(geometrie_incendie__within=sf.geometrie_sf).aggregate(
        surf_total=models.Sum('surface_brulee'))['surf_total']
    if nbr_total_incendies > 0:
        surf_par_incendie = surface_total_brl / nbr_total_incendies
    else:
        surf_par_incendie = " - "

    surface_grp_year = Incendie.objects.filter(geometrie_incendie__within=sf.geometrie_sf)\
        .values('date_eclosion__year')\
        .annotate(surface=Sum('surface_brulee'),nbr_incendies=Count('dp_icd')).order_by('date_eclosion__year')

    years = [e['date_eclosion__year'] for e in surface_grp_year]
    surfaces = [e['surface'] for e in surface_grp_year]
    nbrs = [e['nbr_incendies'] for e in surface_grp_year]

    # Graphique des surfaces brûlées au cours du temps
    fig_surface = go.Figure(data=go.Bar(x=years, y=surfaces))
    fig_surface.update_layout(
        title={
            'text': 'Évolution des surfaces brûlées par an', 'xanchor': 'center', 'x': 0.5
        }, xaxis_title='Année', yaxis_title='Surface brûlée (ha)')

    # Graphique du nombre d'incendies au cours du temps
    fig_nbr_icd = go.Figure(data=go.Bar(x=years, y=nbrs))
    fig_nbr_icd.update_layout(
        title={
            'text': 'Évolution du nombre d\'incendie par an', 'xanchor': 'center', 'x': 0.5
        }, xaxis_title='Année',yaxis_title='Nombre d\'incendies')

    context = {
        'nom_sf': id_sf, 'nom_ccdrf': nom_ccdrf, 'nom_dp': nom_dp,'nbr_pe': nbr_pe, 'nbr_pv': nbr_pv,
        'nbr_total_icd': nbr_total_incendies, 'surface_total_brl': surface_total_brl, 'surf_per_icd': surf_par_incendie,
        'surface_par_an': surface_grp_year,
        'nbr_current': nbr_icd_curent_year, 'surface_curent': srf_current_year,
        'srf_par_icd_current': surf_par_icd_current,
        'div_graph_surface': fig_surface.to_html(full_html=False),
        'div_graph_nbr_icd': fig_nbr_icd.to_html(full_html=False)
    }

    return render(request, 'GestionIncendie/details_sf.html', context=context)