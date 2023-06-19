import os
import json
import requests
import numpy as np
from bs4 import BeautifulSoup
from translate import Translator


def get_element(dom_tree, selector=None, attribute=None, return_list=False):
    try:
        if return_list:
            return ", ".join(tag.text.strip() for tag in dom_tree.select(selector))
        if attribute:
            if selector:
                return dom_tree.select_one(selector)[attribute].text.strip()
            return dom_tree[attribute]
        return dom_tree.select_one(selector).text.strip()
    
    except (AttributeError, TypeError):
        return None
    
def clean_text(text):
    return ' '.join(text.replace(r"\s", " ").split())

selectors = {
    "opinion_id": [None, "data-entry-id"],
    "author": ["span.user-post__author-name"],
    "recommendation": ["span.user-post__author-recommendation > em"],
    "score": ["span.user-post__score-count"],
    "description": ["div.user-post__text"],
    "pros": ["div.review-feature__col:has( > div.review-feature__title--positives) > div.review-feature__item", None, True],
    "cons": ["div.review-feature__col:has( > div.review-feature__title--negatives) > div.review-feature__item", None, True],
    "like": ["button.vote-yes > span"],
    "dislike": ["button.vote-yes > span"],
    "publish_date": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "purchase_date": ["span.user-post__published > time:nth-child(2)", "datetime"]
    }


product_code = "129901214"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
all_opinions = []

from_lang = "pl"
to_land = "en"
translator = Translator(to_land, from_lang)

while url:
    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        page_done = BeautifulSoup(response.text, 'html.parser')
        opinions = page_done.select("div.js_product-review")
        
        if len(opinions) > 0:

            for opinion in opinions:
                
                single_opinion = {}

                for key, value in selectors.items():
                    single_opinion[key] = get_element(opinion, *value)

                single_opinion["recommendation"] = True if single_opinion["recommendation"] == "Polecam" else False if single_opinion["recommendation"] == "Nie polecam" else None
                single_opinion["score"] = np.divide(*[float(score.replace(",", ".")) for score in single_opinion["score"].split("/")])
                single_opinion["like"] = int(single_opinion["like"])
                single_opinion["dislike"] = int(single_opinion["dislike"])
                single_opinion["description"] = clean_text(single_opinion["description"])
                single_opinion["description_en"] = translator.translate(single_opinion["description"][:500])
                single_opinion["pros_en"] = translator.translate(single_opinion["pros"])
                single_opinion["cons_en"] = translator.translate(single_opinion["cons"])

                all_opinions.append(single_opinion)

            try:
                url = "https://www.ceneo.pl" + get_element(page_done, "a.pagination__next", "href")
            except TypeError:
                url = None

        else:
            print(f"There are no opinions about product with code {product_code}")
            url = None

if not os.path.exists("opinions"):
    os.mkdir("opinions")
with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)

print(response.status_code)