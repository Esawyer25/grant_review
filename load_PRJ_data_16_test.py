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
    array= {}
    for item in list:
        item = item.title
        if item == "":
            list.remove(item)
        if "(contact)" in item:
            item.replace("(contact)","*")
    array = set(list)
    return array

import zipfile

zip_files = ['seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2016.zip', 'seed_data/zipfiles_PRJ/RePORTER_PRJ_C_FY2015.zip']

for zip_file in zip_files:
    zf = zipfile.ZipFile(zip_file, 'r')
    for zi in zf.infolist():
        csv_file_path= zf.extract(zi)
        print(csv_file_path)
        zf.close()

# os.remove(csv_file_path)

        dataReader = csv.reader(open(csv_file_path, encoding = "ISO-8859-1"), delimiter=',', quotechar='"')

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
                grant.pi_name= row[30]

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

                grant.suffix = row[40]

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
                    print(f"there was a problem with row {index}, application id: {row[0]}, file {csv_file_path}")
                    # print(f"saved {success} out of {index}")
        print(f"{csv_file_path} saved {success} out of {index}")

        print(f'removing {csv_file_path}')
        os.remove(csv_file_path)

# C - Research Construction Programs (e.g. C06)
# D - Training Projects (e.g. D43)
# F - Fellowship Programs (e.g. F31, F32)
# K - Research Career Programs (e.g. K08, K24)
# M - General Clinical Research Centers Programs (e.g. M01)
# N - Research and Development-Related Contracts (e.g. N01, N02)
# P - Research Program Projects and Centers (e.g. P30, P50)
# R - Research Projects (e.g. R01, R21)
# S - Research-Related Programs (e.g. S10)
# T - Training Programs (e.g. T32, T37)
# U - Cooperative Agreements (e.g. U01, U09)
# Y - Inter-Agency/Intra-Agency Agreements (e.g. Y01, Y02)
# Z - Intramural Research (e.g. Z01)
groups= ["C", "G", "H", "L", "O", "P", "T", "U", "V", "I", "M", "N", "X" "Y,", "Z", " R24", "KL2", "R4", "R18", "R13", "R24", "RM1"]
for code in groups:
    temp = Grant.objects.filter(activity__startswith = code)
    print(f'deleting {temp.count()} grants starting with {code}')
    temp.delete()

    #IK3 = Non-DHHS Nursing Research Initiative
# activity_codes = ["IK3"]
# for code in activity_codes:
#     temp = Grant.objects.filter(activity = code)
#     print(f'deleting {temp.count()} {code} grants')
#     temp.delete()

# csv_PRJABS_files =["seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2015.csv","seed_data/PRJABS_csv/RePORTER_PRJABS_C_FY2016.csv"]

zip_files = [
'seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2016.zip',
'seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2015.zip',]

# zip_files = ['zipfiles_PRJ_ABS/RePORTER_PRJ_C_FY2016.zip', 'zipfiles_PRJ_ABS/RePORTER_PRJ_C_FY2015.zip']

for zip_file in zip_files:
    zf = zipfile.ZipFile(zip_file, 'r')
    for zi in zf.infolist():
        csv_file_path= zf.extract(zi)
        print(csv_file_path)
        zf.close()

    dataReader = csv.reader(open(csv_file_path, encoding = "ISO-8859-1"), delimiter=',', quotechar='"')

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

                string = "Abstract: DESCRIPTION (provided by applicant): "
                if string in abstract_text:
                     abstract_text = abstract_text.replace(string, "")

                # if string = "PROJECT SUMMARY/ ABSTRACT DESCRIPTION: See instructions. State the application's broad, long-term objectives and specific aims, making reference to the health relatedness of the project (i.e., relevance to the mission of the agency). Describe concisely the research design and methods for achieving these goals. Describe the rationale and techniques you will use to pursue these goals."
                #
                # if string in abstract_text:
                #      abstract_text = abstract_text.replace(string, "")
                #
                # focal.abstract_text = abstract_text
                #
                # string ="In addition, in two or three sentences, describe in plain, lay language the relevance of this research to public health. If the application is funded, this description, as is, will become public information. Therefore, do not include proprietary/confidential information. DO NOT EXCEED THE SPACE PROVIDED."

                if string in abstract_text:
                     abstract_text = abstract_text.replace(string, "")

                focal.abstract_text = abstract_text

                try:
                    Grant.clean_fields(focal)
                except ValidationError as e:
                    print(e)

            except:
                pass


            try:
                focal.save()
                success +=1
            # print(f"saved application_id {grant.application_id}")
            # print(f"saved {success} out of {index}")
            except:
                print(f"there was a problem with row {index}, application id: {row[0]}, file: {csv_file_path}")
                # print(f"saved {success} out of {index}")
    print(f"file {csv_file_path} saved {success} out of {index}")

    os.remove(csv_file_path)
