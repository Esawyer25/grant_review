from django.core.exceptions import ValidationError
from CapApp.models import Grant, Grant_Publication, Keyword, Publication, Related_grant
import datetime
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from CapApp.pubmed import Pubmed

class Publication_methods:
    def return_list_of_publications(list_papers):
        pubs = []
        pmids = []
        for paper in list_papers:
            if paper.pmid in pmids:
                pass
            else:
                pmids.append(paper.pmid)
                pub = Publication_methods.return_pub(paper)
                pubs.append(pub)
        return (pubs)

    def return_pub(paper):
        temp = None
        print(f'this is the pmid{paper.pmid}')
        try:
            Publication.objects.get(pmid = paper.pmid)
            temp = Publication.objects.get(pmid = paper.pmid)
            # print(temp)
            pub = temp
        except:
            temp = (Pubmed.parse_xml_web(paper.pmid, sleep=0.5, save_xml=False))
            # print(temp)
            pub = Publication()
            pub.pmid = paper.pmid
            pub.title = temp['title']
            pub.abstract = temp['abstract']
            pub.journal = temp['journal']
            pub.affiliation = temp['affiliation']

            list = temp['authors'].split(";")
            for item in list:
                item = item.title
                if item == "":
                    list.remove(item)

            pub.authors = list
            pub.year = temp['year']
            try:
                Publication.full_clean(pub)
            except ValidationError as e:
                print(e)
            try:
                pub.save()
                print(f'I saved this pub pmid: {pub.pmid}')
            except:
                print(f"there was a problem saving publication {paper.pmid}")
        return(pub)



class Score:
    def return_all_scores():
        pubs = Publication.objects.all()
        score_array = []
        for pub in pubs:
            if pub.score:
                score_array.append(str(pub.score))
            else:
                pass

        return json.dumps(score_array)

    def return_focal_scores(pubs):
        score_array = []
        for pub in pubs:
            if pub.score:
                temp = {'title': pub.title, 'score': str(pub.score)}
                score_array.append(temp)
            else:
                pass
        return json.dumps(score_array)

    def return_n():
        pubs = Publication.objects.all()
        total = 0
        for pub in pubs:
            if pub.score:
                total += 1
            else:
                pass
        return  json.dumps(total)

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
#is it better to do terms or abstract?
        grant_list =Grant.objects.filter(project_terms__search=word)
        grant_list = Add_Keyword.no_repeats(grant_list)
        for grant in grant_list:
            new_word.grants.add(grant)
        print('I have added the grants')

        Add_Keyword.set_keyword_stats(new_word, grant_list)

        state_dict = Stats.states(grant_list)
        new_word.states_dict = state_dict

        states_top_inst = Stats.top_institutions(grant_list)
        new_word.states_top_inst = states_top_inst

        scatterplot_array = Add_Keyword.cost_scatterplot(grant_list)

        new_word.scatterplot_array = scatterplot_array
        try:
            new_word.save()
            print('I saved the states_dict')
        except:
            print(f"there was a problem saving with state_dict")


        b = datetime.datetime.now()
        print(f'time in to create new keyword = {b-a}')
        return new_word

    def cost_scatterplot(grant_list):
        #Make scatter plot array for papers vs. funding
        scatterplot_array =[]
        for grant in grant_list:
            if grant.FY == 2018 and grant.support_year < 5 and grant.support_year > 2:
                all_years = True
            elif grant.FY == 2017 and grant.support_year < 4 and grant.support_year > 1:
                all_years = True
            elif grant.FY == 2016 and grant.support_year < 3:
                all_years = True
            elif grant.FY == 2015 and grant.support_year < 2:
                all_years = True
            elif grant.FY == 2014 and grant.support_year < 1:
                all_years = True
            else:
                all_years = None

            if all_years:
                temp ={}
                temp['number'] = grant.number_of_papers()
                temp['total_cost'] = grant.total_funding_of_core_numb
                temp['core_project_num'] =grant.core_project_num
                temp['support_year'] = grant.support_year
                temp['title'] = grant.project_title
                scatterplot_array.append(temp)
            else:
                pass
        scatterplot_array = json.dumps(scatterplot_array)
        return scatterplot_array

    def set_keyword_stats(new_word, grant_list):
        #grant_list = new_word.grants.all()
        print(f'this is my grant_list {grant_list}')
        print(f'in set keyword stats, this is my word {new_word.keyword}')
        grant_stats = Stats.return_stats_by_year(grant_list, new_word.keyword)
        print(f'these are the grant stats{grant_stats}')

        #see if counting in thousands makes the numbers small enough

        new_word.grant_count = grant_stats['totals']['grant_count']

        new_word.grant_total_cost = round(grant_stats['totals']['grant_total_cost'],-3)/1000
        print('this is the total cost')
        print (new_word.grant_total_cost)

        new_word.grant_direct_cost = round(grant_stats['totals']['grant_direct_cost'],-3)/1000
        print( f'this is the direct cost {new_word.grant_direct_cost}')

        new_word.grant_indirect_cost = round(grant_stats['totals']['grant_indirect_cost'],-3)/1000
        print( f'this is the indirect cost {new_word.grant_indirect_cost}')

        new_word.grant_count_18 = grant_stats['2018']['grant_count']

        new_word.grant_total_cost_18 = round(grant_stats['2018']['grant_total_cost']-3)/1000

        new_word.grant_direct_cost_18 = round(grant_stats['2018']['grant_direct_cost']-3)/1000

        new_word.grant_indirect_cost_18 = round(grant_stats['2018']['grant_indirect_cost']-3)/1000

        new_word.grant_count_17 = grant_stats['2017']['grant_count']

        new_word.grant_total_cost_17 = round(grant_stats['2017']['grant_total_cost'],-3)/1000

        new_word.grant_direct_cost_17 = round(grant_stats['2017']['grant_direct_cost'],-3)/1000

        new_word.grant_indirect_cost_17 = round(grant_stats['2017']['grant_indirect_cost'],-3)/1000

        new_word.grant_count_16 = grant_stats['2016']['grant_count']

        new_word.grant_total_cost_16 = round(grant_stats['2016']['grant_total_cost'],-3)/1000

        new_word.grant_direct_cost_16 = round(grant_stats['2016']['grant_direct_cost'],-3)/1000

        new_word.grant_indirect_cost_16 = round(grant_stats['2016']['grant_indirect_cost'],-3)/1000

        new_word.grant_count_15 = grant_stats['2015']['grant_count']

        new_word.grant_total_cost_15 = round(grant_stats['2015']['grant_total_cost'],-3)/1000

        new_word.grant_direct_cost_15 = round(grant_stats['2015']['grant_direct_cost'],-3)/1000

        new_word.grant_indirect_cost_15 = round(grant_stats['2015']['grant_indirect_cost'],-3)/1000

        new_word.grant_count_14 = grant_stats['2014']['grant_count']

        new_word.grant_total_cost_14 = round(grant_stats['2014']['grant_total_cost'],-3)/1000

        new_word.grant_direct_cost_14 = round(grant_stats['2014']['grant_direct_cost'],-3)/1000

        new_word.grant_indirect_cost_14 = round(grant_stats['2014']['grant_indirect_cost'],-3)/1000

        new_word.f31_count= grant_stats['totals']['f31_count']
        print(f'this is the f31 count {new_word.f31_count}')

        new_word.f31_total_cost= round(grant_stats['totals']['f31_total_cost'],-3)/1000

        new_word.f32_count= grant_stats['totals']['f32_count']

        new_word.f32_total_cost= round(grant_stats['totals']['f32_total_cost'],-3)/1000

        new_word.k99_count= grant_stats['totals']['k99_count']

        new_word.k99_total_cost= round(grant_stats['totals']['k99_total_cost'],-3)/1000

        new_word.r00_count= grant_stats['totals']['r00_count']

        new_word.r00_total_cost= round(grant_stats['totals']['r00_total_cost'],-3)/1000

        new_word.r01_count= grant_stats['totals']['r01_count']

        new_word.r01_total_cost= round(grant_stats['totals']['r01_total_cost'],-3)/1000

        new_word.r35_count= grant_stats['totals']['r35_count']

        new_word.r35_total_cost= round(grant_stats['totals']['r35_total_cost'],-3)/1000

        new_word.dp1_count= grant_stats['totals']['dp1_count']

        new_word.dp1_total_cost= round(grant_stats['totals']['dp1_total_cost'],-3)/1000

        new_word.dp2_count= grant_stats['totals']['dp2_count']

        new_word.dp2_total_cost= round(grant_stats['totals']['dp2_total_cost'],-3)/1000

        try:
            Keyword.full_clean(new_word)
        except ValidationError as e:
            print(e)

        try:
            new_word.save()
        except:
            print(f"there was a problem saving the stats associated with Keyword {new_word}")
        return new_word

    def no_repeats(grant_list):
        # index = 0
        core_project_nums = {}
        grant_list_no_repeats =[]
        for grant in grant_list:
            # print(f'index: {index}')
            # print(f'index: {length}')
            # print(f'success: {success}')
            core_id = grant.core_project_num
            if core_id in core_project_nums:
                pass
            else:
                grant_list_no_repeats.append(grant)
                core_project_nums[core_id] = 1
                # print("a core project number")
                # print(grant.core_project_num)
            # index += 1
        print('no repeats')
        return grant_list_no_repeats

    # def make_short_list(grant_list_long):
    #     length = len(grant_list_long)
    #     print (f'this is the length: {length}')
    #     index = 0
    #     success = 0
    #     core_project_nums =[]
    #     grant_list_short =[]
    #
    #     while success < 100 or index > length:
    #         print(f'index: {index}')
    #         print(f'index: {length}')
    #         print(f'success: {success}')
    #         core_id = grant_list_long[index].core_project_num
    #         if core_id in core_project_nums:
    #             pass
    #         else:
    #             grant_list_short.append(grant_list_long[index])
    #             core_project_nums.append(core_id)
    #             success += 1
    #             print("a core project number")
    #             print(grant_list_long[index].core_project_num)
    #         index += 1
    #     return grant_list_short


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

    def find_cost(list):
        total_cost = 0
        direct_cost = 0
        indirect_cost = 0
        number = 0
        # if list.count() > 0:
        for item in list:
            number += 1
            if item.total_cost:
                if item.total_cost:
                     total_cost += item.total_cost
                if item.direct_cost_amt:
                    direct_cost += item.direct_cost_amt
                if item.indirect_cost_amt:
                    indirect_cost += item.indirect_cost_amt
        return {'total_cost':total_cost, 'direct_cost':direct_cost, 'indirect_cost':indirect_cost,
        'number': number}

    def divide_by_FY(grant_list):
        # years = range(1985,2018,1)
        years = range(2014, 2019, 1)
        grants_by_year={}
        for year in years:
            year_str = str(year)
            grants_by_year[year_str] = grant_list.filter(FY=year)
        return grants_by_year

    def number_of_papers(list):
        total = 0
        for grant in list:
            total += grant.number_of_papers()
        return total

    def return_stats_by_year(grant_list, query):
        #make a dict of all the stats divided by FY
        #{totals: {grant_total_cost: xx, grant_indirect_cost:xx...}, 1985: {grant_total_cost = xx,...}}
        grant_dict = Stats.divide_by_FY(grant_list)
        stats_dict = {}
        stats_dict['totals'] = Stats.return_stats_dict(grant_list, query)
        years = range(2014, 2019, 1)
        for year in years:
            year_str = str(year)
            stats_dict[year_str] = Stats.return_stats_dict(grant_dict[year_str], query)
        return stats_dict

    def states(grant_list):
        a = datetime.datetime.now()
        STATES = ["HI", "AK", "FL", "SC", "GA", "AL", "NC", "TN", "RI", "CT", "MA", "ME", "NH", "VT", "NY", "NJ", "PA", "DE", "MD", "WV", "KY", "OH", "MI", "WY", "MT", "ID", "WA", "DC", "TX", "CA", "AZ", "NV", "UT", "CO", "NM", "OR", "ND", "SD", "NE", "IA", "MS", "IN", "IL", "MN", "WI", "MO", "AR", "OK", "KS", "LA", "VA"]

        states_dict = {
        "HI": 0,  "AK": 0, "FL": 0, "SC": 0, "GA": 0, "AL": 0, "NC": 0, "TN": 0, "RI": 0, "CT": 0, "MA": 0, "ME": 0, "NH": 0, "VT": 0, "NY": 0, "NJ": 0, "PA": 0, "DE": 0, "MD": 0, "WV": 0, "KY": 0, "OH": 0, "MI": 0, "WY": 0, "MT": 0, "ID": 0, "WA": 0, "DC": 0, "TX": 0, "CA": 0, "AZ": 0, "NV": 0, "UT": 0, "CO": 0, "NM": 0, "OR": 0, "ND": 0, "SD": 0, "NE": 0, "IA": 0, "MS": 0, "IN": 0, "IL": 0, "MN": 0, "WI": 0, "MO": 0, "AR": 0, "OK": 0, "KS": 0, "LA": 0, "VA": 0
        }
        for grant in grant_list:
            if grant.org_state in STATES:
                states_dict[grant.org_state] += 1
            else:
                pass
        b = datetime.datetime.now()
        print(f'time calculating states_dict: {b-a}')
        return json.dumps(states_dict)

    def return_max(dictionary):
        #make this return top three
        top_three = []
        if dictionary != {}:
            first =[]
            focal = max(dictionary, key=dictionary.get)
            first = [focal.title(), dictionary[focal]]
            top_three.append(first)
            del dictionary[focal]
        else:
            top_three.append([None, 0])

        if dictionary != {}:
            second = []
            focal = max(dictionary, key=dictionary.get)
            # focal = focal.title()
            second = [focal.title(), dictionary[focal]]
            top_three.append(second)
            del dictionary[focal]
        else:
            top_three.append([None, 0])

        if dictionary != {}:
            third = []
            focal = max(dictionary, key=dictionary.get)
            third = [focal.title(),dictionary[focal]]
            top_three.append(third)
        else:
            top_three.append([None, 0])
        return top_three


    def top_institutions(grant_list):
        a = datetime.datetime.now()
        STATES = ["HI", "AK", "FL", "SC", "GA", "AL", "NC", "TN", "RI", "CT", "MA", "ME", "NH", "VT", "NY", "NJ", "PA", "DE", "MD", "WV", "KY", "OH", "MI", "WY", "MT", "ID", "WA", "DC", "TX", "CA", "AZ", "NV", "UT", "CO", "NM", "OR", "ND", "SD", "NE", "IA", "MS", "IN", "IL", "MN", "WI", "MO", "AR", "OK", "KS", "LA", "VA"]

        institution_hash ={
        "HI": {},  "AK": {}, "FL": {}, "SC": {}, "GA": {}, "AL": {}, "NC": {}, "TN": {}, "RI": {}, "CT": {}, "MA": {}, "ME": {}, "NH": {}, "VT": {}, "NY": {}, "NJ": {}, "PA": {}, "DE": {}, "MD": {}, "WV": {}, "KY": {}, "OH": {}, "MI": {}, "WY": {}, "MT": {}, "ID": {}, "WA": {}, "DC": {}, "TX": {}, "CA": {}, "AZ": {}, "NV": {}, "UT": {}, "CO": {}, "NM": {}, "OR": {}, "ND": {}, "SD": {}, "NE": {}, "IA": {}, "MS": {}, "IN": {}, "IL": {}, "MN": {}, "WI": {}, "MO": {}, "AR": {}, "OK": {}, "KS": {}, "LA": {}, "VA": {}
        }

        for grant in grant_list:
            if grant.org_state in STATES:
                try:
                    institution_hash[grant.org_state][grant.org_name] += 1
                except:
                    institution_hash[grant.org_state][grant.org_name] = 0
            else:
                pass

        new_hash = {}
        for state in STATES:
            new_hash[state] = Stats.return_max(institution_hash[state])

        b = datetime.datetime.now()
        print(f'time calculating top_institutions: {b-a}')
        print(new_hash)
        return json.dumps(new_hash)



        # for state in STATES:
        #     state_grant_list = grant_list.filter(org_state=state)
        #     state_hash = {}
        #     for grant in state_grant_list:
        #         if grant.org_name in state_hash:
        #             state_hash[grant.org_name] += 1
        #         else:
        #             state_hash[grant.org_name] = 1
        #
        #     top_three = Stats.return_max(state_hash)
        #
        #     institution_hash[state] = top_three
        # b = datetime.datetime.now()
        # print(f'time calculating top_institutions: {b-a}')
        # return json.dumps(institution_hash)

    def return_stats_dict(grant_list, query):
        grant1 = grant_list
        a = datetime.datetime.now()
        grant_count = grant_list.count()
        costs = Stats.find_cost(grant_list)
        grant_total_cost = costs['total_cost']
        grant_indirect_cost = costs['indirect_cost']
        grant_direct_cost = costs['direct_cost']
        grant_num_papers = Stats.number_of_papers(grant_list)

        # #make dict where grants are divided by FY
        # #ex. {'2015': <QuerySet []>, '2016': <QuerySet [<Grant: 9082664>, <Grant: 9114892>]}
        # grant_list = Stats.divide_by_FY(grant_list)
        # print(grant_list)

        # Individual Predoctoral NRSA for M.D./Ph.D. Fellowships
        grant_f30 = grant_list.filter(activity="F30")
        costs = Stats.find_cost(grant_f30)
        f30_total_cost = costs['total_cost']
        f30_count = len(Add_Keyword.no_repeats(grant_f30))
        # f30_count = costs['number']

        # Predoctoral Individual National Research Service Award
        grant_f31 = grant_list.filter(activity="F31")
        f31_total_cost = Stats.find_cost(grant_f31)
        costs = Stats.find_cost(grant_f31)
        f31_total_cost = costs['total_cost']
        f31_count = len(Add_Keyword.no_repeats(grant_f31))
        # f31_count = costs['number']

        # Postdoctoral Individual National Research Service Award
        grant_f32 = grant_list.filter(activity="F32")
        f32_total_cost = Stats.find_cost(grant_f32)
        costs = Stats.find_cost(grant_f32)
        f32_total_cost = costs['total_cost']
        f32_count = len(Add_Keyword.no_repeats(grant_f32))
        # f32_count = costs['number']

        #Career Transition Award
        grant_k99 = grant_list.filter(activity="K99")
        k99_total_cost = Stats.find_cost(grant_k99)
        costs = Stats.find_cost(grant_k99)
        k99_total_cost = costs['total_cost']
        k99_count = len(Add_Keyword.no_repeats(grant_k99))
        # k99_count = costs['number']

        #Research Transition Award
        grant_r00 = grant_list.filter(activity="R00")
        r00_total_cost = Stats.find_cost(grant_r00)
        costs = Stats.find_cost(grant_r00)
        r00_total_cost = costs['total_cost']
        r00_count = len(Add_Keyword.no_repeats(grant_r00))
        # r00_count = costs['number']

        #Research Project
        grant_r01 = grant_list.filter(activity="R01")
        r01_total_cost = Stats.find_cost(grant_r01)
        costs = Stats.find_cost(grant_r01)
        r01_total_cost = costs['total_cost']
        r01_count = len(Add_Keyword.no_repeats(grant_r01))
        # r01_count = costs['number']

        #Outstanding Investigator Award
        grant_r35 = grant_list.filter(activity="R35")
        r35_total_cost = Stats.find_cost(grant_r35)
        costs = Stats.find_cost(grant_r35)
        r35_total_cost = costs['total_cost']
        r35_count = len(Add_Keyword.no_repeats(grant_r35))
        # r35_count = costs['number']

        #NIH Director’s Pioneer Award (NDPA)
        grant_dp1 = grant_list.filter(activity="DP1")
        dp1_total_cost = Stats.find_cost(grant_dp1)
        costs = Stats.find_cost(grant_dp1)
        dp1_total_cost = costs['total_cost']
        dp1_count = len(Add_Keyword.no_repeats(grant_dp1))
        # dp1_count = costs['number']

        #NIH Director’s New Innovator Award
        grant_dp2 =grant_list.filter(activity="DP2")
        dp2_total_cost = Stats.find_cost(grant_dp2)
        costs = Stats.find_cost(grant_dp2)
        dp2_total_cost = costs['total_cost']
        dp2_count = len(Add_Keyword.no_repeats(grant_dp2))
        # dp2_count = costs['number']

        b = datetime.datetime.now()
        print(f'time elapsed in stats: {b-a}')
        grant_stats_dict={'query': query,'grant_count': grant_count,'grant_total_cost':grant_total_cost,'grant_direct_cost':grant_direct_cost,'grant_indirect_cost':grant_indirect_cost,'grant_num_papers':grant_num_papers,'f30_count':f30_count,'f30_total_cost':f30_total_cost,'f31_count':f31_count,'f31_total_cost':f31_total_cost,'f32_count':f32_count,'f32_total_cost':f32_total_cost,'k99_count':k99_count,'k99_total_cost':k99_total_cost,'r00_count':r00_count,'r00_total_cost':r00_total_cost,'r01_count':r01_count,'r01_total_cost':r01_total_cost,'r35_count':r35_count,'r35_total_cost':r35_total_cost,'dp1_count':dp1_count,'dp1_total_cost':dp1_total_cost,'dp2_count':dp2_count,'dp2_total_cost':dp2_total_cost}

        return grant_stats_dict

    def remove_common_words(abstract):
        COMMON_WORDS_SET = set(['', 'A', 'What', 'Had', 'Has', 'Be', 'We', 'His', 'Her', 'Not', 'Now', 'By', 'On', 'Did', 'Of', 'She', 'Can', 'Or', 'Day', 'Are', 'Go', 'Find', 'From', 'For', 'Long', 'Which', 'More', 'That', 'Water', 'Part', 'Than', 'He', 'Made', 'Word', 'Look', 'This', 'Could', 'Up', 'Were', 'My', 'First', 'People', 'Use', 'Said', 'Would', 'No', 'Make', 'There', 'When', 'Two', 'Their', 'Way', 'Was', 'Get', 'But', 'Come', 'These', 'So', 'Been', 'Time', 'And', 'How', 'Into', 'Number', 'Him', 'Down', 'See', 'Your', 'Out', 'Write', 'To', 'Other', 'Call', 'You', 'An', 'Each', 'Do', 'Them', 'Oil', 'May', 'Who', 'They', 'Many', 'With', 'A', 'About', 'Like', 'Then', 'I', 'Will', 'The', 'All', 'Is', 'Some', 'It', 'One', 'As', 'At', 'Have', 'In', 'Its', 'If', 'Dr', 'And/or', 'May','To','Project', 'From','On', 'Our', 'Such', 'Description', '(provided', 'Applicant:', 'Where', 'Mostly', 'Here', 'Propose', 'Hypothesis', 'Address', 'Also', 'Already', 'Every', 'Aim', 'Finally', 'Although', 'Over', 'While', 'Study', 'Very', 'Well', 'Also', 'Of', 'Why'])

        COMMON_PUNTUATION =set(['.','?',',', ';', ':' '1)','2)','3)','4)', ')', ')', '#1', ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ', ' = ', '1:', '2:', '3:', '4:', ' - '])


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

        return ' '.join(abstract_list)

    def euclidian(grant_ab, paper_ab):

        corpus = [grant_ab, paper_ab]

        vectorizer = CountVectorizer()
        features = vectorizer.fit_transform(corpus).todense()
        #print( vectorizer.vocabulary_ )

        for f in features:
            d = euclidean_distances(features[0], f)
            e = d.shape
            # print(euclidean_distances(features[0], f))[0]
            # print(euclidean_distances(features[0], f))[1]
            # print(euclidean_distances(features[0], f))[2]

        return(euclidean_distances(features[0], f)[0][0])


class Relate_grants:
    def set_related_grant_stats(grant_list):
        print('related_grants has been called')
        print(grant_list)
        for grant in grant_list:
            #get the related_grants object
            rgo= None
            try:
                rgo = grant.related_grant_set.get()
                print(f'I found this related_grant_set: {related_grant_object}' )
            except:
                pass
            print(rgo)
        #if there is no related_grant_object, make one.
            if rgo == None:
                print('saving new related_grant_object')
                assoc_grants = Grant.objects.filter(core_project_num = grant.core_project_num)
                total_cost = 0
                indirect = 0
                direct = 0
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
            #set grant attributes based on rgo
            grant.total_funding_of_core_numb = rgo.total_funding_of_core_numb
            grant.total_indirect_of_core_numb = rgo.total_indirect_of_core_numb
            grant.total_direct_of_core_numb = rgo.total_direct_of_core_numb

            try:
                grant.save()
                print ('saved total_funding_of_core_numb')

            except ValidationError as e:
                print(e)

        return(grant_list)
        #make hash of grant_ab
        #{word: 2}
