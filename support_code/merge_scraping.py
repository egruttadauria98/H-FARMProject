#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pandas as pd


def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n+1:]
        # put `first` in its own subset
        yield [[first]] + smaller


def get_level(partition_list):
    n = 0

    for partition in partition_list:
        if len(partition) > n:
            n = len(partition)

    return n


def get_main_partition(partition_list, level):

    for partition in partition_list:
        if len(partition) == level:
            return partition


def extract_best_match(d):
    partition_range = list(range(len(d)))
    starting_level = len(d)
    list_intersection_by_level = list()

    #print(partition_range)
    #print(starting_level)

    #p = partition(partition_range)
    #for n, pi in enumerate(p):
    #    print(n, pi)

    for k, partition_list_index in enumerate(partition(partition_range)):
        level = get_level(partition_list_index)
        main_partition_index = get_main_partition(partition_list_index, level)

        #print(k)
        #print(level)
        #print(main_partition_index)

        if level != starting_level:
            if len(flat_list) > 0:
                #print('end function')
                return random.choice(flat_list), level

            #print('update level and list intersection')
            starting_level = level
            list_intersection_by_level = list()

        lists_to_intersect = [val for u, val in enumerate(d.values()) if u in main_partition_index]
        #print(lists_to_intersect)
        intersec_result = list(set(lists_to_intersect[0]).intersection(*lists_to_intersect))
        list_intersection_by_level.append(intersec_result)
        flat_list = [item for sublist in list_intersection_by_level for item in sublist]
        #print(flat_list)

        if k == len(list(partition(partition_range)))-1:
            # As of now, just random assign match first work b/c usually more relevant
            #print('exit with last element')
            try:
                return random.choice(flat_list), level
            except IndexError:
                return None, level


db = pd.read_csv('data.nosync/cfdb.csv')
db = pd.DataFrame(db.loc[:, 'desc'].unique(), columns=['Unique_desc'])
db['scraped'] = 0
db['name_scraped'] = None
db['path_scraped'] = None
db['match_percentage'] = 0

df_scraped = pd.read_csv('data.nosync/premium_price_products.csv')
df_scraped = df_scraped.iloc[:, 1:]
df_scraped = df_scraped.reset_index(drop=True)

exact = True

print(exact)

for i, prod in enumerate(db['Unique_desc']):

    #print(i)
    #print(prod)
    #print('***')

    d = dict()

    split_name = prod.split()

    for j, name in enumerate(split_name):
        #print(j)
        #print(name)

        l = list()

        for scraped_item in df_scraped['ProductName']:
            if exact:
                if name in scraped_item.split():
                    l.append(scraped_item)
            
            else:
                if name in scraped_item:
                    l.append(scraped_item)

        # so that can use same indexing as with lists
        d[j] = l

    match, level = extract_best_match(d)
    percentage_match = level/len(split_name)

    if match is not None:
        db.loc[i, 'scraped'] = 1
        db.loc[i, 'name_scraped'] = match

        path_scraped = df_scraped[df_scraped['ProductName'] == match]['FullPath'].values[0]
        db.loc[i, 'path_scraped'] = path_scraped

        db.loc[i, 'match_percentage', ] = percentage_match

    if i % 100 == 0:
        print('Program at {:.2f} %'.format(i*100/db.shape[0]))

if exact:
    ending_file = 'exact'
else:
    ending_file = 'soft'
        
db.to_csv('data.nosync/name_pairing_{}.csv'.format(ending_file))