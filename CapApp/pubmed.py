# import sys
# import re
import time
import requests
from lxml import etree
from lxml import html
from unidecode import unidecode
from itertools import chain

import os
if 'API_KEY' in os.environ:
    pass
else:
    print('I got it from here')
    from CapProj.settings_secret import API_KEY

#What does this do?
# try:
#     from urllib.request import urlopen
# except ImportError:
#     from urllib2 import urlopen

"""
This coded was taken from
Titipata's pubmed_parser (https://github.com/titipata/pubmed_parser) and only slightly modified for my needs.
Titipat Achakulvisut, Daniel E. Acuna (2015) "Pubmed Parser" http://github.com/titipata/pubmed_parser. http://doi.org/10.5281/zenodo.159504
"""

class Pubmed:
    def stringify_children(node):
        """
        Filters and removes possible Nones in texts and tails
        ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
        """
        parts = ([node.text] +
                 list(chain(*([c.text, c.tail] for c in node.getchildren()))) +
                 [node.tail])
        return ''.join(filter(None, parts))

    def load_xml(pmid, sleep=None):
        """
        Load XML file from given pmid from eutils site
        return a dictionary for given pmid and xml string from the site
        sleep: how much time we want to wait until requesting new xml
        """
        link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=%s" % str(pmid) + "&api_key=" + API_KEY
        print(link)
        page = requests.get(link)
        tree = html.fromstring(page.content)
        if sleep is not None:
            time.sleep(sleep)
        return tree


    def parse_pubmed_web_tree(tree):
        """
        Giving tree, return simple parsed information from the tree
        """

        if tree.xpath('//articletitle') is not None:
            title = ' '.join([title.text for title in tree.xpath('//articletitle')])
        else:
            title = ''

        abstract_tree = tree.xpath('//abstract/abstracttext')
        abstract = ' '.join([Pubmed.stringify_children(a).strip() for a in abstract_tree])

        if tree.xpath('//article//title') is not None:
            journal = ';'.join([t.text.strip() for t in tree.xpath('//article//title')])
        else:
            journal = ''

        pubdate = tree.xpath('//pubmeddata//history//pubmedpubdate[@pubstatus="medline"]')
        if len(pubdate) >= 1 and pubdate[0].find('year') is not None:
            year = pubdate[0].find('year').text
        else:
            year = ''

        affiliations = list()
        if tree.xpath('//affiliationinfo/affiliation') is not None:
            for affil in tree.xpath('//affiliationinfo/affiliation'):
                affiliations.append(affil.text)
        affiliations_text = '; '.join(affiliations)

        authors_tree = tree.xpath('//authorlist/author')
        authors = list()
        if authors_tree is not None:
            for a in authors_tree:
                firstname = a.find('forename').text if a.find('forename') is not None else ''
                lastname = a.find('lastname').text if a.find('forename') is not None else ''
                fullname = (firstname + ' ' + lastname).strip()
                if fullname == '':
                    fullname = a.find('collectivename').text if a.find('collectivename') is not None else ''
                authors.append(fullname)
            authors_text = '; '.join(authors)
        else:
            authors_text = ''

        dict_out = {'title': title,
                    'journal': journal,
                    'affiliation': affiliations_text,
                    'authors': authors_text,
                    'year': year,
                    'abstract': abstract}
        return dict_out


    def parse_xml_web(pmid, sleep=None, save_xml=False):
        """
        Give pmid, load and parse xml from Pubmed eutils
        if save_xml is True, save xml output in dictionary
        """
        tree = Pubmed.load_xml(pmid, sleep=sleep)
        dict_out = Pubmed.parse_pubmed_web_tree(tree)
        dict_out['pmid'] = str(pmid)
        if save_xml:
            dict_out['xml'] = etree.tostring(tree)
        return dict_out
