import argparse
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
import json
import re

snowball = SnowballStemmer("english") 
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def transform_name(product_name):
    parts = word_tokenize(product_name)
    parts = [p.lower() for p in parts]
    parts = [p for p in parts if p not in stopwords.words('english')]
    parts = [snowball.stem(p) for p in parts]
    parts = [p for p in parts if not p.isdigit()]
    parts = [p for p in parts if not is_float(p)]
    parts = [p for p in parts if len(p) > 1 and p != "''"]
    parts = [re.sub(r'\W+','', p).strip() for p in parts]
    return " ".join(parts)

# Directory for product data
directory = r'/workspace/search_with_machine_learning_course/data/pruned_products/'

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=directory,  help="The directory containing product data")
general.add_argument("--output", default="/workspace/datasets/fasttext/output.fasttext", help="the file to output to")

# Consuming all of the product data will take over an hour! But we still want to be able to obtain a representative sample.
general.add_argument("--sample_rate", default=1.0, type=float, help="The rate at which to sample input (default is 1.0)")

# IMPLEMENT: Setting min_products removes infrequent categories and makes the classifier's task easier.
general.add_argument("--min_products", default=0, type=int, help="The minimum number of products per category (default is 0).")

args = parser.parse_args()
output_file = args.output
path = Path(output_file)
output_dir = path.parent
if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)

if args.input:
    directory = args.input
# IMPLEMENT:  Track the number of items in each category and only output if above the min
min_products = args.min_products
sample_rate = args.sample_rate

cat_counts = {}
print("Writing results to %s" % output_file)
with open(output_file + "_temp", 'w') as output:
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            print("Processing %s" % filename)
            f = os.path.join(directory, filename)
            tree = ET.parse(f)
            root = tree.getroot()
            for child in root:
                if random.random() > sample_rate:
                    continue
                # Check to make sure category name is valid
                if (child.find('name') is not None and child.find('name').text is not None and
                    child.find('categoryPath') is not None and len(child.find('categoryPath')) > 0 and
                    child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text is not None):
                      # Choose last element in categoryPath as the leaf categoryId

                      children = child.find('categoryPath')

                      if len(children) > 3:
                          cat = child.find('categoryPath')[2][0].text
                      else:
                        cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text
                      # Replace newline chars with spaces so fastText doesn't complain
                      name = child.find('name').text.replace('\n', ' ')
                      json_to_write = {"cat" : cat, "name": transform_name(name) }
                      # output.write("__label__%s %s\n" % (cat, transform_name(name)))
                      output.write(json.dumps(json_to_write) + "\n")

                      if cat not in cat_counts:
                          cat_counts[cat] = 0
                      cat_counts[cat]  = cat_counts[cat] + 1

rejected_cats = set()
rejected_pdts = 0

with open(output_file, 'w') as output:
    with open(output_file + "_temp") as inp:
        for line in inp.readlines():
            obj = json.loads(line)
            cat = obj["cat"]
            name = obj["name"]
            if min_products is not None and cat_counts[cat] < min_products :
                rejected_cats.add(cat)
                rejected_pdts = rejected_pdts + 1
                continue
            output.write("__label__%s %s\n" % (cat, name))

print(f"Total number of rejected categories {len(rejected_cats)}")
print(f"Total number of rejected products {rejected_pdts}")