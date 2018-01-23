from django.db import models
from django.contrib.postgres.fields import ArrayField
import json
from jsonfield import JSONField

COMMON_WORDS_SET = set(['', 'What', 'Had', 'Has', 'Be', 'We', 'His', 'Her', 'Not', 'Now', 'By', 'On', 'Did', 'Of', 'She', 'Can', 'Or', 'Day', 'Are', 'Go', 'Find', 'From', 'For', 'Long', 'Which', 'More', 'That', 'Water', 'Part', 'Than', 'He', 'Made', 'Word', 'Look', 'This', 'Could', 'Up', 'Were', 'My', 'First', 'People', 'Use', 'Said', 'Would', 'No', 'Make', 'There', 'When', 'Two', 'Their', 'Way', 'Was', 'Get', 'But', 'Come', 'These', 'So', 'Been', 'Time', 'And', 'How', 'Into', 'Number', 'Him', 'Down', 'See', 'Your', 'Out', 'Write', 'To', 'Other', 'Call', 'You', 'An', 'Each', 'Do', 'Them', 'Oil', 'May', 'Who', 'They', 'Many', 'With', 'A', 'About', 'Like', 'Then', 'I', 'Will', 'The', 'All', 'Is', 'Some', 'It', 'One', 'As', 'At', 'Have', 'In', 'Its', 'If', 'Dr', 'And/or', 'May','To','Project', 'From','On', 'Our', 'Such'])

COMMON_PUNTUATION =set(['.','?',',', ';', ':' '1)','2)','3)','4)', ')', ')', '#1', ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ', ' = '])

#Explanation of field names here: https://exporter.nih.gov/about.aspx
class Grant(models.Model):
    application_id = models.CharField(max_length=12, null=True, blank=True, unique=True)

    abstract_text = models.TextField(max_length=6000, null=True, blank=True)
    # need to get this from the abstract doc

    activity = models.CharField(max_length=3, null=True, blank=True)
    # A 3-character code ex. RO1 (https://grants.nih.gov/grants/funding/ac_search_results.htm)

    administering_ic = models.CharField(max_length=2, null=True, blank=True)
    # Administering Institute or Center

    application_type = models.CharField(max_length=1, null=True, blank=True)

    # arra_funded = models.CharField(max_length=1, null=True)

    # award_notice_date = models.DateField(max_length=16, null=True)

    budget_start = models.DateField(max_length=16, null=True, blank=True)

    budget_end = models.DateField(max_length=16, null=True, blank=True)

    # cfda_code = models.CharField(max_length=10, null=True)

    core_project_num = models.CharField(max_length=30, null=True, blank=True)

    ed_inst_type = models.CharField(max_length=100, null=True, blank=True)

    # foa_number = models.CharField(max_length=50, null=True)

    full_project_num = models.CharField(max_length=50, null=True, blank=True)

    funding_ics = models.CharField(max_length=300, null=True, blank=True)

    funding_mechanism = models.CharField(max_length=150, null=True, blank=True)

    FY = models.IntegerField(null=True, blank=True)

    ic_name = models.CharField(max_length=264, null=True, blank=True)

    # nih_spending_cats = models.CharField(max_length=528, null=True)

    org_city = models.CharField(max_length=64, null=True, blank=True)

    org_country = models.CharField(max_length=128, null=True, blank=True)

    org_dept = models.CharField(max_length=128, null=True, blank=True)

    org_district = models.IntegerField(null=True, blank=True)

    # org_duns = models.IntegerField(null=True)

    # org_fips = models.IntegerField(null=True)

    # org_ipf_code = models.IntegerField(null=True)

    org_name = models.CharField(max_length=100, null=True, blank=True)

    org_state = models.CharField(max_length=10, null=True, blank=True)

    org_zipcode = models.CharField(max_length=20, null=True, blank=True)

    phr = models.TextField(max_length=1000, null=True, blank=True)

    pi_ids = models.CharField(max_length=264, null=True, blank=True)

    pi_name= models.CharField(max_length=500, null=True, blank=True)

    # pi_name = ArrayField(models.CharField(max_length=500, null=True, blank=True), null=True)

    # program_officer_name = models.CharField(max_length=128, null=True)

    # project_start = models.CharField(max_length=128, null=True)

    # project_end = models.DateField(null=True)

    project_terms = models.TextField(max_length=3000, null=True, blank=True)

    project_title = models.TextField(max_length=500, null=True, blank=True)

    # serial_number = models.CharField(max_length=10, null=True)

    study_section = models.CharField(max_length=10, null=True, blank=True)

    study_section_name = models.TextField(max_length=200, null=True, blank=True)

    subproject_id = models.CharField(max_length=16, null=True, blank=True)

    suffix = models.CharField(max_length=16, null=True, blank=True)

    support_year = models.IntegerField(null=True, blank=True)

    direct_cost_amt = models.IntegerField(null=True, blank=True)
#should this default to zero if empty?
    indirect_cost_amt = models.IntegerField(null=True, blank=True)

    total_cost = models.IntegerField(null=True, blank=True)

    total_cost_sub_project = models.IntegerField(null=True, blank=True)

    total_funding_of_core_numb = models.IntegerField(null=True, blank=True)

    total_direct_of_core_numb = models.IntegerField(null=True, blank=True)

    total_indirect_of_core_numb = models.IntegerField(null=True, blank=True)
    # related_grants = ArrayField(models.CharField(max_length=500, blank=True), null=True, blank=True)

    # num_of_papers = models.IntegerField(null=True, blank=True)
    #
    # num_of_papers = Grant_Publication.objects.get(project_num= self.core_project_num).count()
    def make_data_structure(self):
        abstract = self.abstract_text
        for punt in COMMON_PUNTUATION:
            abstract = abstract.replace(punt, "")

        abstract = abstract.split(" ")
        abstract_list = []
        for word in abstract:
            abstract_list.append(word.capitalize())

        remove_list = []
        for word in abstract_list:
            if word in COMMON_WORDS_SET:
                remove_list.append(word)

        for word in remove_list:
            abstract_list.remove(word)

        ab_dict = {}
        for word in abstract_list:
            word = word.capitalize()
            try:
                value = ab_dict[word.capitalize()]
            except KeyError:
                value = None
            if value:
                ab_dict[word.capitalize()] += (7)
            else:
                ab_dict[word.capitalize()] = (7)

        data = []
        for word, repeats in ab_dict.items():
            if repeats > 7:
                temp={"text":word, "size": repeats}
                data.append(temp)
        return json.dumps(data)

    def small_data_structure(self):
        abstract = self.abstract_text

        for punt in COMMON_PUNTUATION:
            abstract = abstract.replace(punt, "")

        abstract = abstract.split(" ")
        abstract_list = []
        for word in abstract:
            abstract_list.append(word.capitalize())

        remove_list = []
        for word in abstract_list:
            if word in COMMON_WORDS_SET:
                remove_list.append(word)

        for word in remove_list:
            abstract_list.remove(word)

        ab_dict = {}
        for word in abstract_list:
            word = word.capitalize()
            try:
                value = ab_dict[word]
            except KeyError:
                value = None
            if value:
                ab_dict[word] += (4)
            else:
                ab_dict[word] = (4)

        # for word, repeats in ab_dict.items():
        #     if repeats == 1:
        #         ad_dict.pop(word,0)

        data = []
        for word, repeats in ab_dict.items():
            if repeats > 4:
                temp={"text":word, "size": repeats}
                data.append(temp)
        return json.dumps(data)


    def list_of_papers(self):
        paper_list = Grant_Publication.objects.filter(project_number= self.core_project_num)
        return paper_list

#could I save this as an attribute instead of calculating it every time
    def number_of_papers(self):
        paper_list = Grant_Publication.objects.filter(project_number= self.core_project_num)
        pmids = []
        count = 0
        for paper in paper_list:
            if paper.pmid in pmids:
                pass
            else:
                pmids.append(paper.pmid)
                count +=1
        paper_number = count
        return paper_number


    def __str__(self):
        return self.application_id

    class Meta:
        ordering = ['-total_funding_of_core_numb','-FY']

class Grant_Publication(models.Model):
    pmid = models.CharField(max_length=10, null=True)
    project_number = models.CharField(max_length=12, null=True)

    # def __str__(self):
    #     return self.pmid

class Publication(models.Model):
    pmid = models.CharField(max_length=16, null=True, blank=True, unique=True)

    title = models.CharField(max_length=500, null=True, blank=True)

    abstract = models.TextField(max_length=6000, null=True, blank=True)

    journal = models.CharField(max_length=500, null=True, blank=True)

    affiliation= models.TextField(max_length=5000, null=True, blank=True)

    # authors = models.CharField(max_length=1000, null=True, blank=True)

    authors = ArrayField(models.CharField(max_length=500, null=True, blank=True), null=True)

    year = models.IntegerField(null=True, blank=True)

    score = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)

    class Meta:
        ordering = ['-year',]

    def small_data_structure(self):
        abstract = self.abstract

        for punt in COMMON_PUNTUATION:
            abstract = abstract.replace(punt, "")

        abstract = abstract.split(" ")
        abstract_list = []
        for word in abstract:
            abstract_list.append(word.capitalize())

        remove_list = []
        for word in abstract_list:
            if word in COMMON_WORDS_SET:
                remove_list.append(word)

        for word in remove_list:
            abstract_list.remove(word)

        ab_dict = {}
        for word in abstract_list:
            try:
                value = ab_dict[word.capitalize()]
            except KeyError:
                value = None
            if value:
                ab_dict[word.capitalize()] += (4)
            else:
                ab_dict[word.capitalize()] = (4)

        # for word, repeats in ab_dict.items():
        #     if repeats == 1:
        #         ad_dict.pop(word,0)

        data = []
        for word, repeats in ab_dict.items():
            if repeats > 4:
                temp={"text":word, "size": repeats}
                data.append(temp)

        return json.dumps(data)

    def __str__(self):
        return self.pmid # change this to something more sensible later


class Keyword(models.Model):
    keyword = models.CharField(max_length=100, null=True, unique=True)

    grants = models.ManyToManyField(Grant)

    searches = models.IntegerField(null=True, blank=True)

    states_dict = JSONField(null=True, blank=True)

    states_top_inst = JSONField(null=True, blank=True)

    scatterplot_array = JSONField(null=True, blank=True)

    grant_count = models.IntegerField(null=True, blank=True)

    grant_total_cost = models.IntegerField(null=True, blank=True)

    grant_direct_cost = models.IntegerField(null=True, blank=True)

    grant_indirect_cost = models.IntegerField(null=True, blank=True)

    grant_count_18 = models.IntegerField(null=True, blank=True)

    grant_total_cost_18 = models.IntegerField(null=True, blank=True)

    grant_direct_cost_18 = models.IntegerField(null=True, blank=True)

    grant_indirect_cost_18 = models.IntegerField(null=True, blank=True)

    grant_count_17 = models.IntegerField(null=True, blank=True)

    grant_total_cost_17 = models.IntegerField(null=True, blank=True)

    grant_direct_cost_17 = models.IntegerField(null=True, blank=True)

    grant_indirect_cost_17 = models.IntegerField(null=True, blank=True)

    grant_count_16 = models.IntegerField(null=True, blank=True)

    grant_total_cost_16 = models.IntegerField(null=True, blank=True)

    grant_direct_cost_16 = models.IntegerField(null=True, blank=True)

    grant_indirect_cost_16 = models.IntegerField(null=True, blank=True)

    grant_count_15 = models.IntegerField(null=True, blank=True)

    grant_total_cost_15 = models.IntegerField(null=True, blank=True)

    grant_direct_cost_15 = models.IntegerField(null=True, blank=True)

    grant_indirect_cost_15 = models.IntegerField(null=True, blank=True)

    grant_indirect_cost_16 = models.IntegerField(null=True, blank=True)

    grant_count_14 = models.IntegerField(null=True, blank=True)

    grant_total_cost_14 = models.IntegerField(null=True, blank=True)

    grant_direct_cost_14 = models.IntegerField(null=True, blank=True)

    grant_indirect_cost_14 = models.IntegerField(null=True, blank=True)

    f31_count= models.IntegerField(null=True, blank=True)

    f31_total_cost= models.IntegerField(null=True, blank=True)

    f32_count= models.IntegerField(null=True, blank=True)

    f32_total_cost= models.IntegerField(null=True, blank=True)

    k99_count= models.IntegerField(null=True, blank=True)

    k99_total_cost= models.IntegerField(null=True, blank=True)

    r00_count= models.IntegerField(null=True, blank=True)

    r00_total_cost= models.IntegerField(null=True, blank=True)

    r01_count= models.IntegerField(null=True, blank=True)

    r01_total_cost= models.IntegerField(null=True, blank=True)

    r35_count= models.IntegerField(null=True, blank=True)

    r35_total_cost= models.IntegerField(null=True, blank=True)

    dp1_count= models.IntegerField(null=True, blank=True)

    dp1_total_cost= models.IntegerField(null=True, blank=True)

    dp2_count= models.IntegerField(null=True, blank=True)

    dp2_total_cost= models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.keyword

    class Meta:
        ordering = ['-searches',]

class Related_grant(models.Model):
    core_project_num = models.CharField(max_length=30, null=True, blank=True, unique = True)

    grants = models.ManyToManyField(Grant)

    total_funding_of_core_numb = models.IntegerField(null=True, blank=True)

    total_direct_of_core_numb = models.IntegerField(null=True, blank=True)

    total_indirect_of_core_numb = models.IntegerField(null=True, blank=True)

    # def __str__(self):
    #     return self.core_project_num



# Create your models here.
