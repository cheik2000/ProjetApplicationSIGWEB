from pathlib import Path
from AppliIncendie import GestionIncendie
from django.contrib.gis.gdal import DataSource

directions_p = Path(GestionIncendie.__file__).resolve().parent / 'data' / 'DP.shp'
"""# On transforme le fichier en source de données
ds = DataSource(directions_p)
# On récupère la couche de données dans la source de données
layer = ds[0]"""

# layer.geom_type -> retourn le type de géométrie
# len(layer) -> return le nombre d'entités
# layer.srs -> return le system de coordonnées
# layer.fields -> retourn une liste des champ du shapefile
# [fld.__name__ for fld in layer.field_types] -> retourne la liste des types de champ
# for i in layer : i.get('attribute_name') -> retourne la valeur de l'attribut
# et i.geom -> retourne la géométrie de l'objet
# a = i.geom alors a.json -> forme json de l'objet et retourn un objet json :
#       { "type": "Polygon", "coordinates": [ [ [ 12.415798, 43.957954 ], [ 12.450554, 43.979721 ], ...}
