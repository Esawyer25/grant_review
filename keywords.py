import django
import os
import sys


PATH=os.path.abspath(os.path.dirname(__file__))

if os.name == 'posix': # Unix based systems
    bin_name = 'bin'
else:                  # Windows
    bin_name = 'Scripts'

# Relative path to the virtual environment
# (relative to the stand-alone script)
rel_path = '../venv/%s/activate_this.py' % bin_name
activate_this = os.path.join(PATH, rel_path)

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CapProj.settings")

django.setup()
from django.core.exceptions import ValidationError
from CapApp.models import Keyword, Grant
from CapApp.custom_classes import Stats, Add_Keyword


keywords =["Primate", "Autism", "Primate", "Pain", "Electrosensory", "Cancer", "big data", "biotechnology", "Lung", "Pulmonary fibrosis",  "evolution", "immunotherapy", "somatosensory", "learning", "memory","gender", "therapy", "cancer", "AIDS", "HIV", "cardiac", "stroke"]

# "machine learning", "nanotechnology", "adaptive immune response", "adaptive immunity", "adult", "youth", "disability", "flu", "deppression", "vaccine", "dementia", "malignant", "transplant", "somatosensory", "vision", "audition", "Hodgkin's Disease", "convergance", "cure", "olfaction","Acquired Cognitive Impairment","Acute Respiratory Distress Syndrome", "Adolescent Sexual Activity","data mining", "Agent Orange","Dioxin","Aging","Alcoholism","Allergic Rhinitis", "Hay Fever","ALS","Alzheimer's Disease","Alzheimer's","Alzheimer", "Alzheimer's Disease Related Dementias","American Indians","Alaska Natives","Anorexia","Anthrax","Antimicrobial Resistance","Anxiety Disorders","Aphasia", "Arctic","Arthritis","Assistive Technology","Asthma","Ataxia Telangiectasia","Louis–Bar syndrome", "Atherosclerosis","Attention Deficit Disorder","ADD","Autism","Autoimmune Disease","Back Pain","Batten Disease","Behavioral and Social Science","Biodefense","Bioengineering","Biotechnology","Bipolar Disorder","Brain Cancer","Brain Disorders","Breast Cancer","Burden of Illness","Cachexia","Cancer", "Cancer Genomics","Cannabinoid","Cardiovascular","Caregiving","Cerebral Palsy","Cerebrovascular","Cervical Cancer","Charcot-Marie-Tooth Disease","Child Abuse", "Neglect", "Childhood Leukemia", "Leukemia","Chronic Fatigue Syndrome", "ME/CFS","Chronic Liver Disease", "Cirrhosis","Chronic Obstructive", "Pulmonary Disease","Climate Change","Clinical Trials", "Colo-Rectal Cancer", "Alternative Medicine","Congenital","Congenital Heart Disease","Muscular Dystrophy","Congenital Structural Anomalies","Contraception","Reproduction","Cooley's Anemia","Crohn's Disease","Cystic Fibrosis","Dementia","Craniofacial Disease","Dental","Depression","Diabetes","Prader-Willi syndrome","Prader-Willi"]
#"Diet","Fat","Obesity","Dietary Supplements","Diethylstilbestrol","DES","Digestive Diseases","Gallbladder","Peptic Ulcer","Down Syndrome","Drug Abuse","Duchenne","Duchenne Muscular Dystrophy","Becker","Becker Muscular Dystrophy","Muscular Dystrophy","Dystonia","Eating Disorders","Eczema","Atopic Dermatitis","Emergency Care","Emerging Infectious Diseases","Emphysema","Endocannabinoid","Endocrine Disruptors","Endometriosis","Epilepsy","Estrogen","Eye Disease","Facioscapulohumeral Muscular Dystrophy","Facioscapulohumeral","Fetal Alcohol Syndrome","Fibroid Tumors ","Uterine","Fibromyalgia","Food Allergies","Allergies","Foodborne Illness","Fragile X Syndrome","Frontotemporal Dementia ","FTD","Gene Therapy","Genetic Testing","Genetics","Global Warming","Climate Change","Headaches","Migrane","Health Disparities","Indoor Air Pollution","Health Services","Heart Disease","Coronary Heart Disease","Hematology","Hepatitis","Hepatitis A","Hepatitis B","Hepatitis C","HIV/AIDS","Hodgkin's Disease","Homelessness","Homicide","HPV","Cervical Cancer Vaccines"
#"Human Fetal Tissue","Human Genome","Huntington's Disease","Hydrocephalus","Hyperbaric Oxygen","Hypertension","Immunization","Infant Mortality","Infectious Diseases","Infertility","Inflammatory Bowel Disease","Influenza","Injury","Intellectual ","Developmental Disabilities","Interstitial Cystitis","Kidney Disease","Lead Poisoning","Lewy Body Dementia","Liver Cancer","Liver Disease","Lung","Lung Cancer","Lupus","Lyme Disease","Lymphoma","Macular Degeneration","Major Depressive Disorder","Malaria","Malaria Vaccine","Mental Health","Mental Illness","Methamphetamine","Migraines","Minority","Mucopolysaccharidoses","MPS","Multiple Sclerosis","MS","Muscular Dystrophy","Myasthenia Gravis","Myotonic Dystrophy","Nanotechnology","Neck Pain","Neonatal ","Respiratory,Distress","Neuroblastoma","Neurodegenerative","Neurofibro,atosis","Neurosciences","Nutrition","Obesity","Organ Transplantation","Orphan Drug","Osteoarthritis","Osteogenesis Imperfecta","Osteoporosis","Otitis Media","Ovarian Cancer","Paget's Disease","Pancreatic Cancer","Parkinson's Disease","Patient Safety","Pediatric","Pediatric Cancer","Pediatric Cardiomyopathy","Pediatric Research Initiative","Pelvic Inflammatory Disease","Perinatal Period","Peripheral Neuropathy","Physical Activity","Physical Rehabilitation"
# "Pick's Disease","Pneumonia","Pneumonia & Influenza","Polycystic Kidney Disease","Post-Traumatic Stress Disorder","PTSD","Precision Medicine","Prescription Drug Abuse","Preterm","Low Birth Weight ","Newborn","Prevention","Prostate Cancer","Psoriasis","Radiation Oncology","Rare Diseases","Regenerative Medicine","Rehabilitation","Rett Syndrome","Reye's Syndrome","Rheumatoid Arthritis","Rural Health","Sarcopenia","Schizophrenia","Scleroderma","Substance Abuse","Septicemia","Serious Mental Illness","Sexual and Gender Minorities","Sexually Transmitted Diseases","Herpes","Sickle Cell Disease","Sleep Research","Small pox","Smoking and Health","Spina Bifida","Spinal Cord","Spinal Cord Injury","Spinal Muscular Atrophy","Stem Cell Research","Stroke","Substance Abuse Prevention","Sudden Infant Death Syndrome","SIDS","Suicide","Suicide Prevention","Teenage Pregnancy","Temporomandibular","TMJD","Therapeutic Cannabinoid Research","Tobacco","Topical Microbicides","Tourette Syndrome","Transmissible Spongiform Encephalopathy","TSE","Mad Cow Disease","Transplantation","Tuberculosis","Tuberculosis Vaccine","Tuberous Sclerosis","Underage Drinking","Urologic Diseases","Usher Syndrome","Uterine Cancer","Vaccine","Vaginal Cancer","Valley Fever","Vascular Cognitive Impairment","Vector-Borne Diseases","Violence Against Women","Violence Research","Vulvodynia","West Nile Virus","Women's Health","Men's Health","Youth Violence","Youth Violence"]

# "age", "age related", "aging", "antibody response", "biochemical", "biogenesis", "blood platelets", "cells", "cessation of life", "cytokine", "Cytometry", "Dendritic Cells", "disability", "flu"]

# keywords2 =
#  "elderly", "gene expression", "genetic", "health", "human", "immune",  "immune function", Immune response; Immune system; Immunologics; Immunology; immunosenescence; Impairment; improved; Individual; Infection; Influenza; Influenza A Virus, H1N1 Subtype; Influenza prevention; Influenza vaccination; Influenza virus vaccine; influenzavirus; insight; Institutes; Integration Host Factors; Lipids; Liquid Chromatography; Mass Spectrum Analysis; meetings; Metabolic; Metabolic Pathway; Metabolism; metabolomics; Methods; Mitochondria; Molecular; Molecular Profiling; monocyte; mortality; Natural Immunity; Natural Killer Cells; neutrophil; novel; Nursing Homes; Operative Surgical Procedures; Outcome; oxidation; pandemic disease; Pathway interactions; Pattern recognition receptor;
 # Pharmaceutical Preparations; Physiological; Population; Production; programs; Proteins; Public Health; receptor; receptor function; Recruitment Activity; Registries; Research; Research Infrastructure; residence; Resistance; Resources; response; Sampling; Seasons; Serum; Signal Transduction; Stress; Syndrome; targeted treatment; Toll-like receptors; transcriptome sequencing; transcriptomics; Translating; United States; Vaccination; vaccine response; Vaccines; Viral Hemagglutinins; Whole Blood; Work; young adult;

for word in keywords:
    word = word.capitalize()
    print(f'this is the word: {word}')
    try:
        new_word = Keyword.objects.get(keyword__iexact=word)
    except:
        new_word = None

    if new_word:
        print(f'this is a repeat: {word}')
    else:
        new_word = Keyword()
        new_word.keyword = word
        new_word.searches = 0

        try:
            Keyword.full_clean(new_word)
        except ValidationError as e:
            print(e)


        try:
            new_word.save()
            print(f'saved new keyword {new_word.keyword}')
        except:
            print(f"there was a problem saving with Keyword {word}")


    grant_list =Grant.objects.filter(project_terms__search=word)
    for grant in grant_list:
        new_word.grants.add(grant)

    Add_Keyword.set_keyword_stats(new_word, grant_list)

    Related_grants.set_related_grant_stats(grant_list)




    # grant_stats = Stats.return_stats_by_year(grant_list, word)
    #
    # new_word.grant_count = grant_stats['totals']['grant_count']
    #
    # new_word.grant_total_cost = grant_stats['totals']['grant_total_cost']
    #
    # new_word.grant_direct_cost = grant_stats['totals']['grant_direct_cost']
    #
    # new_word.grant_indirect_cost = grant_stats['totals']['grant_indirect_cost']
    #
    # # new_word.grant_count_18 = grant_stats['2018']['grant_count']
    # #
    # # new_word.grant_total_cost_18 = grant_stats['2018']['grant_total_cost']
    # #
    # # new_word.grant_direct_cost_18 = grant_stats['2018']['grant_direct_cost']
    # #
    # # new_word.grant_indirect_cost_18 = grant_stats['2018']['grant_indirect_cost']
    #
    # new_word.grant_count_17 = grant_stats['2017']['grant_count']
    #
    # new_word.grant_total_cost_17 = grant_stats['2017']['grant_total_cost']
    #
    # new_word.grant_direct_cost_17 = grant_stats['2017']['grant_direct_cost']
    #
    # new_word.grant_indirect_cost_17 = grant_stats['2017']['grant_indirect_cost']
    #
    # new_word.grant_count_16 = grant_stats['2016']['grant_count']
    #
    # new_word.grant_total_cost_16 = grant_stats['2016']['grant_total_cost']
    #
    # new_word.grant_direct_cost_16 = grant_stats['2016']['grant_direct_cost']
    #
    # new_word.grant_indirect_cost_16 = grant_stats['2016']['grant_indirect_cost']
    #
    # new_word.grant_count_15 = grant_stats['2015']['grant_count']
    #
    # new_word.grant_total_cost_15 = grant_stats['2015']['grant_total_cost']
    #
    # new_word.grant_direct_cost_15 = grant_stats['2015']['grant_direct_cost']
    #
    # new_word.grant_indirect_cost_15 = grant_stats['2015']['grant_indirect_cost']
    #
    # new_word.f31_count= grant_stats['totals']['f31_count']
    #
    # new_word.f31_total_cost= grant_stats['totals']['f31_total_cost']
    #
    # new_word.f32_count= grant_stats['totals']['f32_count']
    #
    # new_word.f32_total_cost= grant_stats['totals']['f32_total_cost']
    #
    # new_word.k99_count= grant_stats['totals']['k99_count']
    #
    # new_word.k99_total_cost= grant_stats['totals']['k99_total_cost']
    #
    # new_word.r00_count= grant_stats['totals']['r00_count']
    #
    # new_word.r00_total_cost= grant_stats['totals']['r00_total_cost']
    #
    # new_word.r01_count= grant_stats['totals']['r01_count']
    #
    # new_word.r01_total_cost= grant_stats['totals']['r01_total_cost']
    #
    # new_word.r35_count= grant_stats['totals']['r35_count']
    #
    # new_word.r35_total_cost= grant_stats['totals']['r35_total_cost']
    #
    # new_word.dp1_count= grant_stats['totals']['dp1_count']
    #
    # new_word.dp1_total_cost= grant_stats['totals']['dp1_total_cost']
    #
    # new_word.dp2_count= grant_stats['totals']['dp2_count']
    #
    # new_word.dp2_total_cost= grant_stats['totals']['dp2_total_cost']
    #
    # try:
    #     Keyword.full_clean(new_word)
    # except ValidationError as e:
    #     print(e)
    #
    # try:
    #     new_word.save()
    # except:
    #     print(f"there was a problem saving the stats associated with Keyword {word}")
