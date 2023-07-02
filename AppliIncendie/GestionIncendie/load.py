from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import *


dp_mapping = {
    "nom_dp": "DPEFLCD",
    "geometry_dp": "Polygon"
}

ccdrf_mapping = {
    "dp_ccdrf": {'nom_dp': "DPEFLCD"},
    "nom_ccdrf": "CCDRF",
    "comment_ccdrf": "DESCRIP",
    "geometry_ccdrf": "Polygon"
}


sf_mapping = {
    "ccdrf": {'nom_ccdrf': "CCDRF"},
    "nom_sf": "SECTEUR",
    "comment_sf": "CMT_SF",
    "geometrie_sf": "Polygon"
}

incendies_mapping = {
    "dp_icd": {'nom_dp': "DPEFLCD"},
    "date_eclosion": "DATE_ECLOS",
    "date_arret": "DATE_ARRET",
    "cause_incendie": "CAUSE",
    "surface_brulee": "SURFACE_BR",
    "cout_financier": "COUT_FINAN",
    "comment_incendie": "COMMT_ICD",
    "geometrie_incendie": "Point"
}

point_eau_mapping = {
    "dp_pe": {'nom_dp': "DPEFLCD"},
    "nom_pe": "NOM_LIEU",
    "date_creation_pe": "DATE_CREAT",
    "altitude_pe": "ALTITUDE",
    "capacite_eau": "qte_eau",
    "etat_pe": "ETAT_PE",
    "geometrie_pe": "MultiPoint"
}

postesVigies_mapping = {
    "dp_pv": {'nom_dp': "DPEFLCD"},
    "nom_pv": "NOM_LIEU",
    "date_creation_pv": "CREAT_DATE",
    "altitude_pv": "ALT_PV",
    "etat_pe": "ETAT_PV",
    "geometrie_pe": "MultiPoint"
}

tpf_mapping = {
    "dp_tpf": {'nom_dp': "DPEFLCD"},
    "etat_tpf": "ETAT",
    "largeur_tpf": "LARGEUR",
    "geometrie_tpf": "LineString"
}

dp_sh = Path(__file__).resolve().parent / "data" / "DP.shp"
ccdrf_shp = Path(__file__).resolve().parent / "data" / "CCDRF.shp"
sf_shp = Path(__file__).resolve().parent / "data" / "SecteursForestier.shp"
incendies_shp = Path(__file__).resolve().parent / "data" / "Incendies.shp"
points_eau_shp = Path(__file__).resolve().parent / "data" / "PointsEaux.shp"
postesVigies_shp = Path(__file__).resolve().parent / "data" / "PostesVigies.shp"
tpf_shp = Path(__file__).resolve().parent / "data" / "TranchePF.shp"

models = [Incendie, PointEau, PosteVigie, TracheeParFeu]
fichiers = [incendies_shp, points_eau_shp, postesVigies_shp, tpf_shp]
mappings = [incendies_mapping, point_eau_mapping, postesVigies_mapping, tpf_mapping]


def run(verbose=True):
    for i in range(len(models)):
        lm = LayerMapping(models[i], fichiers[i], mappings[i], transform=False)
        lm.save(strict=True, verbose=verbose)