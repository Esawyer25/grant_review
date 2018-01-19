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

    #4)update the total costs associated with the project feilds in the grant objects
    all_related_grants = Related_grant.objects.all()


    for related_grant_object in all_related_grants:
        # related_grant_object = grant.related_grant_set.get()
        total_cost = 0
        indirect = 0
        direct = 0
        assoc_grants = related_grant_object.grants.all()
        for assoc_grant in assoc_grants:
            if assoc_grant.total_cost:
                total_cost += assoc_grant.total_cost

            if assoc_grant.indirect_cost_amt:
                indirect += assoc_grant.indirect_cost_amt

            if assoc_grant.direct_cost_amt:
                direct += assoc_grant.direct_cost_amt

        related_grant_object.total_funding_of_core_numb = total_cost
        grant.total_funding_of_core_numb = total_cost

        related_grant_object.total_indirect_of_core_numb = indirect
        grant.total_indirect_of_core_numb = indirect

        related_grant_object.total_direct_of_core_numb = direct
        grant.total_direct_of_core_numb = direct

        related_grant_object.save()
        grant.save()

        try:
            related_grant_object.save()
            print (f'new grant_related object {grant.core_project_num}, total_cost = {total_cost}')
        except:
            print(f"there was a problem saving total cost info for related_grant_object {related_grant_object.core_project_num}")

        try:
            assoc_grant.save()
        except:
            print(f"there was a problem saving total cost info for grant {assoc_grant.application_id}")
