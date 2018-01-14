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


str = '9116920,R01,HG,4,N,7/15/2016,8/1/2016,7/31/2017,172,R01HG007407,SCHOOLS OF ARTS AND SCIENCES,RFA-HG-10-012,4R01HG007407-04,NHGRI:509472\,Non-SBIR/STTR RPGs,2016,NATIONAL HUMAN GENOME RESEARCH INSTITUTE,Bioengineering; Genetics; HIV/AIDS; Human Genome; Nanotechnology; ,CHAPEL HILL,UNITED STATES,CHEMISTRY,4,608195277,US,578206,UNIV OF NORTH CAROLINA CHAPEL HILL,NC,275990001,"PUBLIC HEALTH RELEVANCE: Project Narrative:  We propose to develop a nanofluidic platform for the high-throughput restriction mapping of complete genomes. This platform consists of monolithically integrated fluidics for the extraction of chromosomal DNA from cells, its digestion by restriction endonucleases in a long nanochannel, and the high- resolution sizing of ordered restriction fragments. In contrast to other nanochannel-based approaches, we do not rely on the imaging of highly confined and elongated DNA molecules.",1882956; ,"RAMSEY, JOHN MICHAEL;","SMITH, MICHAEL",9/1/2013,7/31/2017,base; Benchmarking; Bioinformatics; Caliber; Cells; cost; Data; density; Detection; Devices; Diagnostic; Digestion; Disease susceptibility; DNA; DNA Integration; DNA Restriction Enzymes; Dyes; electric field; Electrostatics; Elements; Ensure; Enzymes; Escherichia coli; Fluorescence; Future; Genome; Genomic DNA; Goals; Health; Image; Injection of therapeutic agent; Label; Lasers; Maps; member; Methods; nanochannel; nanofluidic; next generation sequencing; Organism; Physiologic pulse; Play; prevent; Probability; Protocols documentation; Reaction; reference genome; Repetitive Sequence; Resolution; restriction enzyme; Restriction Mapping; Role; Saccharomyces cerevisiae; scaffold; Site; Spottings; Techniques; Therapeutic; Variant; ,Nanofluidic Platforms for High Resolution Mapping of Genomic DNA,7407,ZHG1,Special Emphasis Panel ,,,4,340539,168933,509472,'




str = str.split(',', 25)
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
print(f'project_terms {project_terms}')
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
    support_year == None
else:
    support_year = str[9]
print(support_year)

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





# print(str)
