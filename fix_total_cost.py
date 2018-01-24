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
from CapApp.models import Keyword, Grant, Related_grant
from CapApp.custom_classes import Stats, Add_Keyword, Relate_grants

grants = Grant.objects.all()
keywords = Keyword.objects.all()

for keyword in keywords:
    print(keyword)
    grants = keyword.grants.all()
    for grant in grants:
        total_cost = 0
        direct_cost = 0
        indirect_cost = 0
        if grant.total_funding_of_core_numb == None:
            rgo= None
            try:
                rgo = grant.related_grant_set.get()
                print(f'I found this related_grant_set: {related_grant_object}' )
            except:
                pass
            print(rgo)
            for assoc_grant in assoc_grants:
                if assoc_grant.total_cost:
                    total_cost +=   assoc_grant.total_cost

                if assoc_grant.indirect_cost_amt:
                    indirect += assoc_grant.indirect_cost_amt

                if assoc_grant.direct_cost_amt:
                    direct +=  assoc_grant.direct_cost_amt

            rgo= Related_grant()

            rgo.core_project_num = grant.core_project_num

            rgo.total_funding_of_core_numb = total_cost
            print(f'the total_funding_of_core_numb for new RGO is {rgo.total_funding_of_core_numb}')

            rgo.total_indirect_of_core_numb = indirect

            rgo.total_direct_of_core_numb = direct
            try:
                rgo.save()
                print('this is the new_R_G_O ')
                print(rgo.core_project_num)

            except ValidationError as e:
                print(e)

            try:
                rgo.grants.set(assoc_grants)
            except:
                print("there was a problem setting the RGO")

            grant.total_funding_of_core_numb = rgo.total_funding_of_core_numb
            grant.total_indirect_of_core_numb = rgo.total_indirect_of_core_numb
            grant.total_direct_of_core_numb = rgo.total_direct_of_core_numb

            try:
                grant.save()
                print ('saved total_funding_of_core_numb')

            except ValidationError as e:
                print(e)

    grants = Add_Keyword.no_repeats(grants)

    scatterplot_array = Add_Keyword.cost_scatterplot(grants)
    keyword.scatterplot_array = scatterplot_array

    try:
        keyword.save()
        print('I saved the new scatterplot')
    except:
        print(f"there was a problem saving with scatterplot")
