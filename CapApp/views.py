from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# import pubmed_parser as pp
import requests
import datetime
import time
import json
from django.core.exceptions import ValidationError

# from django.core.urlresolvers import reverse
# from CapApp.pubmed import Pubmed
from CapApp.models import Grant, Keyword, Publication, Related_grant
from CapApp.custom_classes import Stats, Add_Keyword, Score, Publication_methods, Relate_grants

# Create your views here.

def about(request):
    return render(request, 'CapApp/about.html')

def index(request):
    # request.session['query'] = None
    request.session['query'] = None
    print('this is the session info')
    print({request.session['query']})
    top_twenty_searches = Keyword.objects.all()
    if top_twenty_searches.count() > 20:
        top_twenty_searches = top_twenty_searches[0:19]

    #none of this is working b/c the search form submits to grants b/c the urls are messed up
    errors = []
    if request.method == 'GET':
        q = request.GET.get('q', '')
        q = q.capitalize()
        print(f'query at the start of index GET: {q}')
        if q !="":
            request.session['query'] = q.rstrip()
            return HttpResponseRedirect('grants/?q='+q)

    #return a hash for the d3 scatterplot
    scatter_dict =[]
    for keyword in top_twenty_searches:
        keyword_2018 = {}
        keyword_2017 = {}
        keyword_2016 = {}
        keyword_2015 = {}
        keyword_2014 = {}

        keyword_2018['Year'] = 2018
        keyword_2018['keyword'] = keyword.keyword
        if keyword.grant_total_cost_18:
            keyword_2018['total_cost'] =round((keyword.grant_total_cost_18/1000), 1)
        else:
            keyword_2018['total_cost'] = 0


        keyword_2017['Year'] = 2017
        keyword_2017['keyword'] =keyword.keyword
        if keyword.grant_total_cost_17:
            keyword_2017['total_cost'] =round((keyword.grant_total_cost_17/1000), 1)
        else:
            keyword_2017['total_cost'] = 0

        keyword_2016['Year'] = 2016
        keyword_2016['keyword'] =keyword.keyword
        if keyword.grant_total_cost_16:
            keyword_2016['total_cost'] =round((keyword.grant_total_cost_16/1000), 1)
        else:
            keyword_2016['total_cost'] = 0

        keyword_2015['Year'] = 2015
        keyword_2015['keyword'] =keyword.keyword
        if keyword.grant_total_cost_15:
            keyword_2015['total_cost'] =round((keyword.grant_total_cost_15/1000), 1)
        else:
            keyword_2015['total_cost'] = 0

        keyword_2014['Year'] = 2014
        keyword_2014['keyword'] = keyword.keyword
        if keyword.grant_total_cost_14:
            keyword_2014['total_cost'] =round((keyword.grant_total_cost_14/1000), 1)
        else:
            keyword_2014['total_cost'] = 0

        scatter_dict.append(keyword_2018)
        scatter_dict.append(keyword_2017)
        scatter_dict.append(keyword_2016)
        scatter_dict.append(keyword_2015)
        scatter_dict.append(keyword_2014)

    scatter_dict = json.dumps(scatter_dict)

    return render(request, 'CapApp/index.html', {'top_twenty_searches': top_twenty_searches, 'errors': errors, 'scatter_dict': scatter_dict})



def grants(request):
    query = request.GET.get('q', '')
    # query = request.session['query']

    #1)See if there is a keyword_object for that keyword
    print(f'this is the query {query}')
    try:
        keyword_object = Keyword.objects.get(keyword__iexact=query)
        print(f'I found a Keyword!')
    except:
        keyword_object = None
    print(f'this is the keyword_object: {keyword_object}')

    #2) If there is a keyword_object, incriment the search feild
    if keyword_object:
        Add_Keyword.incriment_keyword_searches(keyword_object)

        grant_list_short = keyword_object.grants.all()[:100]
        print(f'a keyword exists and this is my grant list {grant_list_short}')
        # grant_list_short = grant_list_long[:100]
        # grant_list_short = Add_Keyword.make_short_list(grant_list_long)

    #3) if there is not, do a database search and create a keyword
    else:
        grant_list_long = Grant.objects.filter(project_terms__search=query)
        print(f'a keyword did not exist and this is my grant list {grant_list_long}')
        keyword_object = Add_Keyword.create_keyword(query, grant_list_long, searches=1)
        grant_list_short = new_word.grant_list[:100]

        # grant_list_short = Add_Keyword.make_short_list(grant_list_long)

        # state_dict = Stats.states(grant_list)
        # new_word.states_dict = state_dict
        #
        # states_top_inst = Stats.top_institutions(grant_list_long)
        #
        # new_word.states_top_inst = states_top_inst
        # try:
        #     new_word.save()
        #     print('I saved the states_dict')
        # except:
        #     print(f"there was a problem saving with state_dict")
    #4) find total cost associated with grant

    #5)Paginate the first 100 results
    # c = datetime.datetime.now()
    # paginator = Paginator(grant_list_short, 10)
    # # Show 10 contacts per page
    # page_number = request.GET.get('page')
    # try:
    #     grants = paginator.page(page_number)
    # except PageNotAnInteger:
    #     grants = paginator.page(1)
    # except EmptyPage:
    #     grants = paginator.page(paginator.num_pages)
    #
    # d = datetime.datetime.now()
    # print(f'time in pagination = {d-c}')

    #6)Calculate the stats for all the results
    # grant_stats = Stats.return_stats_by_year(grant_list_long, query)

    #Make scatter plot array for papers vs. funding
    # scatterplot_array =[]
    # for grant in grant_list_short:
    #     if grant.FY == 2018 and grant.support_year < 5:
    #         all_years = True
    #     elif grant.FY == 2017 and grant.support_year < 4:
    #         all_years = True
    #     elif grant.FY == 2016 and grant.support_year < 3:
    #         all_years = True
    #     elif grant.FY == 2015 and grant.support_year < 2:
    #         all_years = True
    #     elif grant.FY == 2014 and grant.support_year < 1:
    #         all_years = True
    #     else:
    #         all_years = None
    #
    #     if all_years:
    #         temp ={}
    #         temp['number'] = grant.number_of_papers()
    #         temp['total_cost'] = grant.total_funding_of_core_numb
    #         temp['core_project_num'] =grant.core_project_num
    #         scatterplot_array.append(temp)
    #     else:
    #         pass
    # scatterplot_array = json.dumps(scatterplot_array)
    # print(scatterplot_array)


    #     temp = {}
    #     temp['Cost'] = grant.total_cost
    #     temp['num_papers'] = grant.number_of_papers
    #     temp['Journal'] =


    # states_dict = Stats.states(grant_list_long)

    # states_top_inst = Stats.top_institutions(grant_list_long)

    # keyword_object = Keyword.objects.get(keyword__iexact=query)
    return render(request, 'CapApp/grants.html',{'grants':grant_list_short, 'keyword':keyword_object})
    # return render(request, 'CapApp/grants.html',{'grants':grant_list_short, 'keyword':keyword_object, 'states_dict': states_dict, 'states_top_inst': states_top_inst, 'scatterplot_array': scatterplot_array})

#https://github.com/titipata/pubmed_parser
#if you use this package please cite: Titipat Achakulvisut, Daniel E. Acuna (2015) "Pubmed Parser" http://github.com/titipata/pubmed_parser. http://doi.org/10.5281/zenodo.159504
def publications(request):
    app_id = request.GET.get('app_id', '')
    #why do I sometimes get many more than one result for the same core project number when I only have 2018 loaded? this is happening for P60AA009803, P01HL018646, but not RO1s?  Switched to app_id to avoid problem.
    focal = Grant.objects.get(application_id = app_id)
    #list_of_papers returns a list of all Grant_Publication.objects with that project number
    list_papers = focal.list_of_papers()
    pubs = Publication_methods.return_list_of_publications(list_papers)

    # cleaned_grantab_text =
    # cleaned_paperab_text =
    for pub in pubs:
        if pub.abstract == "":
            pass
        elif focal.abstract_text == "":
            pass
        else:
            cleaned_grantab = Stats.remove_common_words(focal.abstract_text)
            cleaned_pubab = Stats.remove_common_words(pub.abstract)
            score = Stats.euclidian(cleaned_grantab, cleaned_pubab)
            print(f'this is the eculdian score: {score}')
            pub.score = round(score, 3)
            pub.save()

    all_papers_score = Score.return_all_scores
    n = Score.return_n
    focal_papers_score = Score.return_focal_scores(pubs)
    box_plot_data ={"n": n, "all_papers_score": all_papers_score, "focal_papers_score": focal_papers_score}

    related_grant_object = None
    try:
        related_grant_object = Related_grant.objects.get(core_project_num = focal.core_project_num)
        print('I found a related_grant_object')
    except ValidationError:
        print('I can not find a related_grant_object')
        Relate_grants.set_related_grant_stats([focal])

    print(f'core_project_num: {focal.core_project_num}')
    related_grant_object = Related_grant.objects.get(core_project_num = focal.core_project_num)

    related = related_grant_object.grants.all()
    same_grant_dif_year = related.filter(project_title = focal.project_title)
    same_grant_dif_year = same_grant_dif_year.exclude(FY=focal.FY)
    dif_grant = related.exclude(project_title = focal.project_title)
    print(f'same grant dif year: {same_grant_dif_year}')
    print(f'dif grant: {dif_grant}')

    return render(request, 'CapApp/publications.html', {'pubs':pubs, 'focal': focal, 'same_grant_dif_year': same_grant_dif_year, 'all_papers_score':all_papers_score, 'focal_papers_score':focal_papers_score, 'n':n })
