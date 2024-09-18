from django.db import models

# Create your models here.

class GoogleUser(models.Model):
    fname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    def __str__(self):
        return str(self.id)
    


class Wilaya(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Daira(models.Model):
    name = models.CharField(max_length=100)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Commune(models.Model):
    name = models.CharField(max_length=100)
    daira = models.ForeignKey(Daira, on_delete=models.CASCADE)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Propriété Site
propriete_site = [
    "AADL", "ACED", "ADA", "ADE", "Aéroport", "Affaires Religieuses", "Algérie Poste", 
    "Algérie Telecom", "APC", "ATM/ Mobilis", "CABAM", "Coloc OTA", "Coloc WTA", 
    "Conservation des forêts", "COSIDER", "Direction de la culture", "DJS", 
    "Domaine", "DOU/ Université", "EPSP", "Exploitation Agricole", "GICA", "MDN", 
    "Naftal", "Privé", "Privé/ A. Commerciale", "Protection Civile", "Rail Telecom", 
    "SCIMAT", "SOGRAL", "TDA", "Université", "Wilaya", "Coloc OOREDO", "ColoC Djezzy"
]

# Type de Banque
type_de_banque = [
    "AGB", "Algérie Poste (CCP)", "ASBA", "B. ABC", "B. EL BARAKA", "BADR", 
    "BDL", "BEA", "BN. HABITAT", "BNA", "BNP PARIS BAS AL DJAZAIR", "CNEP", 
    "CPA", "FRANSABANK EL DJAZAIR", "HBTF", "HSBC", "NATIXIS", "SOCIETE GENERALE", "TBA"
]

# Type de paiement
type_de_paiement = [
    "Virement", "Chèque", "Chash", "Autorisation (MDN)"
]

# Type de contrat
type_de_contrat = [
    "Contrat notarié", "Convention Cadre", "Convention site", "Résilié", "En litige"
]

# État de renouvellement
etat_renouvellement = [
    "En cour", "Renouvelé", "À résilier"
]

class Notaire(models.Model):
    # Fields
    nom_prenom_notaire = models.CharField(max_length=255)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=255)
    num_mobile = models.CharField(max_length=20)
    num_fixe = models.CharField(max_length=20, blank=True, null=True)
    num_fax = models.CharField(max_length=20, blank=True, null=True)
    courriel = models.EmailField()
    banque = models.CharField(max_length=255, choices=[
        ("AGB", "AGB"), ("Algérie Poste (CCP)", "Algérie Poste (CCP)"), ("ASBA", "ASBA"),
        ("B. ABC", "B. ABC"), ("B. EL BARAKA", "B. EL BARAKA"), ("BADR", "BADR"),
        ("BDL", "BDL"), ("BEA", "BEA"), ("BN. HABITAT", "BN. HABITAT"), ("BNA", "BNA"),
        ("BNP PARIS BAS AL DJAZAIR", "BNP PARIS BAS AL DJAZAIR"), ("CNEP", "CNEP"),
        ("CPA", "CPA"), ("FRANSABANK EL DJAZAIR", "FRANSABANK EL DJAZAIR"), ("HBTF", "HBTF"),
        ("HSBC", "HSBC"), ("NATIXIS", "NATIXIS"), ("SOCIETE GENERALE", "SOCIETE GENERALE"),
        ("TBA", "TBA")
    ])
    num_compte = models.CharField(max_length=50, blank=True, null=True)
    autre = models.CharField(max_length=255, blank=True, null=True)
    remarque = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_prenom_notaire} - {self.commune.name}, {self.commune.daira.name}, {self.commune.wilaya.name}"

class Bailleur(models.Model):
    nom_bailleur = models.CharField(max_length=255)
    prenom_bailleur = models.CharField(max_length=255)
    num_mobile = models.CharField(max_length=20)
    num_fixe = models.CharField(max_length=20, blank=True, null=True)
    num_fax = models.CharField(max_length=20, blank=True, null=True)
    courriel = models.EmailField()
    banque = models.CharField(max_length=255, choices=[
        ("AGB", "AGB"), ("Algérie Poste (CCP)", "Algérie Poste (CCP)"), ("ASBA", "ASBA"),
        ("B. ABC", "B. ABC"), ("B. EL BARAKA", "B. EL BARAKA"), ("BADR", "BADR"),
        ("BDL", "BDL"), ("BEA", "BEA"), ("BN. HABITAT", "BN. HABITAT"), ("BNA", "BNA"),
        ("BNP PARIS BAS AL DJAZAIR", "BNP PARIS BAS AL DJAZAIR"), ("CNEP", "CNEP"),
        ("CPA", "CPA"), ("FRANSABANK EL DJAZAIR", "FRANSABANK EL DJAZAIR"), ("HBTF", "HBTF"),
        ("HSBC", "HSBC"), ("NATIXIS", "NATIXIS"), ("SOCIETE GENERALE", "SOCIETE GENERALE"),
        ("TBA", "TBA")
    ])
    num_compte = models.CharField(max_length=50, blank=True, null=True)
    autre = models.CharField(max_length=255, blank=True, null=True)
    remarque = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_bailleur} {self.prenom_bailleur}"

# List of Propriété Site options
PROPRIETE_SITE_CHOICES = [
    ("AADL", "AADL"), ("ACED", "ACED"), ("ADA", "ADA"), ("ADE", "ADE"), ("Aéroport", "Aéroport"),
    ("Affaires Religieuses", "Affaires Religieuses"), ("Algérie Poste", "Algérie Poste"),
    ("Algérie Telecom", "Algérie Telecom"), ("APC", "APC"), ("ATM/ Mobilis", "ATM/ Mobilis"),
    ("CABAM", "CABAM"), ("Coloc OTA", "Coloc OTA"), ("Coloc WTA", "Coloc WTA"),
    ("Conservation des forêts", "Conservation des forêts"), ("COSIDER", "COSIDER"),
    ("Direction de la culture", "Direction de la culture"), ("DJS", "DJS"), ("Domaine", "Domaine"),
    ("DOU/ Université", "DOU/ Université"), ("EPSP", "EPSP"), ("Exploitation Agricole", "Exploitation Agricole"),
    ("GICA", "GICA"), ("MDN", "MDN"), ("Naftal", "Naftal"), ("Privé", "Privé"),
    ("Privé/ A. Commerciale", "Privé/ A. Commerciale"), ("Protection Civile", "Protection Civile"),
    ("Rail Telecom", "Rail Telecom"), ("SCIMAT", "SCIMAT"), ("SOGRAL", "SOGRAL"), ("TDA", "TDA"),
    ("Université", "Université"), ("Wilaya", "Wilaya"), ("Coloc OOREDO", "Coloc OOREDO"),
    ("ColoC Djezzy", "ColoC Djezzy")
]

class Site(models.Model):
    code_site = models.CharField(max_length=100, unique=True)
    nom_site = models.CharField(max_length=255)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    daira = models.ForeignKey(Daira, on_delete=models.CASCADE)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()
    typologie = models.CharField(max_length=255)
    surface_louee = models.FloatField()
    propriete = models.CharField(max_length=255, choices=PROPRIETE_SITE_CHOICES)
    adresse = models.CharField(max_length=255)
    bailleur = models.ForeignKey(Bailleur, on_delete=models.CASCADE)
    remarque = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_site} - {self.commune.name}, {self.commune.daira.name}, {self.commune.wilaya.name}"




class Contrat(models.Model):
    code_site = models.ForeignKey(Site, on_delete=models.CASCADE)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    propriete = models.CharField(max_length=255, choices=PROPRIETE_SITE_CHOICES)
    type_contrat = models.CharField(max_length=255, choices=[
        ("Contrat notarié", "Contrat notarié"),
        ("Convention Cadre", "Convention Cadre"),
        ("Convention site", "Convention site"),
        ("Résilié", "Résilié"),
        ("En litige", "En litige")
    ])
    ref_dernier_contrat = models.CharField(max_length=255,)
    bail_location_annuel = models.FloatField()  # Annual rental lease amount
    notaire = models.ForeignKey(Notaire, on_delete=models.CASCADE)
    date_signature_dernier_contrat = models.DateField()
    duree_bail_dernier_contrat = models.IntegerField()  # in months
    date_fin_contrat = models.DateField()
    duree_restante_avant_expiration = models.CharField(max_length=255,)  # in days
    etat_contrat_actuel = models.CharField(max_length=255, choices=[
        ("Actif", "Actif"),
        ("Expiré", "Expiré"),
        ("Résilié", "Résilié")
    ])
    date_dernier_renouvellement = models.DateField()
    nombre_renouvellement = models.IntegerField()
    etat_renouvellement = models.CharField(max_length=255, choices=[
        ("En cour", "En cour"),
        ("Renouvelé", "Renouvelé"),
        ("À résilier", "À résilier")
    ])
    historique_gestion_renouvellements = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code_site.code_site} - {self.type_contrat} - {self.etat_contrat_actuel}"
