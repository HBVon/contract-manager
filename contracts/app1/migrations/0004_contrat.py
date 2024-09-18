# Generated by Django 5.0.6 on 2024-08-07 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_bailleur_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propriete', models.CharField(choices=[('AADL', 'AADL'), ('ACED', 'ACED'), ('ADA', 'ADA'), ('ADE', 'ADE'), ('Aéroport', 'Aéroport'), ('Affaires Religieuses', 'Affaires Religieuses'), ('Algérie Poste', 'Algérie Poste'), ('Algérie Telecom', 'Algérie Telecom'), ('APC', 'APC'), ('ATM/ Mobilis', 'ATM/ Mobilis'), ('CABAM', 'CABAM'), ('Coloc OTA', 'Coloc OTA'), ('Coloc WTA', 'Coloc WTA'), ('Conservation des forêts', 'Conservation des forêts'), ('COSIDER', 'COSIDER'), ('Direction de la culture', 'Direction de la culture'), ('DJS', 'DJS'), ('Domaine', 'Domaine'), ('DOU/ Université', 'DOU/ Université'), ('EPSP', 'EPSP'), ('Exploitation Agricole', 'Exploitation Agricole'), ('GICA', 'GICA'), ('MDN', 'MDN'), ('Naftal', 'Naftal'), ('Privé', 'Privé'), ('Privé/ A. Commerciale', 'Privé/ A. Commerciale'), ('Protection Civile', 'Protection Civile'), ('Rail Telecom', 'Rail Telecom'), ('SCIMAT', 'SCIMAT'), ('SOGRAL', 'SOGRAL'), ('TDA', 'TDA'), ('Université', 'Université'), ('Wilaya', 'Wilaya'), ('Coloc OOREDO', 'Coloc OOREDO'), ('ColoC Djezzy', 'ColoC Djezzy')], max_length=255)),
                ('type_contrat', models.CharField(choices=[('Contrat notarié', 'Contrat notarié'), ('Convention Cadre', 'Convention Cadre'), ('Convention site', 'Convention site'), ('Résilié', 'Résilié'), ('En litige', 'En litige')], max_length=255)),
                ('ref_dernier_contrat', models.CharField(max_length=255)),
                ('bail_location_annuel', models.FloatField()),
                ('date_signature_dernier_contrat', models.DateField()),
                ('duree_bail_dernier_contrat', models.IntegerField()),
                ('date_fin_contrat', models.DateField()),
                ('duree_restante_avant_expiration', models.IntegerField()),
                ('etat_contrat_actuel', models.CharField(choices=[('Actif', 'Actif'), ('Expiré', 'Expiré'), ('Résilié', 'Résilié')], max_length=255)),
                ('date_dernier_renouvellement', models.DateField()),
                ('nombre_renouvellement', models.IntegerField()),
                ('etat_renouvellement', models.CharField(choices=[('En cour', 'En cour'), ('Renouvelé', 'Renouvelé'), ('À résilier', 'À résilier')], max_length=255)),
                ('historique_gestion_renouvellements', models.TextField(blank=True, null=True)),
                ('code_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.site')),
                ('notaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.notaire')),
                ('wilaya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.wilaya')),
            ],
        ),
    ]
