
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
from CapApp.models import Grant

import csv



myurl = "https://s3-us-west-2.amazonaws.com/nih-cvs-files/RePORTER_PRJ_C_FY2016.csv"

# Full path and name to csv file
# "seed_data/PRJ_csv/RePORTER_PRJ_C_FY2016.csv",
# csv_PRJ_files= ["seed_data/PRJ_csv/RePORTER_PRJ_C_FY2015.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2016.csv"]


# csv_PRJ_files= ["PRJ_csv/RePORTER_PRJ_C_FY2016.csv"]

def date_normal(input):
    if input=="":
        temp = "1111-11-11"
    else:
        temp = input
        if temp[1] == "/":
            temp = "0" + temp
        if temp[4] == "/":
            temp = temp[0:3] + "0" + temp[3:len(temp)]
        temp = temp[6:10] + "-"+ temp[0:2] + "-" + temp[3:5]

    return temp

def make_array_feild(data):
    list = data.split(";")
    for item in list:
        if item == "":
            list.remove(item)
        if "(contact)" in item:
            item.replace("(contact)","*")
    return list




# obj = s3.Object("nih-cvs-files", "RePORTER_PRJ_C_FY2016.csv")
# # csv_file = obj.get()['Body'].read()
# csv_file = obj.get()['Body'].read().decode('ISO-8859-1')

for line in smart_open.smart_open('s3://nih-cvs-files/RePORTER_PRJ_C_FY2016.csv'):
    print(type(line))
    str = line.decode('ISO-8859-1')
    print(type(str))
    print(str)
    print("this is a line break")

    str = str.split(',', 25)
    if str[0] != 'APPLICATION_ID':

        application_id = str[0]
        print(application_id)
        activity = str[1]
        print(activity)
        administering_ic = str[2]
        print(administering_ic)
        application_type = str[3]
        print(application_type)
        # arra_funded = str[4]
        award_notice_date = date_normal(str[5])
        print(award_notice_date)
        budget_start = date_normal(str[6])
        print(budget_start)
        budget_end = date_normal(str[7])
        print(budget_end)
        # cfda_code = str[8]
        core_project_num = str[9]
        print(core_project_num)
        ed_inst_type = str[10]
        print(ed_inst_type)
        foa_number = str[11]
        print(foa_number)
        full_project_num = str[12]
        print(full_project_num)
        funding_ics = str[13]
        print(funding_ics)
        funding_mechanism = str[14]
        print(funding_mechanism )
        FY = str[15]
        print(FY)
        ic_name = str[16]
        print(f'ic_name: {ic_name}')
        # str = str[17].split('",',1)
        # nih_spending_cats = str[17]
        # print(f'spending cats {nih_spending_cats}')
        # str = str[1].split(",",10)
        org_city = str[18]
        print(org_city)
        org_country = str[19]
        print(org_country)
        org_dept = str[20]
        print(f'org_dept: {org_dept}')

        if str[21] == "":
            org_district = None
        else:
            org_district = str[21]
        print(org_district)
            # org_duns = str[4]
            #
            # org_fips = str[5]
            #
            # org_ipf_code = str[6]
        org_name = str[22]
        print(org_name)
        org_state = str[23]
        print(org_state)
        org_zipcode = str[24]
        print(org_zipcode)

        str = str[25].split('",',1)
        phr  = str[0]
        print(phr)

        str = str[1].split(",",1)
        pi_ids = str[0]
        print(pi_ids)

        str = str[1].split('",',2)
        pi_name = make_array_feild(str[0])
        print(f'pi_name{pi_name}')

        # program_officer_name = str[1]
        str = str[2].split(",",14)
        # project_start = date_normal(str[0])
        # project_end = date_normal(str[1])
        # print(project_end)
        project_terms = str[2]
        print(f'project_terms: {project_terms}')
        project_title = str[3]
        print(project_title)
        # serial_number = str[4]
        study_section = str[5]
        print(study_section)
        study_section_name = str[6]
        print(study_section_name)
        subproject_id = str[7]
        print(subproject_id)
        # suffix = str[8]
        if str[9] == "":
            support_year = None
        else:
            support_year = str[9]
        print(f'support_year: {support_year}')

        print(str)
        if str[10] == "":
            direct_cost_amt = None
        else:
            direct_cost_amt = str[10]
        print (direct_cost_amt)

        if str[11] == "":
            indirect_cost_amt = None
        else:
            indirect_cost_amt = str[11]
        print(indirect_cost_amt)

        if str[12] == "":
            total_cost = None;
        else:
            total_cost = str[12]
        print(total_cost)

        if str[13] == "":
            total_cost_sub_project = None
        else:
            total_cost_sub_project = str[13]
        print(total_cost_sub_project)

print(type(csv_file))
# csv_file = obj.get()['Body'].read().decode('ISO-8859-1')
csv_files = []
csv_files.append(csv_file)




for csv_file in csv_files_Stop:
        dataReader = csv.reader(open(csv_file, encoding = "ISO-8859-1"), delimiter=',', quotechar='"')

        # dataReader = csv.reader(open(csv_PRJ_file, encoding = "ISO-8859-1"), delimiter=',', quotechar='"')

        index = -1
        success = 0
        for row in dataReader:
            # print(row[1])
            # print('line break')
            index +=1
            if row[0] != 'APPLICATION_ID': # Ignore the headerrow,
                grant = Grant()
                # print(row[0])
                grant.application_id = row[0]
                # print(row[1])
                grant.activity = row [1]
                # print(row[2])
                grant.administering_ic = row[2]
                # print(row[3])
                grant.application_type = row[3]

                # grant.arra_funded = row[4]

                grant.award_notice_date = date_normal(row[5])

                grant.budget_start = date_normal(row[6])

                grant.budget_end = date_normal(row[7])

                # grant.cfda_code = row[8]
                # print(row[9])
                grant.core_project_num = row[9]
                # print(row[10])
                grant.ed_inst_type = row[10]

                # grant.foa_number = row[11]
                # print(row[12])
                grant.full_project_num = row[12]
                # print(row[13])
                grant.funding_ics = row[13]
                # print(row[14])
                grant.funding_mechanism = row[14]

                # print(row[15])
                grant.FY = row[15]

                # print(row[16])
                grant.ic_name = row[16]

                # grant.nih_spending_cats = row[17]

                # print(row[18])
                grant.org_city = row[18]

                # print(row[19])
                grant.org_country = row[19]

                # print(row[20])
                grant.org_dept = row[20]

                # print(row[21])
                if row[21] == "":
                    grant.org_district = None
                else:
                    grant.org_district = row[21]

                # grant.org_duns = row[22]

                # grant.org_fips = row[23]

                # grant.org_ipf_code = row[24]
                # print(row[25])
                grant.org_name = row[25]

                # print(row[26])
                grant.org_state = row[26]

                # print(row[27])
                grant.org_zipcode = row[27]

                # print(row[28])
                grant.phr = row[28]

                # print(row[29])
                grant.pi_ids = row[29]

                # print(row[30])
                grant.pi_name= make_array_feild(row[30])

                # grant.program_officer_name = row[31]

                # grant.project_start = row[32]

                # grant.project_end = row[33]

                # print(row[34])
                grant.project_terms = row[34]

                # print(row[35])
                grant.project_title = row[35]

                # grant.serial_number = row[36]

                # print(row[37])
                grant.study_section = row[37]

                # print(row[38])
                grant.study_section_name = row[38]

                # print(row[39])
                grant.subproject_id = row[39]

                # grant.suffix = row[40]

                # print(row[41])
                if row[41] == "":
                    grant.support_year = None
                else:
                    grant.support_year = row[41]

                # print(row[42])
                if row[42] == "":
                    grant.direct_cost_amt = None
                else:
                    grant.direct_cost_amt = row[42]

                    # print(row[43])
                if row[43] == "":
                    grant.indirect_cost_amt = None
                else:
                    grant.indirect_cost_amt = row[43]

            # print(row[44])
                if row[44] == "":
                    grant.total_cost = None;
                else:
                    grant.total_cost = row[44]

            # print(row[45])
                if row[45] == "":
                    grant.total_cost_sub_project = None
                else:
                    grant.total_cost_sub_project = row[45]

                try:
                    Grant.full_clean(grant)
                except ValidationError as e:
                    print(e)

                try:
                    grant.save()
                    success +=1
                    # print(f"saved application_id {grant.application_id}")
                    # print(f"saved {success} out of {index}")
                except:
                    print(f"there was a problem with row {index}, application id: {row[0]}, file {csv_PRJ_file}")
                    # print(f"saved {success} out of {index}")
        print(f"{csv_PRJ_file} saved {success} out of {index}")

groups= ["C", "G", "H", "L", "O", "P", "T", "U", "V", "X"]
for code in groups:
    temp = Grant.objects.filter(activity__startswith = code)
    print(f'deleting {temp.count()} grants starting with {code}')
    temp.delete()

    #IK3 = Non-DHHS Nursing Research Initiative
activity_codes = ["IK3"]
for code in activity_codes:
    temp = Grant.objects.filter(activity = code)
    print(f'deleting {temp.count()} {code} grants')
    temp.delete()



# csv_PRJABS_files =["seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2015.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2016.csv"]
csv_PRJABS_files=["PRJABS_csv/RePORTER_PRJABS_C_FY2016.csv"]

for csv_PRJABS_file in csv_PRJABS_files:

    dataReader = csv.reader(open(csv_PRJABS_file, encoding = "ISO-8859-1"), delimiter=',', quotechar='"')

    index = -1
    success = 0
    for row in dataReader:
        index +=1
        if row[0] != 'APPLICATION_ID': # Ignore the headerrow,
            try:
                focal = Grant.objects.get(application_id= row[0])
                abstract_text = row[1]
                if abstract_text[0] == "?":
                    abstract_text = abstract_text[1:]

                focal.abstract_text = abstract_text

                try:
                    Grant.clean_fields(focal)
                except ValidationError as e:
                    print(e)

            except:
                print(f"no grant with application id {row[0]}")


            try:
                focal.save()
                success +=1
            # print(f"saved application_id {grant.application_id}")
            # print(f"saved {success} out of {index}")
            except:
                print(f"there was a problem with row {index}, application id: {row[0]}, file: {csv_PRJABS_file}")
                # print(f"saved {success} out of {index}")
    print(f"file {csv_PRJABS_file} saved {success} out of {index}")
