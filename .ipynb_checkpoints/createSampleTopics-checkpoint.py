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
              dest="output", type="str",
              help="Specify output folder to save the sample topics")
op.add_option("-i",
              dest="topics_file", type="str",
              help="Specify root path of the clinical trials dataset")
op.add_option("-n",
              dest="max_sample_size", type="int",
              help="Specify the sample size")


def topic2dict(topic : xml.etree.ElementTree.Element) -> dict:
    """
    keys that comprise a topic:
        'topicno' using .attrib
        'text' using text
    """
    topicno = int(topic.attrib['number'])
    topic_text = topic.text

    topic_dict = {'patient_id':topicno,'text':topic_text}

    return topic_dict


def create_topic_sample_to_csv(topics_file, output_folder, max_size):
    """
    Creates a sample of max_collection_size documents in a csv format.
    Current version is not even a real sample as it generates sample in an orderly manner.
    
    Supported columns are defined in the function <topic2dict>
    """
    parsed_topics = []
    
    root = ET.parse(topics_file).getroot()
    all_topics = root.findall('topic')
    
    i = 0
    for topic in all_topics:
        topic_dict = topic2dict(topic)
        
        parsed_topics.append(topic_dict)
        i += 1
        
        if i == max_size:
            break

        
    output_file = os.path.join(output_folder,f"patients_{i}.csv")
    
    df = pd.DataFrame(parsed_topics)
    df.to_csv(output_file,index=False)
    print('Success!')
    return True
# +
# script
argv = sys.argv[1:]
(opts, args) = op.parse_args(argv)

output_folderpath = opts.output
topics_file = opts.topics_file
max_size = opts.max_sample_size
create_topic_sample_to_csv(topics_file,output_folderpath,max_size)

