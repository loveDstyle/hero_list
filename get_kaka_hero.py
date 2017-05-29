#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import json
import codecs
import collections
from pyquery import PyQuery as pq


def paser_html(html, page):
    hero_perpage_list = []
    doc = pq(html)
    hero_items = doc("tbody.table-player-detail").find("tr[onclick]")

    for index, hero_item in enumerate(hero_items.items(), 1):
        # print(hero_item)
        if page == 14:
            if index >= 48:
                continue
        hero_dict = {}
        hero_name = doc(hero_item).find("img.hero-img-list").parent().text()
        match_id_info = doc(hero_item).find(
            "td[sorttable_customkey]")
        match_id = doc(match_id_info).attr("sorttable_customkey")
        match_reslut = doc(match_id_info).next().next().text()
        match_KDA = doc(match_id_info).next().next().next().text()
        match_items_info = doc(hero_item).find(
            'td[style="text-align: left;"]').find('a')
        match_items = list(i.find("img").attr("src")
                           for i in match_items_info.items())
        # print(hero_name, match_id, match_reslut, match_KDA, match_items)
        hero_dict["hero_name"] = hero_name
        hero_dict["value"] = {"match_id": match_id, "match_reslut": match_reslut, "match_KDA": match_KDA,
                              "match_items": match_items}
        hero_perpage_list.append(hero_dict)

    return hero_perpage_list


def get_hero_count_list():
    hero_list = []
    for page in range(1, 15):
        url = "http://dotamax.com/player/match/139876032/?skill=pro&ladder=&hero=-1&p={}".format(
            page)
        response = requests.get(url)
        if response.text:
            hero_perpage_list = paser_html(response.text, page)
            print(page)
            hero_list.extend(hero_perpage_list)
        time.sleep(3)
        # break
    return hero_list


def main():
    hero_dict = {}
    hero_list = get_hero_count_list()
    for hero_item in hero_list:
        if hero_item["hero_name"] not in hero_dict:
            hero_dict[hero_item["hero_name"]] = [hero_item["value"]]
        if hero_item["hero_name"] in hero_dict:
            hero_dict[hero_item["hero_name"]].append(hero_item["value"])
    with codecs.open("hero_dict.json", "w", "utf-8") as f:
        f.write(json.dumps(hero_dict, indent=4))
    hero_count_list = []
    for k, v in hero_dict.items():
        hero_count_list.append([len(v), k])
    out = sorted(hero_count_list, reverse=True)
    for i in out:
        print(i[1], i[0])


if __name__ == "__main__":
    main()
