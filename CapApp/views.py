from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# import pubmed_parser as pp
import requests
import datetime
import time
from django.core.exceptions import ValidationError

# from django.core.urlresolvers import reverse
from CapApp.pubmed import Pubmed
from CapApp.models import Grant, Keyword, Publication, Related_grant
from CapApp.custom_classes import Stats, Add_Keyword

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
        # if not q:
        #     print('if not q')
        #     errors.append('Enter a search term.')
            # if len(q) > 30:
            #     errors.append('Please enter at most 30 characters.')
            # else:
            request.session['query'] = q.rstrip()
            return HttpResponseRedirect('grants')

    return render(request, 'CapApp/index.html', {'top_twenty_searches': top_twenty_searches, 'errors': errors})



def grants(request):
    query = request.session['query']

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

        grant_list_long = keyword_object.grants.all()
        print(f'a keyword exists and this is my grant list {grant_list_long}')
        grant_list_short = Add_Keyword.make_short_list(grant_list_long)

    #3) if there is not, do a database search and create a keyword
    else:
        grant_list_long = Grant.objects.filter(project_terms__search=query)
        print(f'a keyword did not exist and this is my grant list {grant_list_long}')
        Add_Keyword.create_keyword(query, grant_list_long, searches=1)

        grant_list_short = Add_Keyword.make_short_list(grant_list_long)

    #4) find total cost associated with grant
    #if this works consider moving it to a script on
    #data base launch
    #TODO: Revisit this when you are reloading the database. Should be able to delete all of this.
    for grant in grant_list_short:
        #get the related_grants object
        related_grant_object = grant.related_grant_set.get()

        #if the grant_object already has the total costs stored, use that.
        if related_grant_object.total_funding_of_core_numb:
            grant.total_funding_of_core_numb = related_grant_object.total_funding_of_core_numb

        if related_grant_object.total_direct_of_core_numb:
            grant.total_direct_of_core_numb = related_grant_object.total_direct_of_core_numb

        if related_grant_object.total_indirect_of_core_numb:
            grant.total_indirect_of_core_numb = related_grant_object.total_indirect_of_core_numb

        #if it doesn't have the total cost scored, calculate it
        if grant.total_funding_of_core_numb and grant.total_direct_of_core_numb and grant.total_indirect_of_core_numb:
            pass
        else:
            #find all the grants associated with that object
            assoc_grants = related_grant_object.grants.all()
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

            related_grant_object.total_funding_of_core_numb = total_cost
            grant.total_funding_of_core_numb = total_cost

            related_grant_object.total_indirect_of_core_numb = indirect
            grant.total_indirect_of_core_numb = indirect

            related_grant_object.total_direct_of_core_numb = direct
            grant.total_direct_of_core_numb = direct

            related_grant_object.save()
            grant.save()

        # print (f'total funding of grant number {grant.core_project_num} is:  {grant.total_funding_of_core_numb}')


    #5)Paginate the first 100 results
    c = datetime.datetime.now()
    paginator = Paginator(grant_list_short, 10)
    # Show 10 contacts per page
    page_number = request.GET.get('page')
    try:
        grants = paginator.page(page_number)
    except PageNotAnInteger:
        grants = paginator.page(1)
    except EmptyPage:
        grants = paginator.page(paginator.num_pages)

    d = datetime.datetime.now()
    print(f'time in pagination = {d-c}')

    #6)Calculate the stats for all the results
    # grant_stats = Stats.return_stats_by_year(grant_list_long, query)

    states_dict = Stats.states(grant_list_long)

    states_top_inst = Stats.top_institutions(grant_list_long)

    #7)save stats in keyword
    #TODO: put this in database set up.
    keyword_object = Keyword.objects.get(keyword__iexact=query)
    # print(f'I am saving the stats in the keyword object {keyword_object}')
    # keyword_object.grant_count = grant_stats['totals']['grant_count']
    # keyword_object.grant_total_cost = grant_stats['totals']['grant_total_cost']
    # print(f' this is the total cost before save: {keyword_object.grant_total_cost}')
    # keyword_object.grant_direct_cost = grant_stats['totals']['grant_direct_cost']
    # keyword_object.grant_indirect_cost = grant_stats['totals']['grant_indirect_cost']
    # try:
    #     Keyword.full_clean(keyword_object)
    # except ValidationError as e:
    #     print(e)
    # try:
    #     keyword_object.save()
    # except:
    #     print(f"there was a problem with saving Keyword {keyword_object}")
    # print(f' this is the total cost after save: {keyword_object.grant_total_cost}')



    return render(request, 'CapApp/grants.html',{'grants':grants, 'keyword':keyword_object, 'states_dict': states_dict, 'states_top_inst': states_top_inst})

#https://github.com/titipata/pubmed_parser
#if you use this package please cite: Titipat Achakulvisut, Daniel E. Acuna (2015) "Pubmed Parser" http://github.com/titipata/pubmed_parser. http://doi.org/10.5281/zenodo.159504
def publications(request):
    app_id = request.GET.get('app_id', '')
    #why do I sometimes get many more than one result for the same core project number when I only have 2018 loaded? this is happening for P60AA009803, P01HL018646, but not RO1s?  Switched to app_id to avoid problem.
    focal = Grant.objects.get(application_id = app_id)
    #list_of_papers returns a list of all Grant_Publication.objects with that project number
    list_papers = focal.list_of_papers()

    all_papers = []
    index = 1
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
                # if "(contact)" in item:
                #     item.replace("(contact)","*")


            pub.authors = list
            pub.year = temp['year']
            try:
                Publication.full_clean(pub)
            except ValidationError as e:
                print(e)

            try:
                pub.save()
                success +=1
            except:
                print(f"there was a problem saving publication {paper.pmid}")


        all_papers.append(pub)
        print('I am going to calculate the score')





        score = Stats.make_similarity_dict(focal.abstract_text, pub.abstract)
        pub.score = score
        pub.save()
        # all_papers.append(Pubmed.parse_xml_web(paper.pmid, sleep=2, save_xml=False))
        index += 1
        # try Related_grant.objects.get(core_project_num = focal.core_project_num):

    related_grant_object = Related_grant.objects.get(core_project_num = focal.core_project_num)
    related = related_grant_object.grants.all()
    same_grant_dif_year = related.filter(project_title = focal.project_title)
    same_grant_dif_year = same_grant_dif_year.exclude(FY=focal.FY)
    dif_grant = related.exclude(project_title = focal.project_title)
    print(f'same grant dif year: {same_grant_dif_year}')
    print(f'dif grant: {dif_grant}')
        # except:
            # related_grants = None


        # time.sleep(0.5)
    return render(request, 'CapApp/publications.html', {'all_papers':all_papers, 'focal': focal, 'same_grant_dif_year': same_grant_dif_year})


# def your_view(request):
#     ''' This could be your actual view or a new one '''
#     # Your code
#     if request.method == 'GET': # If the form is submitted
#
#         search_query = request.GET.get('search_box', None)

# def help(request):
#     helpdict = {'help_insert': 'HELP PAGE'}
#     return render(request, 'CapApp/help.html',context=helpdict)
