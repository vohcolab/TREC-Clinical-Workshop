---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.1
  kernelspec:
    display_name: workshop_21.6
    language: python
    name: workshop_21.6
---

# Meta

This notebook generates the data required for the workshop using the original dataset from [csiro](https://dl.acm.org/doi/abs/10.1145/2911451.2914672). All data is stored under `data/`


```python
import os
import xml.etree.ElementTree as ET
import pandas as pd
from trectools import TrecQrel
from trectools.trec_topics import TrecTopics
from bs4 import BeautifulSoup
import codecs
import xml
```

# Get Patients

```python
topics_path = '/nas/Datasets/csiro_ct/topics-2014_2015-description.topics'
topicsParser = TrecTopics()
# note, for some reason tags have to be in lower_case for this to work. seems to be due to beautifulsoup
topicsParser.read_topics_from_file(topics_path, topic_tag='top',numberid_tag='num',querytext_tag='title',number_attr=False)
patients = topicsParser.topics.copy()
```

```python
print(f'There are {len(patients)} patients in our database')
```

# Get qrels

```python
qrels_file = "/nas/Datasets/csiro_ct/qrels-clinical_trials.txt"
qrels = TrecQrel(qrels_file)

# Internally TrecTools save the objects as Pandas dataframes
qrels = qrels.qrels_data
# some preprocessing
qrels = (qrels
         .rename(columns={'query':'qid'})
         .astype({'qid':str})
        )

# print
qrels.head(3)
qrels.shape
```

# select patients that only exist in qrels & topics

```python
patients_in_qrels_not_topics = [e for e in qrels.qid.unique() if e not in patients.keys()]
patients_in_topics_not_qrels = [e for e in patients.keys() if e not in qrels.qid.unique()]

print(f'Patients in qrels but not in topics: {len(patients_in_qrels_not_topics)}')
print(f'Patients in topics but not in qrels: {len(patients_in_topics_not_qrels)}')
```

```python
common_patients = [e for e in qrels.qid.unique() if e in patients.keys()]

patients = {p:patients[p] for p in common_patients}
print(f'We have {len(patients)} common patients!')
```

```python
# now do the same for qrels (only select patients that exist on both sides)
qrels = qrels[qrels.qid.isin(common_patients)]
qrels.head(3)
qrels.shape
```

# Save patients data

```python
# data in format acceptable to pandas
data = [{'patient_id':e[0],'description':e[1]} for e in list(patients.items())]
df = pd.DataFrame(data).set_index('patient_id')
df.head(2)
df.shape
df.to_csv('../data/patients_sample.csv')
```

# Save qrels data

```python
qrels.drop(columns={'q0'}).to_csv('../data/qrels_sample.csv',index=False)
```

# Now onto the documents

Let's read the documents that exist in the qrels file

```python
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
```

```python
documents = qrels.docid.unique().tolist()
documents_dir = '/nas/Datasets/csiro_ct/clinicaltrials.gov-16_dec_2015/'
doc_list = []
none_list = []
for docid in documents:
    document_file = os.path.join(documents_dir,docid) + '.xml'
    root = ET.parse(document_file).getroot()
    doc = gen_simple_doc(root)
    if doc is None:
        none_list.append(docid)
    else:
        doc_list.append(doc)
        
print(f'Docs that are in qrels but not in collection: {none_list}')

# build sample collection
collection = pd.DataFrame(doc_list)
collection.head(3)
collection.shape
```

# Save the sample collection of documents

```python
collection.to_csv('../data/sample_collection.csv',index=False)
```

```python

```
