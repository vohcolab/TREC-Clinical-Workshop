# ---
# jupyter:
#   jupytext:
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import sys
import os

import xml
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm.notebook import tqdm
from optparse import OptionParser
# -

op = OptionParser()
op.add_option("-o",
              dest="output_folderpath", type="str",
              help="Specify output folder to save the sample colection")
op.add_option("-i",
              dest="dataset_root", type="str",
              help="Specify root path of the clinical trials dataset")
op.add_option("-n",
              dest="max_sample_size", type="int",
              help="Specify the sample collection size")


def gen_simple_doc(root : xml.etree.ElementTree.Element) -> dict:
    """
    Columns that comprise a doc:
        'id' using nct_id
        'summary' using brief_summary
        'gender' using eligibility.gender
        'min_age' using eligibility.minimum_age
        'max_age' using eligibility.maximum_age
    """
    try:
        id_ = root.find('id_info').find('nct_id').text
        title = root.find('brief_title').text
        summary = root.find('brief_summary')[0].text
        gender = root.find('eligibility').find('gender').text
        min_age = root.find('eligibility').find('minimum_age').text
        max_age = root.find('eligibility').find('maximum_age').text

        doc = {'id':id_,'title':title, 'summary':summary,'gender':gender,'min_age':min_age,'max_age':max_age}
    except:
        doc = None
    return doc


def create_collection_sample_to_csv(dataset_root, save_path, max_collection_size):
    """
    Creates a sample of max_collection_size documents in a csv format.
    Current version is not even a real sample as it generates saple in an orderly manner.
    
    Supported columns are defined in the function <gen_simple_doc>
    """
    docs = []
    ignored_docs = 0

    i = 0
    stop = False

    for part in os.listdir(dataset_root):
        part_path = os.path.join(dataset_root,part)
        for folder in os.listdir(part_path):
            folder_path = os.path.join(part_path,folder)
            files = os.listdir(folder_path)
            for file in files:
                filepath = os.path.join(folder_path,file)

                # read and parse file
                root = ET.parse(filepath).getroot()
                doc = gen_simple_doc(root)

                if not doc:
                    ignored_docs +=1
                    continue

                docs.append(doc)
                i +=1

                if i % 1000 == 0:
                    print(f'Progress {i}/{max_collection_size}')

                if i == max_collection_size:
                    print(folder)
                    print(file)
                    stop = True
                    break


            if stop:
                break
        if stop:
            break
    print('Success!')
    print(f'ignored docs: {ignored_docs}')

    df = pd.DataFrame(docs)
    save_file = os.path.join(save_path,f"{max_collection_size}.csv")
    df.to_csv(save_file,index=False)
    return True
# +
# script
argv = sys.argv[1:]
(opts, args) = op.parse_args(argv)

output_folderpath = opts.output_folderpath
dataset_root = opts.dataset_root
max_collection_size = opts.max_sample_size
create_collection_sample_to_csv(dataset_root,output_folderpath,max_collection_size)

