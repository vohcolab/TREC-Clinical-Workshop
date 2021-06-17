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
    display_name: Python 3
    language: python
    name: python3
---

# Welcome

The process of manually searching for clinical trials is very resource intensive and should be automated by a computer.

## Problem
It is very costly (human resources) to manually check each patient description and assign them to a clinical trial

## Objective

Create an algorithm that automatically assigns possible candidates (patients) to clinical trials

```python
import pandas as pd
```

# Data

```python
!ls ../data
```

```python
clinical_trials = pd.read_csv('../data/sample_collection.csv')
patients = pd.read_csv('../data/patients_sample.csv')
relevance = pd.read_csv('../data/qrels_sample.csv')
```

```python
clinical_trials.head(2)
clinical_trials.shape

patients.head(2)
patients.shape
```

<!-- #region -->
# Let's go easy


Main objective: Match based on **gender** requirements
<!-- #endregion -->

## Part 1: Divide and conquer

We have a big objective but in order to solve it let's divide it into smaller objectives that are easier to complete.

<br>

**Sub-objectives**:
- **A**: Detect gender from patient description
- **B**: Go through each trial and assign patients based on their gender

```python
def naive_man_detector(text):

    possible_male_references = ['man', 'male', 'm']
    
    # convert everything to lower case
    text = text.lower() # possible exercise!!
    
    # usually gender is in the first sentence
    # so let's pick the first ~100 characters to find the gender
    first_part = text[:100]
    
    words = first_part.split(" ")
    
    for word in words:
        if word in possible_male_references:
            return True
    return False
```

```python
patients['is_male'] = patients.description.apply(naive_man_detector)
```

Now that we can classify each patient in gender, lets assign patients to clinical trials

```python
patient2trials = {}

for patient in patients.itertuples(index=False):

    patient_id = patient.patient_id
    patient_description = patient.description
    gender = 'male' if patient.is_male == True else 'female'
    
    patient2trials[patient_id] = []
    for trial in clinical_trials.itertuples(index=False):
        if patient.is_male == True and trial.gender in ['All', 'Male']:
            patient2trials[patient_id].append(trial)
        elif patient.is_male == False and trial.gender in ['All','Female']:
            patient2trials[patient_id].append(trial)
            
    print(f'Patient {patient_id} is believed to be a {gender} and was matched to {len(patient2trials[patient_id])} trials!')
```
