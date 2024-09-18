from django.shortcuts import render, get_object_or_404, redirect
from .forms import LocationForm
from django.http import JsonResponse
from django.urls import reverse
from .models import Site, Commune, Daira, Wilaya, Bailleur,Contrat,Notaire
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import random

def create_contrat_instances():
    sites = Site.objects.all()  # Assuming you have some sites available
    notaires = Notaire.objects.all()  # Assuming you have some notaires available
    instances = []

    for i in range(20):  # Adjust to create exactly 20 instances
        site = sites[i % len(sites)]  # Rotating through available sites
        notaire = notaires[i % len(notaires)]  # Rotating through available notaires

        duree_bail = i % 10 + 1  # Random duration in years for the bail
        date_signature = date(2015 + i % 8, 1 + i % 12, 1 + i % 28)
        date_fin = date_signature + relativedelta(years=duree_bail)

        duree_restante = relativedelta(date_fin, timezone.now().date())
        duree_restante_avant_expiration = f"{duree_restante.years} Years, {duree_restante.months} Months, {duree_restante.days} Days"

        if duree_restante.years > 1:
            etat_contrat = "Actif"
        elif duree_restante.years == 1:
            etat_contrat = "Actif"
        elif duree_restante.years == 0:
            etat_contrat = "Reste moins d'une année"
        else:
            etat_contrat = "Expiré"

        date_dernier_renouvellement = date_fin - relativedelta(years=i % 3)
        difference_renouvellement = relativedelta(date_fin, date_dernier_renouvellement)

        if duree_restante.years < 0 and (i % 5 == 0 or site.typologie == 'En litige'):
            etat_renouvellement = "À résilier"
            etat_contrat = "Résilié"
        elif difference_renouvellement.years < 1:
            etat_renouvellement = "Renouvelé"
        elif difference_renouvellement.years >= 1:
            etat_renouvellement = "En cour"
        else:
            etat_renouvellement = "En cour"

        contrat = Contrat(
            code_site=site,
            wilaya=site.wilaya,
            propriete=site.propriete,
            type_contrat="Contrat notarié" if i % 2 == 0 else "Convention Cadre",
            ref_dernier_contrat=f"REF-{1000 + i}",
            bail_location_annuel=100000 + i * 5000,
            notaire=notaire,
            date_signature_dernier_contrat=date_signature,
            duree_bail_dernier_contrat=duree_bail,  # in years
            date_fin_contrat=date_fin,
            duree_restante_avant_expiration=duree_restante_avant_expiration,
            etat_contrat_actuel=etat_contrat,
            date_dernier_renouvellement=date_dernier_renouvellement,
            nombre_renouvellement=i % 4,
            etat_renouvellement=etat_renouvellement,
            historique_gestion_renouvellements="Historique"
        )

        instances.append(contrat)

    Contrat.objects.bulk_create(instances)

def home(request):

    return render(request, 'home.html')

def q(request): #unimportant
    return render(request, 'tester2.html')

def location_view(request):
    # form = LocationForm()
    # locations = Commune.objects.all()

    # # Print each Location instance
    # for location in locations:
    #     print(f"Commune: {location.name}, Daira: {location.daira}, Wilaya: {location.wilaya}")

    # from .models import Commune, Notaire
    # import random

    # # List of communes and corresponding dairas and wilayas
    # communes = [
    #     {"commune": "AHMED RACHEDI", "daira": "OUED ENDJA", "wilaya": "MILA"},
    #     {"commune": "AIN ABID", "daira": "AIN ABID", "wilaya": "CONSTANTINE"},
    #     {"commune": "AIN BABOUCHE", "daira": "AIN BABOUCHE", "wilaya": "OUM EL BOUAGHI"},
    #     {"commune": "AIN BEIDA", "daira": "AIN BEIDA", "wilaya": "OUM EL BOUAGHI"},
    #     {"commune": "AIN BEIDA HARRICHE", "daira": "AIN BEIDA HARRICHE", "wilaya": "MILA"},
    #     {"commune": "AIN DISS", "daira": "AIN BABOUCHE", "wilaya": "OUM EL BOUAGHI"},
    #     {"commune": "AIN DJASSER", "daira": "AIN DJASSER", "wilaya": "BATNA"},
    #     {"commune": "AIN FEKROUN", "daira": "AIN FEKROUN", "wilaya": "OUM EL BOUAGHI"},
    #     {"commune": "AIN KERCHA", "daira": "AIN KERCHA", "wilaya": "OUM EL BOUAGHI"},
    #     {"commune": "AIN MELLOUK", "daira": "CHELGHOUM LAID", "wilaya": "MILA"},
    #     {"commune": "AIN M'LILA", "daira": "AIN M'LILA", "wilaya": "OUM EL BOUAGHI"},
    #     {"commune": "AIN SMARA", "daira": "EL KHROUB", "wilaya": "CONSTANTINE"},
    #     {"commune": "AIN TINE", "daira": "MILA", "wilaya": "MILA"},
    #     {"commune": "AIN TOUILA", "daira": "AIN TOUILA", "wilaya": "KHENCHELA"},
    #     {"commune": "AIN TOUTA", "daira": "AIN TOUTA", "wilaya": "BATNA"},
    #     {"commune": "AIN YAGOUT", "daira": "EL MADHER", "wilaya": "BATNA"},
    #     {"commune": "AIN ZITOUN", "daira": "OUM EL BOUAGHI", "wilaya": "OUM EL BOUAGHI"},
    #     {"commune": "AMIRA ARRES", "daira": "TERRAI BAINEN", "wilaya": "MILA"},
    #     {"commune": "ARRIS", "daira": "ARRIS", "wilaya": "BATNA"},
    #     {"commune": "AZIL ABEDELKADER", "daira": "DJEZZAR", "wilaya": "BATNA"}
    # ]

    # # Randomly generated names for notaires
    # notaire_names = [
    #     "Ahmed Rachedi", "Amina Ben", "Mohamed Salah", "Karim Boumediene", "Fatima Zohra",
    #     "Abdelkader Ali", "Rachida Boudiaf", "Mourad Meziane", "Samira Lalami", "Yacine Amrani",
    #     "Meriem Sidi", "Noureddine Salah", "Hana Saadi", "Walid Cherif", "Rym Benkacem",
    #     "Sofiane Lamari", "Hind Dahmani", "Reda Boukhalfa", "Nadia Cheb", "Adel Hamdi"
    # ]

    # # Randomly generated phone numbers
    # def generate_phone_number():
    #     return f"07{random.randint(10000000, 99999999)}"

    # # Randomly generated email addresses
    # def generate_email(name):
    #     return f"{name.replace(' ', '').lower()}@example.com"

    # # Create 20 instances of Notaire
    # for name in notaire_names:
    #     commune_info = random.choice(communes)
    #     commune_instance = Commune.objects.get(name=commune_info['commune'])
        
    #     notaire = Notaire(
    #         nom_prenom_notaire=name,
    #         commune=commune_instance,
    #         adresse=f"Adresse de {name}",
    #         num_mobile=generate_phone_number(),
    #         num_fixe=generate_phone_number(),
    #         num_fax=generate_phone_number(),
    #         courriel=generate_email(name),
    #         banque="BNA",  # Randomly chosen from the bank list
    #         num_compte=f"12345678{random.randint(1000, 9999)}",
    #         autre="Autre information",
    #         remarque="Remarque sur le notaire"
    #     )
    #     notaire.save()

    # print("20 instances of Notaire have been created.")


    return render(request, 'testing.html', )

def get_location_details(request):   #idk tbh
    commune_id = request.GET.get('commune_id')
    commune = Commune.objects.get(id=commune_id)
    data = {
        'daira': commune.daira.name,
        'wilaya': commune.wilaya.name,
    }
    return JsonResponse(data)

def instance_generator(request): #dump
    
    # bailleur_names = [
    #     ("Khaled", "Benabdelkader"), ("Nadia", "Mouhoub"), ("Ahmed", "Cherif"), ("Fatima Zahra", "Ait Ahmed"), ("Mohamed", "Benaissa"),
    #     ("Amina", "Lounis"), ("Hichem", "Boudiaf"), ("Nadia", "Khelifi"), ("Ali", "Belkacem"), ("Samira", "Saad"),
    #     ("Rachid", "Rahmani"), ("Zina", "Benali"), ("Hassan", "Boukhalfa"), ("Meriem", "Khalfa"), ("Sofiane", "Bouaziz"),
    #     ("Huda", "Benmohamed"), ("Farid", "Tlemcani"), ("Kheira", "Djenane"), ("Adel", "Boumerdassi"), ("Yassir", "Hariri")
    # ]

    # # Randomly generated phone numbers
    # def generate_phone_number():
    #     return f"07{random.randint(10000000, 99999999)}"

    # # Randomly generated email addresses
    # def generate_email(first_name, last_name):
    #     return f"{first_name.lower()}.{last_name.lower()}@example.com"

    # # List of bank names
    # banks = [
    #     "AGB", "Algérie Poste (CCP)", "ASBA", "B. ABC", "B. EL BARAKA", "BADR",
    #     "BDL", "BEA", "BN. HABITAT", "BNA", "BNP PARIS BAS AL DJAZAIR", "CNEP",
    #     "CPA", "FRANSABANK EL DJAZAIR", "HBTF", "HSBC", "NATIXIS", "SOCIETE GENERALE", "TBA"
    # ]

    # # Create 20 instances of Bailleur
    # for first_name, last_name in bailleur_names:

        
    #     bailleur = Bailleur(
    #         nom_bailleur=last_name,
    #         prenom_bailleur=first_name,
    #         num_mobile=generate_phone_number(),
    #         num_fixe=generate_phone_number(),
    #         num_fax=generate_phone_number(),
    #         courriel=generate_email(first_name, last_name),
    #         banque=random.choice(banks),  # Randomly chosen from the bank list
    #         num_compte=f"98765432{random.randint(1000, 9999)}",
    #         autre="Autre information",
    #         remarque="Remarque sur le bailleur"
    #     )
    #     bailleur.save()

    # import random
    # from django.utils import timezone
    # from .models import Commune, Daira, Wilaya, Bailleur, Site

    # # List of random site names
    # site_names = [
    #     "Centre Commercial El Mahdi", "Parc d'Attractions El-Djazair", "Complexe Sportif Al-Mustapha",
    #     "Zone Industrielle Khemis", "Centre Médical El-Khalifa", "Aire de Loisirs Birkhadem",
    #     "Hôtel Le Majestic", "Centre Culturel El-Hadj", "Université Al-Andalus", "Centre d'Affaires El-Sherif",
    #     "Palais des Congrès El-Senhadja", "Complexe Résidentiel El-Mina", "École Supérieure El-Attef",
    #     "Parc Technologique El-Mihoub", "Institut de Recherche Al-Kenitra", "Centre d'Études Al-Falah",
    #     "Hôpital Universitaire El-Guerrara", "Complexe Touristique El-Falah", "Centre Commercial El-Mahfoud",
    #     "Parc de Loisirs El-Safina"
    # ]

    # # List of typologies
    # typologies = ["pylone", "mat", "micro-bts", "multi-mats"]

    # # List of propriete_site values
    # propriete_site = [
    #     "AADL", "ACED", "ADA", "ADE", "Aéroport", "Affaires Religieuses", "Algérie Poste", 
    #     "Algérie Telecom", "APC", "ATM/ Mobilis", "CABAM", "Coloc OTA", "Coloc WTA", 
    #     "Conservation des forêts", "COSIDER", "Direction de la culture", "DJS", 
    #     "Domaine", "DOU/ Université", "EPSP", "Exploitation Agricole", "GICA", "MDN", 
    #     "Naftal", "Privé", "Privé/ A. Commerciale", "Protection Civile", "Rail Telecom", 
    #     "SCIMAT", "SOGRAL", "TDA", "Université", "Wilaya", "Coloc OOREDO", "ColoC Djezzy"
    # ]

    # # List of Wilaya codes
    # wilaya_codes = {
    #     'OUM EL BOUAGHI': '04',
    #     'MILA': '43',
    #     'BATNA': '05',
    #     'KHENCHELA': '40',
    #     'CONSTANTINE': '25'
    # }

    # # Randomly generate longitude and latitude
    # def generate_coordinates():
    #     return round(random.uniform(5, 8), 6), round(random.uniform(35,37), 6)

    # # Create 20 instances of Site
    # for _ in range(20):
    #     # Pick a random Commune
    #     commune = Commune.objects.order_by('?').first()
        
    #     # Determine the wilaya and the site code prefix
    #     wilaya = commune.wilaya.name
    #     site_code_prefix = wilaya_codes.get(wilaya, '00')
        
    #     # Generate a unique site code
    #     site_code = f"{site_code_prefix}{random.randint(1000, 9999)}"
        
    #     # Pick a random bailleur
    #     bailleur = Bailleur.objects.order_by('?').first()
        
    #     # Generate random longitude and latitude
    #     longitude, latitude = generate_coordinates()
        
    #     site = Site(
    #         code_site=site_code,
    #         nom_site=random.choice(site_names),
    #         commune=commune,
    #         daira=commune.daira,
    #         wilaya=commune.wilaya,
    #         longitude=longitude,
    #         latitude=latitude,
    #         typologie=random.choice(typologies),
    #         surface_louee=random.uniform(100.0, 1000.0),
    #         propriete=random.choice(propriete_site),
    #         adresse=f"Adresse de {random.choice(site_names)}",
    #         bailleur=bailleur,
    #         remarque="Remarque sur le site"
    #     )
    #     site.save()

    return render(request, 'te.html')

### SITES ###

def sites(request):           #displays sites list
    sites = Site.objects.all()
    return render(request, 'sites/sites.html', {'sites': sites})

def site_search(request):          #filtering logic for sites
    search_query = request.GET.get('search_query', '').strip()
    filter_by = request.GET.get('filter_by', 'nom_site')
    print(search_query)
    print(filter_by)
    
    if search_query:
        if filter_by == 'nom_site':
            sites = Site.objects.filter(nom_site__icontains=search_query)
        elif filter_by == 'code_site':
            sites = Site.objects.filter(code_site__icontains=search_query)
        elif filter_by == 'adresse':
            sites = Site.objects.filter(adresse__icontains=search_query)
        elif filter_by == 'commune':
            sites = Site.objects.filter(commune__name__icontains=search_query)
        elif filter_by == 'daira':
            sites = Site.objects.filter(daira__name__icontains=search_query)
        elif filter_by == 'wilaya':
            sites = Site.objects.filter(wilaya__name__icontains=search_query)
        elif filter_by == 'typologie':
            sites = Site.objects.filter(typologie__icontains=search_query)
        elif filter_by == 'propriete':
            sites = Site.objects.filter(propriete__icontains=search_query)
        elif filter_by == 'bailleur':
            sites = Site.objects.filter(bailleur__nom_bailleur__icontains=search_query)
        else:
            sites = Site.objects.all()
    else:
        sites = Site.objects.all()
    
    return render(request, 'sites/sites.html', {'sites': sites, 'search_query': search_query, 'filter_by': filter_by})

def site_detail(request, id):          #displays site profile
    site = get_object_or_404(Site, id=id)
    return render(request, 'sites/siteprofile2.html', {'site': site})

def create_site(request):            #actiavtes site creation button
    if request.method == 'POST':
        code_site = request.POST.get('code_site')
        nom_site = request.POST.get('nom_site')
        commune_id = request.POST.get('commune')
        daira_id = request.POST.get('daira')
        wilaya_id = request.POST.get('wilaya')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        typologie = request.POST.get('typologie')
        surface_louee = request.POST.get('surface_louee')
        propriete = request.POST.get('propriete')
        adresse = request.POST.get('adresse')
        bailleur_id = request.POST.get('bailleur')
        remarque = request.POST.get('remarque')

        # Fetch related objects
        commune = get_object_or_404(Commune, id=commune_id)
        daira = get_object_or_404(Daira, id=daira_id)
        wilaya = get_object_or_404(Wilaya, id=wilaya_id)
        bailleur = get_object_or_404(Bailleur, id=bailleur_id)

        # Create a new Site instance
        Site.objects.create(
            code_site=code_site,
            nom_site=nom_site,
            commune=commune,
            daira=daira,
            wilaya=wilaya,
            longitude=longitude,
            latitude=latitude,
            typologie=typologie,
            surface_louee=surface_louee,
            propriete=propriete,
            adresse=adresse,
            bailleur=bailleur,
            remarque=remarque
        )

    # Fetch necessary data for the form
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()
    sites = Site.objects.all()


    return render(request, 'sites/sites.html', {
        'sites': sites,

    })

def mod_site(request,id):           #opens modification page
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()
    site = get_object_or_404(Site, id=id)

    return render(request, 'sites/sitemodifyprofile.html', {'communes': communes,'dairas': dairas,'wilayas': wilayas,'bailleurs': bailleurs,'site':site})

def update_site(request, id):          #activates modifying button
    site = get_object_or_404(Site, id=id)

    if request.method == 'POST':
        code_site = request.POST.get('code_site')
        nom_site = request.POST.get('nom_site')
        commune_id = request.POST.get('commune')
        daira_id = request.POST.get('daira')
        wilaya_id = request.POST.get('wilaya')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        typologie = request.POST.get('typologie')
        surface_louee = request.POST.get('surface_louee')
        propriete = request.POST.get('propriete')
        adresse = request.POST.get('adresse')
        bailleur_id = request.POST.get('bailleur')
        remarque = request.POST.get('remarque')

        # Fetch related objects
        commune = get_object_or_404(Commune, id=commune_id)
        daira = get_object_or_404(Daira, id=daira_id)
        wilaya = get_object_or_404(Wilaya, id=wilaya_id)
        bailleur = get_object_or_404(Bailleur, id=bailleur_id)

        # Update the existing Site instance
        site.code_site = code_site
        site.nom_site = nom_site
        site.commune = commune
        site.daira = daira
        site.wilaya = wilaya
        site.longitude = longitude
        site.latitude = latitude
        site.typologie = typologie
        site.surface_louee = surface_louee
        site.propriete = propriete
        site.adresse = adresse
        site.bailleur = bailleur
        site.remarque = remarque
        site.save()

        # Redirect to a success page or the updated site detail page
        return redirect(reverse('site_detail', args=[site.id]))

    # Fetch necessary data for the form
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()

    return render(request, 'siteprofile2.html', {
        'communes': communes,
        'dairas': dairas,
        'wilayas': wilayas,
        'bailleurs': bailleurs,
        'site': site,
    })

def delete_site(request, site_id):                 #activates site delete button
    site = get_object_or_404(Site, id=site_id)
    site.delete()
    return redirect(reverse('sitess'))

def setnprofile(request):                  #Contains new profile page
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()

    return render(request, 'sites/sitenewprofile.html', {'communes': communes,'dairas': dairas,'wilayas': wilayas,'bailleurs': bailleurs,})

### NOTAIRES ###

def notaires(request):
    notaires = Notaire.objects.all()
    return render(request, 'notaires/notaires.html', {'notaires': notaires})

def notaire_detail(request, id): #notaires profile displayer
    notaire = get_object_or_404(Notaire, id=id)
    return render(request, 'notaires/notaire_detail.html', {'notaire': notaire})

def newnotaire(request):  #this one is resposible for creating the new notaires
    communes = Commune.objects.all()
    
    return render(request, 'notaires/newnotaire.html', {'communes': communes})

def create_notaire(request):        #notaire creation form button
    if request.method == 'POST':
        nom_prenom_notaire = request.POST.get('nom_prenom_notaire')
        commune_id = request.POST.get('commune')
        adresse = request.POST.get('adresse')
        num_mobile = request.POST.get('num_mobile')
        num_fixe = request.POST.get('num_fixe')
        num_fax = request.POST.get('num_fax')
        courriel = request.POST.get('courriel')
        banque = request.POST.get('banque')
        num_compte = request.POST.get('num_compte')
        autre = request.POST.get('autre')
        remarque = request.POST.get('remarque')

        commune = Commune.objects.get(id=commune_id)
        print(remarque)
        print(nom_prenom_notaire)

        Notaire.objects.create(
            nom_prenom_notaire=nom_prenom_notaire,
            commune=commune,
            adresse=adresse,
            num_mobile=num_mobile,
            num_fixe=num_fixe,
            num_fax=num_fax,
            courriel=courriel,
            banque=banque,
            num_compte=num_compte,
            autre=autre,
            remarque=remarque
        )
  
    notaires = Notaire.objects.all()
    communes = Commune.objects.all()
    for notaire in notaires:
        print(f"ID: {notaire.id}")
        print(f"Nom et Prénom: {notaire.nom_prenom_notaire}")
        print(f"Commune: {notaire.commune.name}")
        print(f"Daira: {notaire.commune.daira.name}")
        print(f"Wilaya: {notaire.commune.daira.wilaya.name}")
        print(f"Adresse: {notaire.adresse}")
        print(f"Numéro Mobile: {notaire.num_mobile}")
        print(f"Numéro Fixe: {notaire.num_fixe}")
        print(f"Numéro Fax: {notaire.num_fax}")
        print(f"Courriel: {notaire.courriel}")
        print(f"Banque: {notaire.banque}")
        print(f"Numéro de Compte: {notaire.num_compte}")
        print(f"Autre: {notaire.autre}")
        print(f"Remarque: {notaire.remarque}")
        print("-" * 40)
    return render(request, 'notaires/notaires.html', {'communes': communes,'notaires': notaires})

def notaire_search(request): #notaire filtering logic
    search_query = request.GET.get('search_query', '').strip()
    filter_by = request.GET.get('filter_by', 'name')
    
    if search_query:
        if filter_by == 'name':
            notaires = Notaire.objects.filter(nom_prenom_notaire__icontains=search_query)
        elif filter_by == 'num_fixe':
            notaires = Notaire.objects.filter(num_fixe__icontains=search_query)
        elif filter_by == 'courriel':
            notaires = Notaire.objects.filter(courriel__icontains=search_query)
        else:
            notaires = Notaire.objects.all()
    else:
        notaires = Notaire.objects.all()
    
    return render(request, 'notaires/notaires.html', {'notaires': notaires, 'search_query': search_query, 'filter_by': filter_by})

### CONTRATS ###

def contrats(request):
    contrats = Contrat.objects.all()
    notaires = Notaire.objects.all()
    return render(request, 'contrats/contrats.html', {'contrats': contrats,"notaires":notaires})

def contrat_search(request):
    search_query = request.GET.get('search_query', '').strip()
    filter_by = request.GET.get('filter_by', 'ref_dernier_contrat')
    print(search_query)
    print(filter_by)
    
    if search_query:
        if filter_by == 'ref_dernier_contrat':
            contrats = Contrat.objects.filter(ref_dernier_contrat__icontains=search_query)
        elif filter_by == 'code_site':
            contrats = Contrat.objects.filter(code_site__code_site__icontains=search_query)
        elif filter_by == 'wilaya':
            contrats = Contrat.objects.filter(wilaya__name__icontains=search_query)
        elif filter_by == 'propriete':
            contrats = Contrat.objects.filter(propriete__icontains=search_query)
        elif filter_by == 'notaire':
            contrats = Contrat.objects.filter(notaire__nom_notaire__icontains=search_query)
        elif filter_by == 'etat_contrat_actuel':
            contrats = Contrat.objects.filter(etat_contrat_actuel__icontains=search_query)
        elif filter_by == 'duree_bail_dernier_contrat__gt':
            try:
                contrats = Contrat.objects.filter(duree_bail_dernier_contrat__gt=int(search_query))
            except ValueError:
                contrats = Contrat.objects.none()
        elif filter_by == 'duree_bail_dernier_contrat__lt':
            try:
                contrats = Contrat.objects.filter(duree_bail_dernier_contrat__lt=int(search_query))
            except ValueError:
                contrats = Contrat.objects.none()
        elif filter_by == 'bail_location_annuel__gt':
            try:
                contrats = Contrat.objects.filter(bail_location_annuel__gt=float(search_query))
            except ValueError:
                contrats = Contrat.objects.none()
        elif filter_by == 'bail_location_annuel__lt':
            try:
                contrats = Contrat.objects.filter(bail_location_annuel__lt=float(search_query))
            except ValueError:
                contrats = Contrat.objects.none()
        elif filter_by == 'etat_renouvellement':
            contrats = Contrat.objects.filter(etat_renouvellement__icontains=search_query)
        else:
            contrats = Contrat.objects.all()
    else:
        contrats = Contrat.objects.all()

    return render(request, 'contrats/contrats.html', {'contrats': contrats, 'search_query': search_query, 'filter_by': filter_by})

def contrat_detail(request, id):          #displays contrat profile
    contrat = get_object_or_404(Contrat, id=id)
    return render(request, 'contrats/contratprofile.html', {'contrat': contrat})

def renew_contract(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    
    # Logic to extend the contract by 1 year
    contrat.nombre_renouvellement += 1
    contrat.etat_renouvellement = "Renouvelé" 
    contrat.duree_bail_dernier_contrat += 1
    contrat.date_dernier_renouvellement   = timezone.now()  
    contrat.save()

    return redirect(reverse('contrat_detail', args=[contrat_id]))

def contrat_new(request):          #displays contrat profile
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()

    
    return render(request, 'contrats/contratnewprofile.html',{'communes': communes,'dairas': dairas,'wilayas': wilayas,'bailleurs': bailleurs,} )


def contratmod(request,id):           #opens modification page
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()
    site = get_object_or_404(Contrat, id=id)

    return render(request, 'contrats/contratmodify.html', {'communes': communes,'dairas': dairas,'wilayas': wilayas,'bailleurs': bailleurs,'contrat':site})



def calculate_statistics(request):
    # Initialize the statistics dictionary
    stats = {}
    wilayas = Wilaya.objects.all()

    for wilaya in wilayas:
        # Get the number of physical sites in the wilaya
        num_sites = Site.objects.filter(commune__wilaya=wilaya).count()

        # Get the number of contracts in the wilaya
        contrats = Contrat.objects.filter(wilaya=wilaya)
        num_contrats = contrats.count()
        num_contrats_actifs = contrats.filter(etat_contrat_actuel='Actif').count()
        num_contrats_une_annee_et_moins = contrats.filter(date_fin_contrat__lte=timezone.now() + timedelta(days=365)).count()
        num_contrats_expired = contrats.filter(etat_contrat_actuel='Expiré').count()
        num_contrats_en_cours_de_negociation = contrats.filter(etat_renouvellement='En cour').count()
        num_contrats_renouveles = contrats.filter(etat_renouvellement='Renouvelé').count()
        num_contrats_en_litiges = contrats.filter(type_contrat='En litige').count()
        num_contrats_a_resilier = contrats.filter(etat_renouvellement='À résilier').count()
        num_contrats_resilies = contrats.filter(etat_contrat_actuel='Résilié').count()

        # Store the statistics in the dictionary
        stats[wilaya.name] = {
            'nbr_sites_physiques': num_sites,
            'nbr_contrats': num_contrats,
            'gap_nbr_sites_nbr_contrats': num_sites - num_contrats,
            'nbr_contrats_actifs': num_contrats_actifs,
            'nbr_contrats_une_annee_et_moins': num_contrats_une_annee_et_moins,
            'nbr_contrats_expired': num_contrats_expired,
            'nbr_contrats_en_cours_de_negociation_de_renouvellement': num_contrats_en_cours_de_negociation,
            'nbr_contrats_renouveles': num_contrats_renouveles,
            'nbr_contrats_en_litiges': num_contrats_en_litiges,
            'nbr_contrats_a_resilier': num_contrats_a_resilier,
            'nbr_contrats_resilies': num_contrats_resilies,
        }

    # Render the statistics to a template
    return render(request, 'statistics.html', {'stats': stats})



#you'll need a notaire detail,modify and delete + contract add + bailleur add

def mod_notaire(request,id):           #opens modification page
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()
    notaire = get_object_or_404(Notaire, id=id)

    return render(request, 'notaires/notairemodify.html', {'communes': communes,'dairas': dairas,'wilayas': wilayas,'bailleurs': bailleurs,'notaire':notaire})


def update_notaire (request, id):          #activates modifying button
    notaire = get_object_or_404(Notaire, id=id)

    if request.method == 'POST':
        # Retrieve form data
        nom_prenom_notaire = request.POST.get('nom_prenom_notaire')
        commune_id = request.POST.get('commune')
        adresse = request.POST.get('adresse')
        num_mobile = request.POST.get('num_mobile')
        num_fixe = request.POST.get('num_fixe')
        num_fax = request.POST.get('num_fax')
        courriel = request.POST.get('courriel')
        banque = request.POST.get('banque')
        num_compte = request.POST.get('num_compte')
        remarque = request.POST.get('remarque')

        # Fetch related objects
        commune = get_object_or_404(Commune, id=commune_id)
        


        # Update the existing Notaire instance
        notaire.nom_prenom_notaire = nom_prenom_notaire
        notaire.commune = commune
        notaire.adresse = adresse
        notaire.num_mobile = num_mobile
        notaire.num_fixe = num_fixe
        notaire.num_fax = num_fax
        notaire.courriel = courriel
        notaire.banque = banque
        notaire.num_compte = num_compte
        notaire.remarque = remarque
        notaire.save()

        # Redirect to a success page or the updated site detail page
        return redirect(reverse('notaire_detail', args=[notaire.id]))
    
def delete_notaire(request, not_id):                 #activates site delete button
    notaire = get_object_or_404(Notaire, id=not_id)
    notaire.delete()
    return redirect(reverse('notaires'))

def contnprofile(request):                  #Contains new profile page
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()
    notaires = Notaire.objects.all()
    sites = Site.objects.all()


    return render(request, 'contrats/contratnewprofile.html', {'communes': communes,'dairas': dairas,'wilayas': wilayas,'bailleurs': bailleurs,'notaires':notaires,'sites':sites})


def create_contrat(request):
    if request.method == 'POST':
        code_site_id = request.POST.get('code_site')
        wilaya_id = request.POST.get('wilaya')
        propriete = request.POST.get('propriete')
        type_contrat = request.POST.get('type_contrat')
        ref_dernier_contrat = request.POST.get('ref_dernier_contrat')
        bail_location_annuel = request.POST.get('bail_location_annuel')
        notaire_id = request.POST.get('notaire')
        date_signature_dernier_contrat = request.POST.get('date_signature_dernier_contrat')
        duree_bail_dernier_contrat = request.POST.get('duree_bail_dernier_contrat')
        date_fin_contrat = request.POST.get('date_fin_contrat')
        duree_restante_avant_expiration = request.POST.get('duree_restante_avant_expiration')
        etat_contrat_actuel = request.POST.get('etat_contrat_actuel')
        date_dernier_renouvellement = request.POST.get('date_dernier_renouvellement')
        nombre_renouvellement = request.POST.get('nombre_renouvellement')
        etat_renouvellement = request.POST.get('etat_renouvellement')
        historique_gestion_renouvellements = request.POST.get('historique_gestion_renouvellements')

        # Fetch related objects
        code_site = get_object_or_404(Site, id=code_site_id)
        wilaya = get_object_or_404(Wilaya, id=wilaya_id)
        notaire = get_object_or_404(Notaire, id=notaire_id)

        # Create a new Contrat instance
        Contrat.objects.create(
            code_site=code_site,
            wilaya=wilaya,
            propriete=propriete,
            type_contrat=type_contrat,
            ref_dernier_contrat=ref_dernier_contrat,
            bail_location_annuel=bail_location_annuel,
            notaire=notaire,
            date_signature_dernier_contrat=date_signature_dernier_contrat,
            duree_bail_dernier_contrat=duree_bail_dernier_contrat,
            date_fin_contrat=date_fin_contrat,
            duree_restante_avant_expiration=duree_restante_avant_expiration,
            etat_contrat_actuel=etat_contrat_actuel,
            date_dernier_renouvellement=date_dernier_renouvellement,
            nombre_renouvellement=nombre_renouvellement,
            etat_renouvellement=etat_renouvellement,
            historique_gestion_renouvellements=historique_gestion_renouvellements
        )

        # Redirect to the list of contracts or another page
        return redirect('contrats')  # Assuming you have a URL named 'contrats' for listing contracts

    # Fetch necessary data for the form
    sites = Site.objects.all()
    wilayas = Wilaya.objects.all()
    notaires = Notaire.objects.all()
    
    return render(request, 'contrats/create_contrat.html', {
        'sites': sites,
        'wilayas': wilayas,
        'notaires': notaires,
    })


def delete_contrat(request, c_id):                 #activates site delete button
    contrat = get_object_or_404(Contrat, id=c_id)
    contrat.delete()
    return redirect(reverse('contrats'))

def bailnprofile(request):                  #Contains new profile page
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()

    return render(request, 'bailleurs/newbailleur.html', {'communes': communes,'dairas': dairas,'wilayas': wilayas,'bailleurs': bailleurs,})

def create_bail(request):            #actiavtes site creation button
    if request.method == 'POST':
        nom_bailleur = request.POST.get('nom_bailleur')
        prenom_bailleur = request.POST.get('prenom_bailleur')
        num_mobile = request.POST.get('num_mobile')
        num_fixe = request.POST.get('num_fixe')
        num_fax = request.POST.get('num_fax')
        courriel = request.POST.get('courriel')
        banque = request.POST.get('banque')
        num_compte = request.POST.get('num_compte')
        autre = request.POST.get('autre')
        remarque = request.POST.get('remarque')

        # Create a new Bailleur instance
        Bailleur.objects.create(
            nom_bailleur=nom_bailleur,
            prenom_bailleur=prenom_bailleur,
            num_mobile=num_mobile,
            num_fixe=num_fixe,
            num_fax=num_fax,
            courriel=courriel,
            banque=banque,
            num_compte=num_compte,
            autre=autre,
            remarque=remarque
        )

    # Fetch necessary data for the form
    communes = Commune.objects.all()
    dairas = Daira.objects.all()
    wilayas = Wilaya.objects.all()
    bailleurs = Bailleur.objects.all()
    sites = Site.objects.all()


    return render(request, 'sites/sites.html', {
        'sites': sites,

    })