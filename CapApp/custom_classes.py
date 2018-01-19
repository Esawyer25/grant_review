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
        for paper in list_papers:
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
            pubs.append(pub)

        return (pubs)


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
        for grant in grant_list:
            new_word.grants.add(grant)

        Add_Keyword.set_keyword_stats(new_word, grant_list)

        b = datetime.datetime.now()
        print(f'time in to create new keyword = {b-a}')

    def set_keyword_stats(new_word, grant_list):
        #grant_list = new_word.grants.all()
        print(f'this is my grant_list {grant_list}')
        print(f'in set keyword stats, this is my word {new_word.keyword}')
        grant_stats = Stats.return_stats_by_year(grant_list, new_word.keyword)
        print(f'these are the grant stats{grant_stats}')

        #see if counting in thousands makes the numbers small enough

        new_word.grant_count = grant_stats['totals']['grant_count']

        new_word.grant_total_cost = round(grant_stats['totals']['grant_total_cost'],-3)/1000
        print( f'this is the total cost {new_word.grant_total_cost}')

        new_word.grant_direct_cost = round(grant_stats['totals']['grant_direct_cost'],-3)/1000
        print( f'this is the direct cost {new_word.grant_direct_cost}')

        new_word.grant_indirect_cost = round(grant_stats['totals']['grant_indirect_cost'],-3)/1000
        print( f'this is the indirect cost {new_word.grant_indirect_cost}')

        # new_word.grant_count_18 = grant_stats['2018']['grant_count']
        #
        # new_word.grant_total_cost_18 = grant_stats['2018']['grant_total_cost']
        #
        # new_word.grant_direct_cost_18 = grant_stats['2018']['grant_direct_cost']
        #
        # new_word.grant_indirect_cost_18 = grant_stats['2018']['grant_indirect_cost']

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
        years = range(2015, 2018, 1)
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
        years = range(2015, 2018, 1)
        for year in years:
            year_str = str(year)
            stats_dict[year_str] = Stats.return_stats_dict(grant_dict[year_str], query)
        return stats_dict

    def states(grant_list):
        a = datetime.datetime.now()
        STATES = ["HI", "AK", "FL", "SC", "GA", "AL", "NC", "TN", "RI", "CT", "MA","ME", "NH", "VT", "NY", "NJ", "PA", "DE", "MD", "WV", "KY", "OH", "MI", "WY", "MT", "ID", "WA", "DC", "TX", "CA", "AZ", "NV", "UT", "CO", "NM", "OR", "ND", "SD", "NE", "IA", "MS", "IN", "IL", "MN", "WI", "MO", "AR", "OK", "KS", "LS", "VA"]
        states_dict={}
        for state in STATES:
            results = grant_list.filter(org_state=state)
            length = len(results)
            states_dict[state] = length
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
        STATES = ["HI", "AK", "FL", "SC", "GA", "AL", "NC", "TN", "RI", "CT", "MA","ME", "NH", "VT", "NY", "NJ", "PA", "DE", "MD", "WV", "KY", "OH", "MI", "WY", "MT", "ID", "WA", "DC", "TX", "CA", "AZ", "NV", "UT", "CO", "NM", "OR", "ND", "SD", "NE", "IA", "MS", "IN", "IL", "MN", "WI", "MO", "AR", "OK", "KS", "LS", "VA"]
        institution_hash ={}
        for state in STATES:
            state_grant_list = grant_list.filter(org_state=state)
            state_hash = {}
            for grant in state_grant_list:
                if grant.org_name in state_hash:
                    state_hash[grant.org_name] += 1
                else:
                    state_hash[grant.org_name] = 1

            top_three = Stats.return_max(state_hash)

            institution_hash[state] = top_three
        b = datetime.datetime.now()
        print(f'time calculating top_institutions: {b-a}')
        return json.dumps(institution_hash)

    def return_stats_dict(grant_list, query):
        grant1= grant_list
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
        grant_f30 = grant_list.filter(activity="F30")
        costs = Stats.find_cost(grant_f30)
        f30_total_cost = costs['total_cost']
        f30_count = costs['number']

        # Predoctoral Individual National Research Service Award
        grant_f31 = grant_list.filter(activity="F31")
        f31_total_cost = Stats.find_cost(grant_f31)
        costs = Stats.find_cost(grant_f31)
        f31_total_cost = costs['total_cost']
        f31_count = costs['number']

        # Postdoctoral Individual National Research Service Award
        grant_f32 = grant_list.filter(activity="F32")
        f32_total_cost = Stats.find_cost(grant_f32)
        costs = Stats.find_cost(grant_f32)
        f32_total_cost = costs['total_cost']
        f32_count = costs['number']

        #Career Transition Award
        grant_k99 = grant_list.filter(activity="K99")
        k99_total_cost = Stats.find_cost(grant_k99)
        costs = Stats.find_cost(grant_k99)
        k99_total_cost = costs['total_cost']
        k99_count = costs['number']

        #Research Transition Award
        grant_r00 = grant_list.filter(activity="R00")
        r00_total_cost = Stats.find_cost(grant_r00)
        costs = Stats.find_cost(grant_r00)
        r00_total_cost = costs['total_cost']
        r00_count = costs['number']

        #Research Project
        grant_r01 = grant_list.filter(activity="R01")
        r01_total_cost = Stats.find_cost(grant_r01)
        costs = Stats.find_cost(grant_r01)
        r01_total_cost = costs['total_cost']
        r01_count = costs['number']

        #Outstanding Investigator Award
        grant_r35 = grant_list.filter(activity="R35")
        r35_total_cost = Stats.find_cost(grant_r35)
        costs = Stats.find_cost(grant_r35)
        r35_total_cost = costs['total_cost']
        r35_count = costs['number']

        #NIH Director’s Pioneer Award (NDPA)
        grant_dp1 = grant_list.filter(activity="DP1")
        dp1_total_cost = Stats.find_cost(grant_dp1)
        costs = Stats.find_cost(grant_dp1)
        dp1_total_cost = costs['total_cost']
        dp1_count = costs['number']

        #NIH Director’s New Innovator Award
        grant_dp2 =grant_list.filter(activity="DP2")
        dp2_total_cost = Stats.find_cost(grant_dp2)
        costs = Stats.find_cost(grant_dp2)
        dp2_total_cost = costs['total_cost']
        dp2_count = costs['number']

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
        for grant in grant_list:
            #get the related_grants object
            related_grant_object = None
            try:
                related_grant_object = grant.related_grant_set.get()
            except:
                pass

            #if the grant_object already has the total costs stored, use that.
            if related_grant_object:
                try:
                    grant.total_funding_of_core_numb = related_grant_object.total_funding_of_core_numb
                except:
                    pass

                try:
                    grant.total_direct_of_core_numb = related_grant_object.total_direct_of_core_numb
                except:
                    pass

                try:
                    grant.total_indirect_of_core_numb = related_grant_object.total_indirect_of_core_numb
                except:
                    pass
            #if it doesn't have the total cost scored, calculate it
            else:
                #find all the grants associated with that object
                print('saving new related_grant_object')
                assoc_grants = Grant.objects.filter(core_project_num = grant.core_project_num)
                total_cost = 0
                indirect = 0
                direct = 0
                for assoc_grant in assoc_grants:
                    if assoc_grant.total_cost:
                        total_cost += assoc_grant.total_cost

                    if assoc_grant.indirect_cost_amt:
                        indirect += assoc_grant.indirect_cost_amt

                    if assoc_grant.direct_cost_amt:
                        direct += assoc_grant.direct_cost_amt

                new_R_G_O= Related_grant()
                new_R_G_O.total_funding_of_core_numb = total_cost
                grant.total_funding_of_core_numb = total_cost

                new_R_G_O.total_indirect_of_core_numb = indirect
                grant.total_indirect_of_core_numb = indirect

                new_R_G_O.total_direct_of_core_numb = direct
                grant.total_direct_of_core_numb = direct

                new_R_G_O.save()
                grant.save()

                new_R_G_O.grants.set(assoc_grants)
        return(grant_list)
        #make hash of grant_ab
        #{word: 2}
