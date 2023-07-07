
// Déclaration des variables
var osm, esriIMG, map, couche_dp, couche_ccdrf, couche_sf, couche_pe, couche_pv, couche_tpf;


// Variable de style lorsu'on survole une couche polygone
var highlightStyle = {
  fillColor: 'blue',
  fillOpacity: 0.5,
  color: 'blue',
};

// Couche sélectionnée sur la carte
var selectedFeature = null;
var coordonnees_clic = null;


var url_detail_ccdrf = "";
var url_detail_sf = "";

// ---------------- Chargement des détails d'incendies --------------
function InfoGlobal () {
    var url_objet = 'http://127.0.0.1:8000/detail_global';

    $.ajax(
        {
            url: url_objet,
            type: 'GET',
            success: function(data) {
                console.log(data);
              $('#details_objet').html(data);
            }
        });
};

function InfoRequest (id_object, object_class) {
    var url_objet = "";
    if (object_class === 'dp') {
        console.log("Direction provinciale : " + id_object);
        var url_objet = `http://127.0.0.1:8000/detail_dp/${id_object}`;
    } else if (object_class === 'ccdrf') {
        console.log("CCDRF : " + id_object);
        var url_objet = `http://127.0.0.1:8000/detail_ccdrf/${id_object}`;
    } else if (object_class === 'sf') {
        console.log("Secteur forestier : " + id_object);
        var url_objet = `http://127.0.0.1:8000/detail_sf/${id_object}`;
    };

    $.ajax(
        {
            url: url_objet,
            type: 'GET',
            success: function(data) {
                console.log(data);
              $('#details_objet').html(data);
            }
        });
};


// Fonction qui modifie le style de l'entité au survole
function modifierStylePolygon(event) {
    var layer = event.target;
    if (selectedFeature) {
        retablirStylePolygon(selectedFeature);
    };
    // Changer le style de la couche survolée
    layer.setStyle(highlightStyle);
    selectedFeature = layer;
};

// Fonction pour gérer l'événement de sortie de la souris
function retablirStylePolygon(couche) {
  var cles = Object.keys(couche.feature.properties)

  // Rétablir le style par défaut de la couche survolée
  if (cles.includes('comment_dp')) {
    couche_dp.resetStyle(couche);
  } else if (cles.includes('comment_ccdrf')) {
    couche_ccdrf.resetStyle(couche);
  } else if (cles.includes('comment_sf')) {
    couche_sf.resetStyle(couche);
  }
};


// Action qui s'exécute quand on clique sur une direction provinciale
function handleDpClick(event) {
    // On fixe les coordonnées de la zone clickée
    coordonnees_clic = event.latlng
    // On modifie le style de la couche
    modifierStylePolygon(event);
    InfoRequest(event.target.feature.id, 'dp');
};

function handleCcdrfClick(event) {
    console.log(event.target.feature.id);
    // On fixe les coordonnées de la zone clickée
    coordonnees_clic = event.latlng
    modifierStylePolygon(event);
    InfoRequest(event.target.feature.id, 'ccdrf');
};


function handleSfClick(event) {
    console.log(event.target.feature.id);
    // On fixe les coordonnées de la zone clickée
    coordonnees_clic = event.latlng
    modifierStylePolygon(event);
    InfoRequest(event.target.feature.id, 'sf');
};


function handleMapClick(event) {
    // On vérifie si le click est en dehors des entités
    if (event.latlng !== coordonnees_clic) {
        console.log("Evènement map");
        couche_dp.resetStyle();
        couche_ccdrf.resetStyle();
        couche_sf.resetStyle();
    };
    InfoGlobal();
};


// Fonction qui initialise la carte
function initialiserCarte (){

    // Tuilage de couches raster
    osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    esriIMG = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    });


    // On crée la carte : et par défaut, on ajoute les couches osm et cities
    map = L.map('map', {
        layers: [osm]
    });
    map.setView([35.45, -5.50], 9);
    map.on('click', handleMapClick);
    //map.zoomControl.setPosition('topright');


    // Récupération des données de mes 7 couches
    var dp = JSON.parse(document.getElementById('data').getAttribute('dp'));
    console.log(dp);
    couche_dp = L.geoJSON(dp, {
      style: function (feature) {
        return {
          fillColor: "transparent",  // Définir la couleur de remplissage sur "transparent"
          color: "blue",  // Couleur des contours du polygon
          weight: 4  // Épaisseur des contours du polygon
        }},
      onEachFeature: function(feature, layer){
            // layer.bindPopup("DPEFLCD : " + feature.id);
            // layer.on('mouseover', modifierStylePolygon);
            // layer.on('mouseout', retablirStylePolygon);
            layer.bindTooltip("DPEFLCD : " + feature.id);
            layer.on('click', handleDpClick);
        }
    }).addTo(map);

    var ccdrf = JSON.parse(document.getElementById('data').getAttribute('ccdrf'));
    couche_ccdrf = L.geoJSON(ccdrf, {
      style: function (feature) {
        return {
          fillColor: "transparent",  // Définir la couleur de remplissage sur "transparent"
          color: "blue",  // Couleur des contours du polygon
          weight: 2  // Épaisseur des contours du polygon
        }},
      onEachFeature: function(feature, layer){
            // layer.bindPopup("CCDRF : " + feature.id);
            // layer.on('mouseover', modifierStylePolygon);
            // layer.on('mouseout', retablirStylePolygon);
            layer.bindTooltip("CCDRF : " + feature.id);
            layer.on('click', handleCcdrfClick);
        }
    });

    var sf = JSON.parse(document.getElementById('data').getAttribute('sf'));
    couche_sf = L.geoJSON(sf, {
      style: function (feature) {
        return {
          fillColor: "transparent",  // Définir la couleur de remplissage sur "transparent"
          color: "blue",  // Couleur des contours du polygon
          weight: 0.5  // Épaisseur des contours du polygon
        }},
      onEachFeature: function(feature, layer){
            // layer.bindPopup("Secteur forestier : " + feature.id);
            // layer.on('mouseover', modifierStylePolygon);
            // layer.on('mouseout', retablirStylePolygon);
            layer.bindTooltip("Secteur forestier : " + feature.id);
            layer.on('click', handleSfClick);
        }
    });

    var pe = JSON.parse(document.getElementById('data').getAttribute('pe'));
    couche_pe = L.geoJSON(pe)

    var pv = JSON.parse(document.getElementById('data').getAttribute('pv'));
    couche_pv = L.geoJSON(pv)

    var tpf = JSON.parse(document.getElementById('data').getAttribute('tpf'));
    couche_tpf = L.geoJSON(tpf)


    // ------------- Groupage --------
    // Un dictionnaire des fonds de cartes
    var fondsCarto = {'Open Street Map': osm, 'Imagery Satellitaire': esriIMG};
    // Un dictionnaire des couches qui seront disposées au dessus du fond de carte
    var overlayLayers = {
        "Postes vigies": couche_pv,
        "Points d'eau": couche_pe,
        "Tranchées par feu": couche_tpf,
        "Secteurs forestier": couche_sf,
        "CCDRF": couche_ccdrf,
        "Directions provinciales": couche_dp
        };

    // Création du controleur : Affiche un widget contenant les fondsCarto et overlayLayers
    var layerControl = L.control.layers(fondsCarto, overlayLayers, {
        collapsed: true
     }).addTo(map);

     // Chargement des détails global
     InfoGlobal()
     };


document.addEventListener('DOMContentLoaded', initialiserCarte);


