from django.contrib.gis.db import models


# Create your models here.
class DirectionProvinciale(models.Model):
    choix = (
        ('CHEFCHAOUEN', 'CHEFCHAOUEN'),
        ('LARACHE', 'LARACHE'),
        ('TANGER', 'TANGER'),
        ('TETOUAN', 'TETOUAN')
    )
    nom_dp = models.CharField(primary_key=True, max_length=80, verbose_name="Nom de la DPEFLCD", choices=choix)
    comment_dp = models.TextField(null=True, blank=True, max_length=500, verbose_name="Description")
    geometry_dp = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.nom_dp


class Ccdrf(models.Model):
    choix = (
        ('ASSILAH', 'ASSILAH'),
        ('BAB BERRED', 'BAB BERRED'),
        ('BEN KARRICH', 'BEN KARRICH'),
        ('BENI AAROUSS', 'BENI AAROUSS'), ('CHECHAOUEN NORD', 'CHECHAOUEN NORD'), ('CHECHAOUEN SUD', 'CHECHAOUEN SUD'),
        ('FAHS-ANJRA', 'FAHS-ANJRA'), ('JEBHA', 'JEBHA'), ('LARACHE', 'LARACHE'), ('MDIQ-TETOUAN', 'MDIQ-TETOUAN'),
        ('MOKRISSET', 'MOKRISSET'), ('TATTOFT', 'TATTOFT')
    )
    # Clé étrangère
    dp_ccdrf = models.ForeignKey(DirectionProvinciale, on_delete=models.CASCADE, verbose_name="Nom de la DPEFLCD", related_name="ccdrf")
    nom_ccdrf = models.CharField(primary_key=True, max_length=80, verbose_name="Nom du CCDRF", choices=choix)
    comment_ccdrf = models.TextField(blank=True, null=True, max_length=500, verbose_name="Description")
    geometry_ccdrf = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.nom_ccdrf


class SecteurForestier(models.Model):
    choix = (
        ('AIN JDIDA', 'AIN JDIDA'), ('BEN KARRICH', 'BEN KARRICH'), ('Bni Hassane', 'Bni Hassane'), ('CAP SPARTEL', 'CAP SPARTEL'),
        ('OUED LAOU', 'OUED LAOU'), ('TORRETA', 'TORRETA'), ('Tamrabta', 'Tamrabta'), ('MELLOUSSA', 'MELLOUSSA'),
        ('BGHAGHZA', 'BGHAGHZA'), ('DAR CHAOUI', 'DAR CHAOUI'), ('HARCHA', 'HARCHA'), ('Oued Raouze', 'Oued Raouze'),
        ('GHABA LARACHE', 'GHABA LARACHE'), ('Koudiat Tayfor', 'Koudiat Tayfor'), ('Machrah', 'Machrah'),
        ('Rouaousa', 'Rouaousa'), ('GHABA KHALIFA', 'GHABA KHALIFA'), ('TATTOFT', 'TATTOFT'), ('El Ghorraf', 'El Ghorraf'),
        ('BOUHACHEM', 'BOUHACHEM'), ('TAZIA', 'TAZIA'), ('TAGHRAMT', 'TAGHRAMT'), ('RESTINGA', 'RESTINGA'),
        ('KRIMDA', 'KRIMDA'), ('ASSILAH', 'ASSILAH'), ('NOUADER', 'NOUADER')
    )
    # clé étrangère
    ccdrf = models.ForeignKey(Ccdrf, on_delete=models.CASCADE, verbose_name="Nom du CCDRF", related_name="secteurs")

    nom_sf = models.CharField(primary_key=True, max_length=80, verbose_name="Nom du Secteur forestier", choices=choix)
    comment_sf = models.TextField(blank=True, null=True, max_length=500, verbose_name="Description")
    geometrie_sf = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.nom_sf


class Incendie(models.Model):
    # Clé étrangère
    dp_icd = models.ForeignKey(DirectionProvinciale, on_delete=models.CASCADE, verbose_name="Nom de la DPEFLCD", related_name="incendies")

    id_incendie = models.BigAutoField(primary_key=True)
    date_eclosion = models.DateField(verbose_name="Date d'éclosion", null=True, blank=True)
    date_arret = models.DateField(verbose_name="Date d'arrêt", null=True, blank=True)
    cause_incendie = models.CharField(verbose_name="Cause", choices=(("INCONNUE", "INCONNUE"), ("HUMAINE", "HUMAINE"),
                                                                     ("NATURELLE", "NATURELLE")), max_length=80)
    surface_brulee = models.FloatField(verbose_name="Surface brûlée", null=True, blank=True)
    cout_financier = models.FloatField(verbose_name="Coût financier (Dhs)", null=True, blank=True)
    comment_incendie = models.TextField(blank=True, null=True, max_length=500, verbose_name="Commentaire")
    geometrie_incendie = models.MultiPointField(srid=4326)

    def __str__(self):
        return "Incendie " + str(self.id_incendie) + " - " + str(self.dp_icd)


class PointEau(models.Model):
    # Clé étrangère
    dp_pe = models.ForeignKey(DirectionProvinciale, on_delete=models.CASCADE, verbose_name="Nom de la DPEFLCD", related_name="points_eaux")

    id_pe = models.BigAutoField(primary_key=True)
    nom_pe = models.CharField(verbose_name="Lieu", max_length=50, null=True, blank=True)
    date_creation_pe = models.DateField(verbose_name="Date de création", null=True, blank=True)
    altitude_pe = models.FloatField(verbose_name="Altitude", null=True, blank=True)
    capacite_eau = models.FloatField(verbose_name="Capacité en eau", null=True, blank=True)
    etat_pe = models.CharField(verbose_name="Etat", choices=(("FONCTIONNEL", "FONCTIONNEL"),
                                                             ("NON FONCTIONNEL", "NON FONCTIONNEL")), max_length=80)
    geometrie_pe = models.MultiPointField(srid=4326)

    def __str__(self):
        return "Point d'eau " + str(self.id_pe) + " à " + str(self.nom_pe)


class PosteVigie(models.Model):
    # Clé étrangère
    dp_pv = models.ForeignKey(DirectionProvinciale, on_delete=models.CASCADE, verbose_name="Nom de la DPEFLCD", related_name="postes_vigies")

    id_pv = models.BigAutoField(primary_key=True)
    nom_pv = models.CharField(verbose_name="Lieu", max_length=50, null=True, blank=True)
    date_creation_pv = models.DateField(verbose_name="Date de création", null=True, blank=True)
    altitude_pv = models.FloatField(verbose_name="Altitude", null=True, blank=True)
    etat_pe = models.CharField(verbose_name="Etat", choices=(("FONCTIONNEL", "FONCTIONNEL"),
                                                             ("NON FONCTIONNEL", "NON FONCTIONNEL")), max_length=80)
    geometrie_pv = models.MultiPointField(srid=4326)

    def __str__(self):
        return  "Poste vigie " + str(self.id_pv) + " à " + str(self.nom_pv)


class TracheeParFeu(models.Model):
    # Clé étrangère
    dp_tpf = models.ForeignKey(DirectionProvinciale, on_delete=models.CASCADE, verbose_name="Nom de la DPEFLCD", related_name="tpf")

    id_tpf = models.BigAutoField(primary_key=True)
    etat_tpf = models.CharField(verbose_name="Etat", choices=(("BON", "BON"), ("MOYEN", "MOYEN"),
                                                              ("MAUVAIS", "MAUVAIS")), max_length=80)
    largeur_tpf = models.IntegerField(verbose_name="Largeur", null=True, blank=True)
    geometrie_tpf = models.MultiLineStringField(srid=4326)

    def __str__(self):
        return "TPF " + str(self.id_tpf) + " - " + str(self.dp_tpf)


"""class PisteForestiere(models.Model):
    # Clé étrangère
    dp_tpf = models.ForeignKey(DirectionProvinciale, on_delete=models.CASCADE, verbose_name="Nom de la DPEFLCD")

    id_pf = models.BigAutoField(primary_key=True)
    comment_pf = models.TextField(blank=True, null=True, max_length=500, verbose_name="Commentaire")
    etat_pf = models.CharField(verbose_name="Etat", choices=["BON", "MOYEN", "MAUVAIS"], max_length=80)
    largeur_pf = models.IntegerField(verbose_name="Largeur", null=True, blank=True, max_length=80)
    geometrie_pe = models.MultiLineStringField(srid=4326)"""