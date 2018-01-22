import django
import os
import sys

PATH=os.path.abspath(os.path.dirname(__file__))

if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    pass
else:
    from CapProj.settings_secret import SECRET_KEY

if os.name == 'posix': # Unix based systems
    bin_name = 'bin'
else:                  # Windows
    bin_name = 'Scripts'

# Relative path to the virtual environment
# (relative to the stand-alone script)
rel_path = '../venv/%s/activate_this.py' % bin_name
activate_this = os.path.join(PATH, rel_path)

sys.path.append('../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CapProj.settings')

django.setup()
from django.core.exceptions import ValidationError
from CapApp.models import Grant, Keyword
from CapApp.custom_classes import Stats, Add_Keyword

import csv

def date_normal(input):
    if input=='':
        temp = '1111-11-11'
    else:
        temp = input
        if temp[1] == '/':
            temp = '0' + temp
        if temp[4] == '/':
            temp = temp[0:3] + '0' + temp[3:len(temp)]
        temp = temp[6:10] + '-'+ temp[0:2] + '-' + temp[3:5]

    return temp

def make_array_feild(data):
    list = data.split(';')
    array= {}
    for item in list:
        item = item.title
        if item == '':
            list.remove(item)
        # if '(contact)' in item:
        #     item.replace('(contact)','*')
    array = set(list)
    return array

import zipfile

# Full path and name to your csv file

zip_files = ["seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_052.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_051.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_050.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_049.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_048.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_047.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_046.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_045.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_044.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_043.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_042.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_041.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_040.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_039.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_038.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_037.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_036.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_035.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_034.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_033.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_032.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_031.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_030.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_029.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_028.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_027.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_026.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_025.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_024.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_023.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_022.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_021.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_020.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_019.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_018.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_017.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_016.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_015.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_014.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_013.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_012.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_011.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_010.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_009.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_008.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_007.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_006.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_005.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_004.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_002.zip","seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2017_001.zip"]

for zip_file in zip_files:
    zf = zipfile.ZipFile(zip_file, 'r')
    for zi in zf.infolist():
        csv_file_path= zf.extract(zi)
        print(csv_file_path)
        zf.close()


        dataReader = csv.reader(open(csv_file_path, encoding = 'ISO-8859-1'), delimiter=',', quotechar='"')

        for row in dataReader:

            if row[0] != 'APPLICATION_ID': # Ignore the headerrow,
                try:
                    focal = Grant.objects.get(application_id= row[0])
                    focal.pi_name= row[30]


                    try:
                        Grant.full_clean(focal)
                    except ValidationError as e:
                        print(e)

                    try:
                        focal.save()
                    except:
                        print('there was a problem with row')

                except:
                    pass
            print('i have reached the end of a row')
                # print(f"saved {success} out of {index}")
    os.remove(csv_file_path)
    print('I HAVE REACHED THE END OF A FILE')
