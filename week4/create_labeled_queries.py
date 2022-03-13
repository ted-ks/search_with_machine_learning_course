import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv
import re

# Useful if you want to perform stemming.
import nltk
from nltk import word_tokenize

stemmer = nltk.stem.PorterStemmer()

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/labeled_query_data_1000.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
df = pd.read_csv(queries_file_name)[['category', 'query']]
df = df[df['category'].isin(categories)]

def transform(q):
    q = q.lower()
    q = re.sub(r'\W+', ' ', q)
    parts = word_tokenize(q)
    parts = [stemmer.stem(p) for p in parts]
    parts = [p.strip() for p in parts]
    return " ".join(parts)


def get_parent(cat, leaf_df):
    if cat == "cat00000":
        return "cat00000"
    else:
        return parents_df[parents_df["category"]==cat]["parent"].iloc[0]
# DONE: IMPLEMENT ME: Convert queries to lowercase, and optionally implement other normalization, like stemming.

df["query"] = df['query'].apply(transform)

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.

if min_queries > 1:
    #grp_df = df.groupby(['category']).size().sort_values(ascending=False).to_frame('size')
    grp_df = df.groupby(['category']).size().to_frame('size')


    rem_prune_count = len(grp_df[grp_df["size"] < min_queries])

    while rem_prune_count > 0:
        items = grp_df[grp_df["size"] < min_queries]
        ct = 0
        for i,row in items.iterrows():
            df["category"].replace({i:get_parent(i, parents_df)}, inplace=True)
            print(f"Replacing for {i} #{ct}/{rem_prune_count}")
            ct = ct + 1
        grp_df = df.groupby(['category']).size().to_frame('size')
        rem_prune_count = len(grp_df[grp_df["size"] < min_queries])
        print(f"Remaining to prune {rem_prune_count}")
        print(f"Unique Categories now {len(grp_df)}")

    
# Create labels in fastText format.
df['label'] = '__label__' + df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
df = df[df['category'].isin(categories)]
df['output'] = df['label'] + ' ' + df['query']
df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)
