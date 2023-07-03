// Chargement des Incendies
var incendiesJson = function (reponse) {
    //var donnes = reponse.features;
    //console.log(donnes)
    var couche_incendies = L.geoJSON(reponse);
    return couche_incendies
};

var url = 'http://127.0.0.1:8000/map';
var getOptions = {
    method: 'GET',
    async: true,
    cache: false,
    success: incendiesJson
};
// $.ajax(url, getOptions);

// La variable qui contient la carte
var map;
var osm, esriIMG;
var couche_incendies, couche_dp, couche_ccdrf, couche_sf, couche_pe, couche_pv, couche_tpf;


document.addEventListener('DOMContentLoaded', function(){

    // Tuilage de couches raster
    osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    esriIMG = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    });

    // Récupération des données de mes 7 couches
    var incendies = JSON.parse(document.getElementById('data').getAttribute('incendies'));
    couche_incendies = L.geoJSON(incendies)

    var dp = JSON.parse(document.getElementById('data').getAttribute('dp'));
    couche_dp = L.geoJSON(dp, {
      style: function (feature) {
        return {
          fillColor: "transparent",  // Définir la couleur de remplissage sur "transparent"
          color: "blue",  // Couleur des contours du polygon
          weight: 4  // Épaisseur des contours du polygon
        }}
    });

    var ccdrf = JSON.parse(document.getElementById('data').getAttribute('ccdrf'));
    couche_ccdrf = L.geoJSON(ccdrf, {
      style: function (feature) {
        return {
          fillColor: "transparent",  // Définir la couleur de remplissage sur "transparent"
          color: "blue",  // Couleur des contours du polygon
          weight: 2  // Épaisseur des contours du polygon
        }}
    });

    var sf = JSON.parse(document.getElementById('data').getAttribute('sf'));
    couche_sf = L.geoJSON(sf, {
      style: function (feature) {
        return {
          fillColor: "transparent",  // Définir la couleur de remplissage sur "transparent"
          color: "blue",  // Couleur des contours du polygon
          weight: 0.5  // Épaisseur des contours du polygon
        }}
    });

    var pe = JSON.parse(document.getElementById('data').getAttribute('pe'));
    couche_pe = L.geoJSON(pe)

    var pv = JSON.parse(document.getElementById('data').getAttribute('pv'));
    couche_pv = L.geoJSON(pv)

    var tpf = JSON.parse(document.getElementById('data').getAttribute('tpf'));
    couche_tpf = L.geoJSON(tpf)



    // On crée la carte : et par défaut, on ajoute les couches osm et cities
    map = L.map('map', {
        layers: [osm]
    });
    map.setView([34.05, -6.81667], 10);
    //map.zoomControl.setPosition('topright');


    // ------------- Groupage --------
    // Un dictionnaire des fonds de cartes
    var fondsCarto = {'Open Street Map': osm, 'Imagery Satellitaire': esriIMG};
    // Un dictionnaire des couches qui seront disposées au dessus du fond de carte
    var overlayLayers = {
        "Incendies": couche_incendies,
        "Postes vigies": couche_pv,
        "Points d'eau": couche_pe,
        "Tranchées par feu": couche_tpf,
        "Secteurs forestier": couche_sf,
        "CCDRF": couche_ccdrf,
        "Directions provinciales": couche_dp
        };

    // Création du controleur : Affiche un widget contenant les fondsCarto et overlayLayers
    var layerControl = L.control.layers(fondsCarto, overlayLayers, {
        collapsed: false
     }).addTo(map);
});


