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


keywords =["Hodgkin's Disease", "autism", "primate", "big data", "cancer",  "biotechnology", "convergance", "cure", "evolution", "data mining", "immunotherapy", "machine learning", "learning", "memory", "nanotechnology", "novel", "scalability", "synergey", "therapy", "cancer", "AIDS", "HIV", "cardiac", "stroke", "gender" "acute", "adaptive immune response", "adaptive immunity", "adult", "youth", "disability", "flu", "deppression", "vaccine", "dementia", "malignant", "transplant", "somatosensory", "vision", "audition", "olfaction","Acquired Cognitive Impairment","Acute Respiratory Distress Syndrome", "Adolescent Sexual Activity", "Agent Orange",'Dioxin","Aging","Alcoholism","Allergic Rhinitis", "Hay Fever","ALS","Alzheimer's Disease","Alzheimer's","Alzheimer". "Alzheimer's Disease Related Dementias","American Indians", "Alaska Natives","Anorexia","Anthrax","Antimicrobial Resistance","Anxiety Disorders","Aphasia","Arctic","Arthritis","Assistive Technology","Asthma","Ataxia Telangiectasia","Louis–Bar syndrome","Atherosclerosis","Attention Deficit Disorder","ADD","Autism","Autoimmune Disease","Back Pain","Batten Disease","Behavioral and Social Science","Biodefense","Bioengineering","Biotechnology","Bipolar Disorder","Brain Cancer","Brain Disorders","Breast Cancer","Burden of Illness","Cachexia","Cancer","Cancer Genomics","Cannabinoid","Cardiovascular","Caregiving","Cerebral Palsy","Cerebrovascular","Cervical Cancer","Charcot-Marie-Tooth Disease","Child Abuse", "Neglect", "Childhood Leukemia", "Leukemia","Chronic Fatigue Syndrome", "ME/CFS","Chronic Liver Disease", "Cirrhosis","Chronic Obstructive", "Pulmonary Disease","Climate Change","Clinical Trials", "Colo-Rectal Cancer", "Alternative Medicine","Congenital","Congenital Heart Disease","Muscular Dystrophy","Congenital Structural Anomalies","Contraception","Reproduction","Cooley's Anemia","Crohn's Disease","Cystic Fibrosis","Dementia","Craniofacial Disease","Dental","Depression","Diabetes","Prader-Willi syndrome","Prader-Willi","Diet","Fat","Obesity","Dietary Supplements","Diethylstilbestrol","DES","Digestive Diseases","Gallbladder","Peptic Ulcer","Down Syndrome","Drug Abuse","Duchenne","Duchenne Muscular Dystrophy","Becker","Becker Muscular Dystrophy","Muscular Dystrophy","Dystonia","Eating Disorders","Eczema","Atopic Dermatitis","Emergency Care","Emerging Infectious Diseases","Emphysema","Endocannabinoid","Endocrine Disruptors","Endometriosis","Epilepsy","Estrogen","Eye Disease","Facioscapulohumeral Muscular Dystrophy","Facioscapulohumeral","Fetal Alcohol Syndrome","Fibroid Tumors ","Uterine","Fibromyalgia","Food Allergies","Allergies","Foodborne Illness","Fragile X Syndrome","Frontotemporal Dementia ","FTD","Gene Therapy","Genetic Testing","Genetics","Global Warming","Climate Change","Headaches","Migrane","Health Disparities","Indoor Air Pollution","Health Services","Heart Disease","Coronary Heart Disease","Hematology","Hepatitis","Hepatitis A","Hepatitis B","Hepatitis C","HIV/AIDS","Hodgkin's Disease","Homelessness","Homicide","HPV","Cervical Cancer Vaccines","Human Fetal Tissue","Human Genome","Huntington's Disease","Hydrocephalus","Hyperbaric Oxygen","Hypertension","Immunization","Infant Mortality","Infectious Diseases","Infertility","Inflammatory Bowel Disease","Influenza","Injury","Intellectual ","Developmental Disabilities","Interstitial Cystitis","Kidney Disease","Lead Poisoning","Lewy Body Dementia","Liver Cancer","Liver Disease","Lung","Lung Cancer","Lupus","Lyme Disease","Lymphoma","Macular Degeneration","Major Depressive Disorder","Malaria","Malaria Vaccine","Mental Health","Mental Illness","Methamphetamine","Migraines","Minority","Mucopolysaccharidoses","MPS","Multiple Sclerosis","MS","Muscular Dystrophy","Myasthenia Gravis","Myotonic Dystrophy","Nanotechnology","Neck Pain","Neonatal ","Respiratory,Distress","Neuroblastoma","Neurodegenerative","Neurofibro,atosis","Neurosciences","Nutrition","Obesity","Organ Transplantation","Orphan Drug","Osteoarthritis","Osteogenesis Imperfecta","Osteoporosis","Otitis Media","Ovarian Cancer","Paget's Disease","Pain","Pancreatic Cancer","Parkinson's Disease","Patient Safety","Pediatric","Pediatric Cancer","Pediatric Cardiomyopathy","Pediatric Research Initiative","Pelvic Inflammatory Disease","Perinatal Period","Peripheral Neuropathy","Physical Activity","Physical Rehabilitation","Pick's Disease","Pneumonia","Pneumonia & Influenza","Polycystic Kidney Disease","Post-Traumatic Stress Disorder","PTSD","Precision Medicine","Prescription Drug Abuse","Preterm","Low Birth Weight ","Newborn","Prevention","Prostate Cancer","Psoriasis","Radiation Oncology","Rare Diseases","Regenerative Medicine","Rehabilitation","Rett Syndrome","Reye's Syndrome","Rheumatoid Arthritis","Rural Health","Sarcopenia","Schizophrenia","Scleroderma","Substance Abuse","Septicemia","Serious Mental Illness","Sexual and Gender Minorities","Sexually Transmitted Diseases","Herpes","Sickle Cell Disease","Sleep Research","Small pox","Smoking and Health","Spina Bifida","Spinal Cord","Spinal Cord Injury","Spinal Muscular Atrophy","Stem Cell Research","Stroke	"		,"Substance Abuse Prevention","Sudden Infant Death Syndrome","SIDS","Suicide","Suicide Prevention","Teenage Pregnancy","Temporomandibular","TMJD","Therapeutic Cannabinoid Research","Tobacco","Topical Microbicides","Tourette Syndrome","Transmissible Spongiform Encephalopathy","TSE","Mad Cow Disease","Transplantation","Tuberculosis","Tuberculosis Vaccine","Tuberous Sclerosis","Underage Drinking","Urologic Diseases","Usher Syndrome","Uterine Cancer","Vaccine","Vaginal Cancer","Valley Fever","Vascular Cognitive Impairment","Vector-Borne Diseases","Violence Against Women","Violence Research","Vulvodynia","West Nile Virus","Women's Health","Men's Health","Youth Violence","Youth Violence"]

# "age", "age related", "aging", "antibody response", "biochemical", "biogenesis", "blood platelets", "cells", "cessation of life", "cytokine", "Cytometry", "Dendritic Cells", "disability", "flu"]

# keywords2 =
#  "elderly", "gene expression", "genetic", "health", "human", "immune",  "immune function", Immune response; Immune system; Immunologics; Immunology; immunosenescence; Impairment; improved; Individual; Infection; Influenza; Influenza A Virus, H1N1 Subtype; Influenza prevention; Influenza vaccination; Influenza virus vaccine; influenzavirus; insight; Institutes; Integration Host Factors; Lipids; Liquid Chromatography; Mass Spectrum Analysis; meetings; Metabolic; Metabolic Pathway; Metabolism; metabolomics; Methods; Mitochondria; Molecular; Molecular Profiling; monocyte; mortality; Natural Immunity; Natural Killer Cells; neutrophil; novel; Nursing Homes; Operative Surgical Procedures; Outcome; oxidation; pandemic disease; Pathway interactions; Pattern recognition receptor;
 # Pharmaceutical Preparations; Physiological; Population; Production; programs; Proteins; Public Health; receptor; receptor function; Recruitment Activity; Registries; Research; Research Infrastructure; residence; Resistance; Resources; response; Sampling; Seasons; Serum; Signal Transduction; Stress; Syndrome; targeted treatment; Toll-like receptors; transcriptome sequencing; transcriptomics; Translating; United States; Vaccination; vaccine response; Vaccines; Viral Hemagglutinins; Whole Blood; Work; young adult;

for word in keywords:
    try:
        present = Keyword.objects.get(keyword=word)
    except:
        present = None

    if present:
        print(f'this is a repeat: {present}')
    new_word = Keyword()
    new_word.keyword = word
    new_word.searches = 0

    try:
        Keyword.full_clean(new_word)
    except ValidationError as e:
        print(e)

    print(new_word.keyword)

    try:
        new_word.save()
    except:
        print(f"there was a problem saving with Keyword {word}")

    present = Keyword.objects.get(keyword=word)

    grant_list =Grant.objects.filter(project_terms__search=word)
    for grant in grant_list:
        present.grants.add(grant)
