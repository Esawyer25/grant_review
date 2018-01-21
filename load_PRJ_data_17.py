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

                except:
                    print('there was a problem with row')
            print('i have reached the end of a row')
                # print(f"saved {success} out of {index}")
    os.remove(csv_file_path)
    print('I HAVE REACHED THE END OF A FILE')

groups= ['C', 'G', 'H', 'L', 'O', 'P', 'T', 'U', 'V', 'I', 'M', 'N', 'X', 'Y', 'Z']
for code in groups:
    temp = Grant.objects.filter(activity__startswith = code)
    print(f'deleting {temp.count()} grants starting with {code}')
    temp.delete()

    #IK3 = Non-DHHS Nursing Research Initiative
activity_codes = ["IK3", 'R24', 'KL2', 'R4', 'R18', 'R13', 'R24', 'RM1']
for code in activity_codes:
    temp = Grant.objects.filter(activity = code)
    temp.delete()


zip_files = ["seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_052.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_051.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_050.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_049.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_048.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_047.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_046.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_045.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_044.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_043.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_042.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_041.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_040.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_039.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_038.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_037.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_036.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_035.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_034.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_033.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_032.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_031.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_030.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_029.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_028.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_027.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_026.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_025.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_024.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_023.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_022.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_021.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_020.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_019.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_018.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_017.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_016.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_015.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_014.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_013.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_012.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_011.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_010.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_009.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_008.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_007.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_006.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_005.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_004.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_002.zip","seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_001.zip"]

# Note: "seed_data/zipfiles_PRJ_ABS/RePORTER_PRJABS_C_FY2017_003.zip" is not online Jan/7/2018

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
                abstract_text = row[1]
                if abstract_text[0] == '?':
                    abstract_text = abstract_text[1:]

                string = 'Abstract: DESCRIPTION (provided by applicant): '
                if string in abstract_text:
                     abstract_text = abstract_text.replace(string, '')

                if string in abstract_text:
                     abstract_text = abstract_text.replace(string, '')

                focal.abstract_text = abstract_text

                try:
                    Grant.clean_fields(focal)
                except ValidationError as e:
                    print(e)

            except:
                pass

            try:
                focal.save()
                print('saved a grant abstrat')
            # print(f"saved application_id {grant.application_id}")
            # print(f"saved {success} out of {index}")
            except:
                pass
                # print(f'there was a problem with row {index}, application id: {row[0]}, file: {csv_file_path}'')
                # print(f"saved {success} out of {index}")
    # print(f'file {csv_file_path} saved {success} out of {index}'')

    os.remove(csv_file_path)
