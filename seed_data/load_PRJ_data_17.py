
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


# Full path and name to your csv file
# csv_PRJ_files= ["seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_004.csv"]
csv_PRJ_files= ["PRJ_csv/RePORTER_PRJ_C_FY2017_052.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_051.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_050.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_049.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_048.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_047.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_046.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_045.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_044.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_043.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_042.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_041.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_040.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_039.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_038.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_037.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_036.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_035.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_034.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_033.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_032.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_031.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_030.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_029.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_028.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_027.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_026.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_025.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_024.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_023.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_022.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_021.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_020.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_019.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_018.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_017.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_016.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_015.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_014.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_013.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_012.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_011.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_010.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_009.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_008.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_007.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_006.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_005.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_004.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_002.csv","PRJ_csv/RePORTER_PRJ_C_FY2017_001.csv"]



#csv_PRJ_files= ["seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_052.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_051.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_050.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_049.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_048.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_047.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_046.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_045.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_044.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_043.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_042.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_041.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_040.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_039.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_038.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_037.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_036.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_035.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_034.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_033.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_032.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_031.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_030.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_029.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_028.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_027.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_026.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_025.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_024.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_023.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_022.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_021.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_020.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_019.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_018.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_017.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_016.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_015.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_014.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_013.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_012.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_011.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_010.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_009.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_008.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_007.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_006.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_005.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_004.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_002.csv","seed_data/PRJ_csv/RePORTER_PRJ_C_FY2017_001.csv"]


# Note: "seed_data/PRJABS_csv/RePORTER_PRJ_C_FY2017_003.csv" is not online Jan/7/2018

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


for csv_PRJ_file in csv_PRJ_files:

    dataReader = csv.reader(open(csv_PRJ_file, encoding = "ISO-8859-1"), delimiter=',', quotechar='"')

    index = -1
    success = 0
    for row in dataReader:
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

            grant.org_name = row[24]

            grant.org_state = row[25]

            grant.org_zipcode = row[26]

            grant.phr = row[27]

            grant.pi_ids = row[28]

            grant.pi_name= make_array_feild(row[29])

            # grant.program_officer_name = row[30]

            # grant.project_start = row[31]

            # grant.project_end = row[32]

            # print(row[34])
            grant.project_terms = row[33]

            # print(row[35])
            grant.project_title = row[34]

            # grant.serial_number = row[35]

            # print(row[37])
            grant.study_section = row[36]

            # print(row[38])
            grant.study_section_name = row[37]

            # print(row[39])
            grant.subproject_id = row[38]

            # grant.suffix = row[39]

            # print(row[40])
            if row[40] == "":
                grant.support_year = None
            else:
                grant.support_year = row[40]

            # print(row[42])
            if row[41] == "":
                grant.direct_cost_amt = None
            else:
                grant.direct_cost_amt = row[41]

                # print(row[43])
            if row[42] == "":
                grant.indirect_cost_amt = None
            else:
                grant.indirect_cost_amt = row[42]

        # print(row[44])
            if row[43] == "":
                grant.total_cost = None;
            else:
                grant.total_cost = row[43]

        # print(row[45])
            if row[44] == "":
                grant.total_cost_sub_project = None
            else:
                grant.total_cost_sub_project = row[44]

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


csv_PRJABS_files =["PRJABS_csv/RePORTER_PRJABS_C_FY2017_052.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_051.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_050.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_049.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_048.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_047.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_046.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_045.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_044.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_043.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_042.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_041.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_040.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_039.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_038.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_037.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_036.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_035.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_034.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_033.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_032.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_031.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_030.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_029.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_028.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_027.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_026.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_025.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_024.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_023.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_022.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_021.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_020.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_019.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_018.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_017.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_016.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_015.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_014.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_013.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_012.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_011.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_010.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_009.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_008.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_007.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_006.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_005.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_004.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_002.csv","PRJABS_csv/RePORTER_PRJABS_C_FY2017_001.csv"]



# csv_PRJABS_files=["seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_004.csv"]
# csv_PRJABS_files =["seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_052.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_051.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_050.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_049.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_048.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_047.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_046.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_045.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_044.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_043.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_042.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_041.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_040.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_039.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_038.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_037.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_036.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_035.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_034.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_033.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_032.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_031.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_030.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_029.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_028.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_027.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_026.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_025.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_024.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_023.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_022.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_021.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_020.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_019.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_018.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_017.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_016.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_015.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_014.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_013.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_012.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_011.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_010.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_009.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_008.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_007.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_006.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_005.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_004.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_002.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_001.csv"]

# Note: "seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2017_003.csv" is not online Jan/7/2018

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

            except:
                print(f"no grant with application id {row[0]}")

            try:
                Grant.clean_fields(focal)
            except ValidationError as e:
                print(e)

            try:
                focal.save()
                success +=1
            # print(f"saved application_id {grant.application_id}")
            # print(f"saved {success} out of {index}")
            except:
                print(f"there was a problem with row {index}, application id: {row[0]}, file: {csv_PRJABS_file}")
                # print(f"saved {success} out of {index}")
    print(f"file {csv_PRJABS_file} saved {success} out of {index}")
