"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import httpretty
import os
import json


SAMPLE_ARTHRITIS = r'''{"ListRecords":[{"total_hits":5015},{"record":{"header":{"header:content":{"core:repositoryIdentifier":"143","identifier":"669636"},"header:attr":{"xmlns:core":"http:\/\/core.kmi.open.ac.uk\/api\/doc"}},"metadata":{"oai_dc:dc":{"oai_dc:ns":[{"xmlns:oai_dc":"http:\/\/www.openarchives.org\/OAI\/2.0\/oai_dc\/","xmlns:dc":"http:\/\/purl.org\/dc\/elements\/1.1\/"}],"dc:creator":"R Kudyar","dc:format":"application\/pdf","dc:source":"http:\/\/www.jkscience.org\/archive\/111\/18-RL-JACORD%20ARTHRITIS.pdf","dc:date":"2009","dc:identifier":"http:\/\/www.jkscience.org\/archive\/111\/18-RL-JACORD%20ARTHRITIS.pdf","dc:description":"A case of a patient with rheumatic valvulardisease who had comparable deformities of the handsand fingers and who fulfilled all of the criteriasuggested by Bywaters to describe Jaccoud's Arthritis is decribed here.","dc:title":"Jaccoud\u2019s Arthritis"}}}},{"record":{"header":{"header:content":{"core:repositoryIdentifier":"140","identifier":"60225"},"header:attr":{"xmlns:core":"http:\/\/core.kmi.open.ac.uk\/api\/doc"}},"metadata":{"oai_dc:dc":{"oai_dc:ns":[{"xmlns:oai_dc":"http:\/\/www.openarchives.org\/OAI\/2.0\/oai_dc\/","xmlns:dc":"http:\/\/purl.org\/dc\/elements\/1.1\/"}],"dc:creator":"Zai Liu, Guo Deng, Simon Foster and Andrej Tarkowski","dc:format":"application\/pdf","dc:source":"http:\/\/eprints.whiterose.ac.uk\/21\/1\/ar330.pdf","dc:date":"2001-09-17","dc:identifier":"http:\/\/eprints.whiterose.ac.uk\/21\/1\/ar330.pdf","dc:description":"Staphylococcus aureus is one of the most important pathogens in septic arthritis. To analyse the arthritogenic properties of staphylococcal peptidoglycan (PGN), highly purified PGN from S. aureus was intra-articularly injected into murine joints. The results demonstrate that PGN will trigger arthritis in a dose-dependent manner. A single injection of this compound leads to massive infiltration of predominantly macrophages and polymorphonuclear cells with occasional signs of cartilage and\/or bone destruction, lasting for at least 14 days. Further studies showed that this condition is mediated by the combined impact of acquired and innate immune systems. Our results indicate that PGN exerts a central role in joint inflammation triggered by S. aureus.","dc:title":"Staphylococcal peptidoglycans induce arthritis"}}}},{"record":{"header":{"header:content":{"core:repositoryIdentifier":"143","identifier":"5726004"},"header:attr":{"xmlns:core":"http:\/\/core.kmi.open.ac.uk\/api\/doc"}},"metadata":{"oai_dc:dc":{"oai_dc:ns":[{"xmlns:oai_dc":"http:\/\/www.openarchives.org\/OAI\/2.0\/oai_dc\/","xmlns:dc":"http:\/\/purl.org\/dc\/elements\/1.1\/"}],"dc:creator":"Karambin Mohammad Mehdi and Hashemian Hooman","dc:format":"application\/pdf","dc:source":"http:\/\/journals.tums.ac.ir\/PdfMed.aspx?pdf_med=\/upload_files\/pdf\/12751.pdf&manuscript_id=12751","dc:date":"2009","dc:identifier":"http:\/\/journals.tums.ac.ir\/PdfMed.aspx?pdf_med=\/upload_files\/pdf\/12751.pdf&manuscript_id=12751","dc:description":"To determine the rate of different types of arthritis in children. We prepared a retrospective descriptive study and included the whole 100 cases of arthritis referred to 17-Shahrivar Hospital, Rasht, Guilan during a 3 years period. Using their medical files, data including age, sex, season of admission, history of trauma, signs and symptoms, lab findings and duration of hospitalization were collected. SPSS 13.0 (statistical software) applied for statistical analysis. The most common age of involvement ranged 6-9 years. Septic arthritis, brucellosis, and rheumatoid fever were the most frequent causes of arthritis in our study. Fever and restricted range of motion had the highest rate among different signs and symptoms. Lab data demonstrated leukocytosis, positive CRP, and increased ESR among 74, 79.5, and 73 percent of our patients, respectively. According to the high prevalence of septic arthritis and the arthritis due to brucellosis and rheumatoid fever, it seems that mentioned diseases are still major problems in the issue of hygiene management.","dc:title":"Childhood Arthritis: Rate of Different Types"}}}}]}'''


class SimpleTest(TestCase):

    def setUp(self):
        os.environ['CORE_API_KEY'] = 'Not really an API key'

    @httpretty.activate
    def test_core_search_success(self):
        """
        Test that a successful request is proxied correctly
        """
        httpretty.register_uri(
            httpretty.GET,
            "http://core.kmi.open.ac.uk/api/search/arthritis",
            body=SAMPLE_ARTHRITIS)

        c = Client()
        response = c.get('/metadata/coresearch.json/arthritis')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, SAMPLE_ARTHRITIS)

    @httpretty.activate
    def test_core_search_failure(self):
        """
        Test that a failed request is passed on
        """
        httpretty.register_uri(
            httpretty.GET,
            "http://core.kmi.open.ac.uk/api/search/arthritis",
            body='ERROR',
            status=418)

        c = Client()
        response = c.get('/metadata/coresearch.json/arthritis')

        self.assertEqual(response.status_code, 502)

        response_info = json.loads(response.content)
        self.assertTrue('error' in response_info)
        self.assertEqual(response_info['error']['status'], 418)
        self.assertEqual(response_info['error']['content'], 'ERROR')
