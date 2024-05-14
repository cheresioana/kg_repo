import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from  logs import logger
from tests.populate_db import populate
from constanst import AGGREGATOR_URL

from DataObject.SubGraphResult import ComplexEncoder, ResultItem, Node, Link


from SearchEngine import SearchEngine

import random
from collections import Counter
from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin
import requests
from Neo4JConnector.NeoConnector import (NeoConnector)
from ChatGPT.ChatGPTWrapper import ChatGPTWrapper
from Neo4JConnector.NeoAlgorithms import (NeoAlgorithms)
import pandas as pd
import time

app = Flask(__name__)

neo_aglo = NeoAlgorithms()
connector = NeoConnector()
chat = ChatGPTWrapper()
search_engine = SearchEngine()

CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

#df = pd.read_csv('data/data2.csv')

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200

@app.route('/sample_kg', methods=['GET'])
def get_sample_kg():
    N = 10  # or whatever value you want

    gData = {
        "nodes": [{"id": i} for i in range(N)],
        "links": [
            {
                "source": id,
                "target": round(random.random() * (id - 1))
            }
            for id in range(1, N)  # Python's range is [start, end) exclusive the end.
        ]
    }

    return jsonify(gData)


@app.route('/get_kg', methods=['GET'])
def get_kg():
    logger.info("Get /get_kg")
    print("get kg")
    kg = connector.get_kg()
    with open("sample.json", "w") as outfile:
        json.dump(kg, outfile)
    return jsonify(kg)


@app.route('/get_similar/<id>', methods=['GET'])
def get_similar_kg(id):
    similar_list = connector.get_similar(id)
    return jsonify(similar_list)

@app.route('/analyze2_test', methods=['POST'])
def analyze2_test():

    return {
    "origin": [
        {
            "intra_id": 69956,
            "statement": "USA is evil",
            "tag": "query",
            "id": 69956,
            "community": 0
        }
    ],
    "keywords": [],
    "all_results": [
        {
            "intra_id": 45853,
            "query_id": 69956,
            "selected": 1,
            "statement": "The USA fights with the Nord Stream and the Russian nuclear industry to eliminate more advanced competition",
            "date": "04.12.2020",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-fights-with-the-nord-stream-and-the-russian-nuclear-industry-in-order-to-eliminate-more-advanced-competition/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 83305,
            "query_id": 69956,
            "selected": 1,
            "statement": "Bundeswehrkommando works in the USA and Canada",
            "date": "27.06.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/bundeswehrkommando-arbeitet-in-den-usa-und-kanada/",
            "languages": ""
        },
        {
            "intra_id": 50951,
            "query_id": 69956,
            "selected": 1,
            "statement": "USA hopes to partition Russia after the end of Putin\u2019s Presidency",
            "date": "09.03.2020",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-hopes-that-after-the-end-of-putins-presidency-there-will-be-a-possibility-for-the-partition-of-russia/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 52827,
            "query_id": 69956,
            "selected": 1,
            "statement": "The USA will fulfil NATO\u2019s Article 5 only if it is required by its national interests",
            "date": "22.11.2019",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-will-fulfill-natos-article-5-only-if-it-is-required-by-its-national-interests/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 31551,
            "query_id": 69956,
            "selected": 1,
            "statement": "USA has occupied Germany as a colonial power for eight decades",
            "date": "24.02.2024",
            "channel": [
                "de.rt.com"
            ],
            "location": [
                "Germany"
            ],
            "url": "https://euvsdisinfo.eu/report/usa-has-occupied-germany-as-a-colonial-power-for-eight-decades/",
            "languages": [
                "German"
            ]
        },
        {
            "intra_id": 5102,
            "query_id": 69956,
            "selected": 1,
            "statement": "The USA will sustain a strategic defeat in Ukraine",
            "date": "16.02.2024",
            "channel": "",
            "location": [
                "Russia"
            ],
            "url": "https://www.veridica.ro/en/fake-news/war-propaganda-the-usa-will-sustain-a-strategic-defeat-in-ukraine",
            "languages": ""
        },
        {
            "intra_id": 32400,
            "query_id": 69956,
            "selected": 1,
            "statement": "The USA will sacrifice Ukraine",
            "date": "21.12.2023",
            "channel": [
                "report.az"
            ],
            "location": [
                "Azerbaijan"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-will-sacrifice-ukraine/",
            "languages": [
                "Azerbaijani"
            ]
        },
        {
            "intra_id": 33008,
            "query_id": 69956,
            "selected": 1,
            "statement": "The USA blew up the Nord Stream pipeline",
            "date": "31.10.2023",
            "channel": [
                "news.am"
            ],
            "location": [
                "Armenia"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-blew-up-the-nord-stream-pipeline/",
            "languages": [
                "Armenian"
            ]
        },
        {
            "intra_id": 33819,
            "query_id": 69956,
            "selected": 1,
            "statement": "The USA is turning Ukraine into a European Afghanistan",
            "date": "12.08.2023",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-is-turning-ukraine-into-a-european-afghanistan/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 83779,
            "query_id": 69956,
            "selected": 1,
            "statement": "These military vehicles were not intended for Ukraine \u2013 they are relocated to the USA",
            "date": "31.03.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/diese-militrfahrzeuge-waren-nicht-fr-die-ukraine-bestimmt-sie-werden-in-die-usa-zurckverlegt/",
            "languages": ""
        },
        {
            "intra_id": 83803,
            "query_id": 69956,
            "selected": 1,
            "statement": "WEF statement invented: Family size in the USA unlimited",
            "date": "24.03.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/wef-aussage-erfunden-familiengre-in-den-usa-unbegrenzt/",
            "languages": ""
        },
        {
            "intra_id": 83805,
            "query_id": 69956,
            "selected": 1,
            "statement": "Nord-Stream-Sabotage: This quote from Ursula from the Leyen about the \u201cdoodleless reputation\u201d of the USA is invented",
            "date": "24.03.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/nord-stream-sabotage-dieses-zitat-von-ursula-von-der-leyen-ber-den-tadellosen-ruf-der-usa-ist-erfunden/",
            "languages": ""
        },
        {
            "intra_id": 83862,
            "query_id": 69956,
            "selected": 1,
            "statement": "Nato military vehicles are shipped back to the USA",
            "date": "15.03.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/nato-militrfahrzeuge-werden-zurck-in-die-usa-verschifft/",
            "languages": ""
        },
        {
            "intra_id": 35862,
            "query_id": 69956,
            "selected": 1,
            "statement": "The USA wants Ukraine to \u201cfight to the last Ukrainian\u201d",
            "date": "29.12.2022",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-wants-ukraine-to-fight-to-the-last-ukrainian/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 84488,
            "query_id": 69956,
            "selected": 1,
            "statement": "USA support Ukraine in combating biological hazards",
            "date": "09.12.2022",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/usa-untersttzen-ukraine-bei-bekmpfung-biologischer-gefahren/",
            "languages": ""
        },
        {
            "intra_id": 37087,
            "query_id": 69956,
            "selected": 1,
            "statement": "USA and the EU made Ukraine dependent on the West",
            "date": "27.07.2022",
            "channel": [
                "iravunk.com"
            ],
            "location": [
                "Armenia"
            ],
            "url": "https://euvsdisinfo.eu/report/usa-and-the-eu-made-ukraine-dependent-on-the-west/",
            "languages": [
                "Armenian"
            ]
        },
        {
            "intra_id": 39646,
            "query_id": 69956,
            "selected": 1,
            "statement": "The USA creates its lobby within the EU by deploying forces in the Baltic states",
            "date": "11.10.2021",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-creates-its-lobby-within-the-eu-by-deploying-forces-in-the-baltic-states/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 46295,
            "query_id": 69956,
            "selected": 1,
            "statement": "Unlike Russia, Poland is a defenceless country fully dependent on the USA",
            "date": "16.11.2020",
            "channel": [
                "pl.rubaltic.ru"
            ],
            "location": [
                "Russia",
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/unlike-russia-poland-is-a-defenceless-country-fully-dependent-on-the-usa/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 46622,
            "query_id": 69956,
            "selected": 1,
            "statement": "The USA conditions Maia Sandu's victory",
            "date": "04.11.2020",
            "channel": [
                "www.kp.md"
            ],
            "location": [
                "Moldova"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-sets-the-condition-to-win-maia-sandu/",
            "languages": [
                "Russian"
            ]
        },
        {
            "intra_id": 83962,
            "query_id": 69956,
            "selected": 0,
            "statement": "Video shows no tsunami on the coast off Turkey and Syria, but comes from the USA",
            "date": "23.02.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/video-zeigt-keinen-tsunami-an-der-kste-vor-der-trkei-und-syrien-sondern-stammt-aus-den-usa/",
            "languages": ""
        },
        {
            "intra_id": 54459,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA weakens the EU\u2019s military-industrial complex by passing Leopards to Ukraine",
            "date": "28.01.2023",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland",
                "Ukraine"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-weakens-the-eus-military-industrial-complex-by-passing-leopards-to-ukraine/",
            "languages": [
                "Polish",
                "Ukrainian"
            ]
        },
        {
            "intra_id": 35646,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA and NATO push the EU to war by supplying tanks to Ukraine",
            "date": "24.01.2023",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-and-nato-push-the-eu-to-war-by-supplying-tanks-to-ukraine/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 38946,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA wants to use the migration crisis to unleash a war",
            "date": "25.11.2021",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-wants-to-use-the-migration-crisis-to-unleash-a-war/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 39973,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA may inspire new \u201cBrexits\u201d through the Three Seas Initiative",
            "date": "21.09.2021",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-may-inspire-new-brexits-through-the-three-seas-initiative/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 40642,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA can organise a \u201cMaidan\u201d in Poland, exerting pressure on the Polish authorities",
            "date": "11.08.2021",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-can-organise-a-maidan-in-poland-exerting-pressure-on-the-polish-authorities/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 41219,
            "query_id": 69956,
            "selected": 0,
            "statement": "The intrusion of Defender into Russian territorial waters was a UK and USA provocation",
            "date": "08.07.2021",
            "channel": [
                "de.rt.com"
            ],
            "location": [
                "Germany"
            ],
            "url": "https://euvsdisinfo.eu/report/the-intrusion-of-defender-into-russian-territorial-waters-was-a-uk-and-usa-provocation/",
            "languages": [
                "German"
            ]
        },
        {
            "intra_id": 42485,
            "query_id": 69956,
            "selected": 0,
            "statement": "USA is trying to make Ukraine a \"springboard of aggression\" against Russia",
            "date": "18.05.2021",
            "channel": [
                "de.news-front.info"
            ],
            "location": [
                "Germany"
            ],
            "url": "https://euvsdisinfo.eu/report/usa-is-trying-to-make-ukraine-a-springboard-of-aggression-against-russia/",
            "languages": [
                "German"
            ]
        },
        {
            "intra_id": 57391,
            "query_id": 69956,
            "selected": 0,
            "statement": "USA doesn't allow OSCE to observe its elections",
            "date": "06.11.2020",
            "channel": [
                "youtube.com"
            ],
            "location": "",
            "url": "https://euvsdisinfo.eu/report/usa-doesnt-allow-osce-to-observe-the-elections/",
            "languages": [
                "Russian"
            ]
        },
        {
            "intra_id": 47145,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA uses Navalny poisoning in order to promote its expensive fuel to Europe",
            "date": "01.10.2020",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-uses-navalny-poisoning-in-order-to-promote-its-expensive-fuel-to-europe/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 57772,
            "query_id": 69956,
            "selected": 0,
            "statement": "USA admits that they support strikes in Belarus",
            "date": "11.09.2020",
            "channel": [
                "youtube.com"
            ],
            "location": "",
            "url": "https://euvsdisinfo.eu/report/usa-admits-that-they-support-strikes-in-belarus/",
            "languages": [
                "Russian"
            ]
        },
        {
            "intra_id": 48699,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA is planning a coup in Bulgaria in order to subsequently blame Russia",
            "date": "18.06.2020",
            "channel": [
                "bgr.news-front.info"
            ],
            "location": [
                "Bulgaria"
            ],
            "url": "https://euvsdisinfo.eu/report/usa-is-planning-a-coup-in-bulgaria-in-order-to-subsequently-blame-russia/",
            "languages": [
                "Bulgarian"
            ]
        },
        {
            "intra_id": 48808,
            "query_id": 69956,
            "selected": 0,
            "statement": "USA wants to divide Russian society before the constitutional referendum",
            "date": "11.06.2020",
            "channel": [
                "deutsch.rt.com"
            ],
            "location": [
                "Germany"
            ],
            "url": "https://euvsdisinfo.eu/report/usa-wants-to-divide-russian-society-before-constitutional-referendum/",
            "languages": [
                "German"
            ]
        },
        {
            "intra_id": 49509,
            "query_id": 69956,
            "selected": 0,
            "statement": "Ukraine and the Baltic states want to present the USSR as an \u201cabsolute evil\u201d in WWII",
            "date": "11.05.2020",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/ukraine-and-the-baltic-states-want-to-present-the-ussr-as-an-absolute-evil-in-wwii/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 49797,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA will force Poland to buy more American weapons to support its struggling economy",
            "date": "28.04.2020",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-will-force-poland-to-buy-more-american-weapons-to-support-its-struggling-economy/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 50106,
            "query_id": 69956,
            "selected": 0,
            "statement": "Polish Strategy of National Security was written under the dictation of the USA",
            "date": "13.04.2020",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-polish-strategy-of-national-security-was-written-under-the-dictation-of-the-usa/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 51124,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA promotes the cult of Nazi collaborators throughout Eastern Europe to spread its military presence in the region",
            "date": "27.02.2020",
            "channel": [
                "pl.sputniknews.com"
            ],
            "location": [
                "Poland"
            ],
            "url": "https://euvsdisinfo.eu/report/the-usa-promotes-the-cult-of-nazi-collaborators-throughout-eastern-europe-in-order-to-spread-its-military-presence-in-the-region/",
            "languages": [
                "Polish"
            ]
        },
        {
            "intra_id": 51659,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA is to blame for the coronavirus in China",
            "date": "03.02.2020",
            "channel": [
                "tsargrad.tv",
                "twitter.com",
                "nsn.fm"
            ],
            "location": [
                "Tuvalu",
                "Micronesia"
            ],
            "url": "https://euvsdisinfo.eu/report/the-us-is-to-blame-for-the-coronavirus-in-china/",
            "languages": [
                "Russian",
                "French"
            ]
        },
        {
            "intra_id": 4591,
            "query_id": 69956,
            "selected": 0,
            "statement": "The name of Volodimir Zelenski translates into Spanish as \"the evil one owns the world.\"FAKE",
            "date": "02.04.2024",
            "channel": "",
            "location": [
                "Spain"
            ],
            "url": "https://info-veritas.com/desinformacion_el-nombre-de-volodimir-zelenski-incorrecta-traduccion/",
            "languages": [
                "Spanish"
            ]
        },
        {
            "intra_id": 94147,
            "query_id": 69956,
            "selected": 0,
            "statement": "FACT CHECK | Pictures about the \"companies\" of the Republic of Estonia are spreading on social media. These are Estonian embassies in the USA",
            "date": "28.02.2024",
            "channel": "",
            "location": [
                "Estonian"
            ],
            "url": "https://epl.delfi.ee/artikkel/120273876/faktikontroll-sotsiaalmeedias-levivad-pildid-eesti-vabariigi-ettevotete-kohta-tegemist-on-eesti-saatkondadega-usas",
            "languages": ""
        },
        {
            "intra_id": 5114,
            "query_id": 69956,
            "selected": 0,
            "statement": "Economic partnerships with the USA lead to bankruptcy",
            "date": "13.02.2024",
            "channel": [
                "t.me"
            ],
            "location": [
                "Ecuador"
            ],
            "url": "https://www.veridica.ro/en/fake-news/fake-news-economic-partnerships-with-the-usa-lead-to-bankruptcy",
            "languages": ""
        },
        {
            "intra_id": 53382,
            "query_id": 69956,
            "selected": 0,
            "statement": "USA wants to starve millions just to annoy Russia",
            "date": "02.02.2024",
            "channel": [
                "freedert.online"
            ],
            "location": "",
            "url": "https://euvsdisinfo.eu/report/usa-wants-to-starve-millions-just-to-annoy-russia/",
            "languages": [
                "German"
            ]
        },
        {
            "intra_id": 53647,
            "query_id": 69956,
            "selected": 0,
            "statement": "USA behind Arab Spring",
            "date": "17.11.2023",
            "channel": [
                "respublika-news.az"
            ],
            "location": [
                "Azerbaijan"
            ],
            "url": "https://euvsdisinfo.eu/report/usa-behind-arab-spring/",
            "languages": [
                "Azeri"
            ]
        },
        {
            "intra_id": 82628,
            "query_id": 69956,
            "selected": 0,
            "statement": "Fake video of alleged convocation in the USA reappears during the war of Israel",
            "date": "25.10.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/geflschtes-video-von-angeblicher-einberufung-in-den-usa-taucht-im-zuge-des-israelkriegs-wieder-auf/",
            "languages": ""
        },
        {
            "intra_id": 82638,
            "query_id": 69956,
            "selected": 0,
            "statement": "Videos incorrectly translated: Putin did not warn the USA to stay away from war in the Middle East",
            "date": "24.10.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/videos-falsch-bersetzt-putin-warnte-die-usa-nicht-sich-vom-krieg-im-nahen-osten-fernzuhalten/",
            "languages": ""
        },
        {
            "intra_id": 82660,
            "query_id": 69956,
            "selected": 0,
            "statement": "Wrong translated: Erdo\u011fan does not warn the USA in this video to keep away from war in the Middle East",
            "date": "18.10.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/falsch-bersetzt-erdoan-warnt-die-usa-in-diesem-video-nicht-sich-vom-krieg-im-nahen-osten-fernzuhalten/",
            "languages": ""
        },
        {
            "intra_id": 82692,
            "query_id": 69956,
            "selected": 0,
            "statement": "Fake document proves no eight billion dollars military aid from the USA to Israel",
            "date": "12.10.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/geflschtes-dokument-belegt-keine-acht-milliarden-dollar-militrhilfe-von-den-usa-an-israel/",
            "languages": ""
        },
        {
            "intra_id": 26899,
            "query_id": 69956,
            "selected": 0,
            "statement": "The new Rhein/Neue Ruhr Zeitung titles in one article: \"The USA prepares a plan for the division of Ukraine based on the model of South Korea\".",
            "date": "09.08.2023",
            "channel": "",
            "location": [
                "Germany"
            ],
            "url": "https://correctiv.org/faktencheck/2023/08/23/gefaelschter-nrz-artikel-ueber-angebliche-teilungsplaene-netzwerk-von-twitter-bots-macht-stimmung-gegen-die-ukraine/",
            "languages": [
                "German"
            ]
        },
        {
            "intra_id": 83570,
            "query_id": 69956,
            "selected": 0,
            "statement": "Obama was legitimate president of the USA",
            "date": "10.05.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/obama-war-legitimer-prsident-der-usa/",
            "languages": ""
        },
        {
            "intra_id": 83738,
            "query_id": 69956,
            "selected": 0,
            "statement": "Sharepic shows wind turbines in the USA, not in Germany",
            "date": "12.04.2023",
            "channel": "",
            "location": [
                "German"
            ],
            "url": "https://gadmo.eu/sharepic-zeigt-windrder-in-den-usa-nicht-in-deutschland/",
            "languages": ""
        },
        {
            "intra_id": 5888,
            "query_id": 69956,
            "selected": 0,
            "statement": "The USA will dispatch 200 thousand Ukrainian suicide bombers who will take their orders from the Pentagon",
            "date": "10.04.2023",
            "channel": [
                "svpressa.ru"
            ],
            "location": [
                "Russia"
            ],
            "url": "https://www.veridica.ro/en/fake-news/war-propaganda-the-usa-will-dispatch-200-thousand-ukrainian-suicide-bombers-who-will-take-their-orders-from-the-pentagon",
            "languages": ""
        }
    ]
    }


@app.route('/get_graph', methods=['POST'])
def get_graph():
    data = request.get_json()
    logger.info(f"analyze2 {data}")
    print(data['ids'])
    nodes, links = search_engine.get_nodes(data['ids'])
    nodes_dict = [node.to_dict() for node in nodes]
    return json.dumps({
        'nodes': nodes_dict,
        'links': links
    }, indent=4)

@app.route('/expand_node', methods=['POST'])
def expand_node():
    data = request.get_json()
    logger.info(f"expand node {data}")
    print(data)
    print(data['node_id'])
    print(data['query_id'])
    print(data['current_results'])
    print(data['all_nodes_ids'])

    nodes, links = search_engine.expand_node(data['node_id'], data['query_id'], data['current_results'])
    nodes = [node for node in nodes if node.id not in data['all_nodes_ids'] ]
    nodes_dict = [node.to_dict() for node in nodes]
    return json.dumps({
        'nodes': nodes_dict,
        'links': links
    }, indent=4)


@app.route('/analyze2', methods=['POST'])
def analyze2():
    data = request.get_json()
    logger.info(f"analyze2 {data}")

    start_time = time.time()
    keywords, show_links, show_nodes, path_result, origin_node = search_engine.find_results(data['statement'])
    duration = time.time() - start_time
    logger.info(f"The search took {duration} seconds to run.")
    print(f"The search took {duration} seconds to run.")
    json_response = {
        'origin': [origin_node],
        'keywords': keywords,
        'all_results': path_result
    }
    json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
    return json_str


@app.route('/load_more', methods=['POST'])
def load_more():
    data = request.get_json()
    logger.info(f"analyze2 {data}")
    start_time = time.time()
    keywords, show_links, show_nodes, path_result, origin_node = search_engine.find_results(data['statement'], data['skip'])
    duration = time.time() - start_time
    logger.info(f"The search took {duration} seconds to run.")
    print(f"The search took {duration} seconds to run.")
    json_response = {
        'origin': [origin_node],
        'keywords': keywords,
        'all_results': path_result
    }
    json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
    return json_str, 200, {'ContentType': 'application/json'}


# @app.route('/node_info/<id>', methods=['GET'])
# def get_node_info(id):
#     res = df[df['id'] == int(id)]
#     if len(res) == 0:
#         return jsonify([])
#     res.fillna(0, inplace=True)
#     result = res.iloc[0]
#
#     return jsonify(result.to_dict())


@app.route('/addStatement', methods=['POST'])
def addStatement():
    logger.info("ADD STATEMENT")
    data = request.get_json()
    print(data)
    intra_id = data['intra_id']
    query_node = Node(data['origin']['intra_id'], data['origin']['statement'], data['origin']['id'])
    # parsed_data = json.loads(data["all_results"])
    result_items = [
        ResultItem(
            item_data['weight'],
            item_data['intra_id'],
            item_data['query_id'],
            item_data['statement'],
            [Node(**node) for node in item_data['nodes']],  # Convert each dict to a Node instance
            [Link(**link) for link in item_data['links']],  # Convert each dict to a Link instance
            selected=item_data.get('selected', 0),# using .get() in case 'selected' is not present
            date=item_data.get('date', ""),
            channel=item_data.get('channel', ""),
            location=item_data.get('location', ""),
            url=item_data.get('url', "")
        )
        for item_data in data["all_results"]
    ]
    show_nodes = []
    show_links = []
    for result_item in result_items:
        if result_item.selected == 1:
            show_nodes.extend(result_item.nodes)
            show_links.extend(result_item.links)
        elif result_item.intra_id == intra_id:
            show_nodes.extend(result_item.nodes)
            show_links.extend(result_item.links)
            result_item.selected = 1
    show_links = list(set(show_links))
    show_nodes = (list(set(show_nodes)))
    show_nodes.append(query_node)
    json_response = {
        'origin': [query_node],
        'keywords': data['keywords'],
        'links': show_links,
        'nodes': show_nodes,
        'all_results': result_items
    }

    print(result_items[0].weight)
    print(result_items[0].statement)

    json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
    return json_str


@app.route('/removeStatement', methods=['POST'])
def removeStatement():
    print("REMOVE")
    data = request.get_json()
    print(data)
    intra_id = data['intra_id']
    query_node = Node(data['origin']['intra_id'], data['origin']['statement'], data['origin']['id'])
    # parsed_data = json.loads(data["all_results"])
    result_items = [
        ResultItem(
            item_data['weight'],
            item_data['intra_id'],
            item_data['query_id'],
            item_data['statement'],
            [Node(**node) for node in item_data['nodes']],  # Convert each dict to a Node instance
            [Link(**link) for link in item_data['links']],  # Convert each dict to a Link instance
            selected=item_data.get('selected', 0),  # using .get() in case 'selected' is not present
            date=item_data.get('date', ""),
            channel=item_data.get('channel', ""),
            location=item_data.get('location', ""),
            url=item_data.get('url', "")
        )
        for item_data in data["all_results"]
    ]
    show_nodes = []
    show_links = []
    for result_item in result_items:
        if result_item.intra_id == intra_id:
            result_item.selected = 0
        elif result_item.selected == 1:
            show_nodes.extend(result_item.nodes)
            show_links.extend(result_item.links)

    show_links = list(set(show_links))
    show_nodes = (list(set(show_nodes)))
    show_nodes.append(query_node)
    json_response = {
        'origin': [query_node],
        'keywords': data['keywords'],
        'links': show_links,
        'nodes': show_nodes,
        'all_results': result_items
    }

    print(result_items[0].weight)
    print(result_items[0].statement)

    json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
    return json_str

@app.route('/init_db', methods=['GET'])
def init_db():
    populate()
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
