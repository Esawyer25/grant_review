
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

# Full path and name to csv file
csv_files= ["seed_data/linktables_csv/RePORTER_PUBLNK_C_2016.csv"]

for csv_file in csv_files:

    dataReader = csv.reader(open(csv_file, encoding = "ISO-8859-1"), delimiter=',', quotechar='"')

    index = -1
    success = 0
    for row in dataReader:
        index +=1
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
                success +=1
                # print(f"saved application_id {grant.application_id}")
                # print(f"saved {success} out of {index}")
            except:
                print(f"there was a problem with row {index}, pmid id: {row[0]}, file {csv_file}")
                # print(f"saved {success} out of {index}")
    print(f"{csv_file} saved {success} out of {index}")
