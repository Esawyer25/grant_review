
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
from CapApp.models import Grant_Publication

import csv
import zipfile

# Full path and name to csv file
# csv_files= ["seed_data/linktables_csv/RePORTER_PUBLNK_C_2016.csv"]

zip_files = ['seed_data/zipfiles_linktables/RePORTER_PUBLNK_C_2016.zip']

for zip_file in zip_files:
    zf = zipfile.ZipFile(zip_file, 'r')
    for zi in zf.infolist():
        csv_file_path= zf.extract(zi)
        print(csv_file_path)
        zf.close()

        dataReader = csv.reader(open(csv_file_path, encoding = "ISO-8859-1"), delimiter=',', quotechar='"')

        for row in dataReader:

            if row[0] != 'PMID': # Ignore the headerrow,
        #consider only importing rows where the project_number exists in the database
                grant_pub = Grant_Publication()
            # print(row[0])
                grant_pub.pmid = row[0]
            # print(row[1])
                grant_pub.project_number = row[1]

                try:
                    Grant_Publication.full_clean(grant_pub)
                except ValidationError as e:
                    print(e)

                try:
                        grant_pub.save()
                        print('saved a link')
                except:
                    print('there was a problem with row with a link')

        print(csv_file_path)
