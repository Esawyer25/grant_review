import django
import os
import sys


PATH = os.path.abspath(os.path.dirname(__file__))

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
from CapApp.models import Grant, Related_grant

all_grants = Grant.objects.all()
for grant in all_grants:
    #1) Does a releated_grant object already exist?
    try:
        present = Related_grant.objects.get(core_project_num=grant.core_project_num)
    except:
        present = None
    #2) if one does not exist, make it
    if present:
        print(f'this core_project_num is present: {present}')
    else:
        new_related_grant = Related_grant()
        new_related_grant.core_project_num = grant.core_project_num
    #3) try to save it and report errors
    try:
        new_related_grant.save()
    except:
        print(f"there was a problem saving with related_grant {grant.core_project_num}")
    #4) retrive the right grant
    present = Related_grant.objects.get(core_project_num=grant.core_project_num)

    grant_list = Grant.objects.filter(core_project_num=grant.core_project_num)
    for grant in grant_list:
        present.grants.add(grant)
