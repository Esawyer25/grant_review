from django.core.exceptions import ValidationError
from CapApp.models import Grant, Grant_Publication, Keyword
import datetime

class Add_Keyword:
    def create_keyword(word, grant_list, searches=0):
        a = datetime.datetime.now()

        new_word = Keyword()
        new_word.keyword = word
        new_word.searches = searches
        try:
            Keyword.full_clean(new_word)
        except ValidationError as e:
            print(e)

        try:
            new_word.save()
        except:
            print(f"there was a problem saving with Keyword {word}")

        grant_list =Grant.objects.filter(project_terms__search=word)
        for grant in grant_list:
            new_word.grants.add(grant)

        b = datetime.datetime.now()
        print(f'time in to create new keyword = {b-a}')

    def make_short_list(grant_list_long):
        if grant_list_long.count() > 100:
            grant_list_short = grant_list_long[0:100]
        else:
            grant_list_short = grant_list_long
        return grant_list_short

    def incriment_keyword_searches(keyword_object):
        keyword_object.searches += 1

        try:
            Keyword.full_clean(keyword_object)
        except ValidationError as e:
            print(e)
        try:
            keyword_object.save()
        except:
            print(f"there was a problem saving with Keyword {query}")


class Stats:
    def find_cost(list):
        total_cost = 0
        direct_cost = 0
        indirect_cost = 0
        # if list.count() > 0:
        for item in list:
            if item.total_cost:
                if item.total_cost:
                     total_cost += item.total_cost
                if item.direct_cost_amt:
                    direct_cost += item.direct_cost_amt
                if item.indirect_cost_amt:
                    indirect_cost += item.indirect_cost_amt
        return {'total_cost':total_cost, 'direct_cost':direct_cost, 'indirect_cost':indirect_cost}

    def divide_by_FY(grant_list):
        # years = range(1985,2018,1)
        years = range(2015, 2018, 1)
        grants_by_year={}
        for year in years:
            year_str = str(year)
            grants_by_year[year_str] = grant_list.filter(FY=year)
        return grants_by_year


    def return_stats_by_year(grant_list, query):

        #make a dict of all the stats divided by FY
        #{totals: {grant_total_cost: xx, grant_indirect_cost:xx...}, 1985: {grant_total_cost = xx,...}}
        grant_dict = Stats.divide_by_FY(grant_list)
        stats_dict = {}
        stats_dict['totals'] = Stats.return_stats_dict(grant_list, query)
        years = range(2015, 2018, 1)
        for year in years:
            year_str = str(year)
            stats_dict[year_str] = Stats.return_stats_dict(grant_dict[year_str], query)
        return stats_dict


    def return_stats_dict(grant_list, query):


        grant1= grant_list
        a = datetime.datetime.now()
        grant_count = grant_list.count()
        costs = Stats.find_cost(grant_list)
        grant_total_cost = costs['total_cost']
        grant_indirect_cost = costs['indirect_cost']
        grant_direct_cost = costs['direct_cost']

        # #make dict where grants are divided by FY
        # #ex. {'2015': <QuerySet []>, '2016': <QuerySet [<Grant: 9082664>, <Grant: 9114892>]}
        # grant_list = Stats.divide_by_FY(grant_list)
        # print(grant_list)

        # Individual Predoctoral NRSA for M.D./Ph.D. Fellowships
        grant_f30 = grant_list.filter(activity="F30")
        grant_f30 = grant_list.filter(activity="F30")
        costs = Stats.find_cost(grant_f30)
        f30_total_cost = costs['total_cost']
        f30_count = grant_f30.count()

        # Predoctoral Individual National Research Service Award
        grant_f31 = grant_list.filter(activity="F31")
        f31_total_cost = Stats.find_cost(grant_f31)
        costs = Stats.find_cost(grant_f31)
        f31_total_cost = costs['total_cost']
        f31_count = grant_f31.count()

        # Postdoctoral Individual National Research Service Award
        grant_f32 = grant_list.filter(activity="F32")
        f32_total_cost = Stats.find_cost(grant_f32)
        costs = Stats.find_cost(grant_f32)
        f32_total_cost = costs['total_cost']
        f32_count = grant_f32.count()

        #Career Transition Award
        grant_k99 = grant_list.filter(activity="K99")
        k99_total_cost = Stats.find_cost(grant_k99)
        costs = Stats.find_cost(grant_k99)
        k99_total_cost = costs['total_cost']
        k99_count = grant_k99.count()

        #Research Transition Award
        grant_r00 = grant_list.filter(activity="R00")
        r00_total_cost = Stats.find_cost(grant_r00)
        costs = Stats.find_cost(grant_r00)
        r00_total_cost = costs['total_cost']
        r00_count = grant_r00.count()

        #Research Project
        grant_r01 = grant_list.filter(activity="R01")
        r01_total_cost = Stats.find_cost(grant_r01)
        costs = Stats.find_cost(grant_r01)
        r01_total_cost = costs['total_cost']
        r01_count = grant_r01.count

        #Outstanding Investigator Award
        grant_r35 = grant_list.filter(activity="R35")
        r35_total_cost = Stats.find_cost(grant_r35)
        costs = Stats.find_cost(grant_r35)
        r35_total_cost = costs['total_cost']
        r35_count = grant_r35.count

        #NIH Director’s Pioneer Award (NDPA)
        grant_dp1 = grant_list.filter(activity="DP1")
        dp1_total_cost = Stats.find_cost(grant_dp1)
        costs = Stats.find_cost(grant_dp1)
        dp1_total_cost = costs['total_cost']
        dp1_count = grant_dp1.count

        #NIH Director’s New Innovator Award
        grant_dp2 =grant_list.filter(activity="DP2")
        dp2_total_cost = Stats.find_cost(grant_dp2)
        costs = Stats.find_cost(grant_dp2)
        dp2_total_cost = costs['total_cost']
        dp2_count = grant_dp1.count

        b = datetime.datetime.now()
        print(f'time elapsed in stats: {b-a}')
        grant_stats_dict={'query': query,'grant_count': grant_count,'grant_total_cost':grant_total_cost,'grant_direct_cost':grant_direct_cost,'grant_indirect_cost':grant_indirect_cost,'f30_count':f30_count,'f30_total_cost':f30_total_cost,'f31_count':f31_count,'f31_total_cost':f31_total_cost,'f32_count':f32_count,'f32_total_cost':f32_total_cost,'k99_count':k99_count,'k99_total_cost':k99_total_cost,'r00_count':r00_count,'r00_total_cost':r00_total_cost,'r01_count':r01_count,'r01_total_cost':r01_total_cost,'r35_count':r35_count,'r35_total_cost':r35_total_cost,'dp1_count':dp1_count,'dp1_total_cost':dp1_total_cost,'dp2_count':dp2_count,'dp2_total_cost':dp2_total_cost}

        return grant_stats_dict
