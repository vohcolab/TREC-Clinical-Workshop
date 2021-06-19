# TREC-Clinical-Workshop


# Notebooks

- [Part 1 Notebook](https://colab.research.google.com/github/vohcolab/TREC-Clinical-Workshop/blob/main/Workshop/ClinicalTrialsMatching-Part1.ipynb)
- [Part 2 Notebook](https://colab.research.google.com/github/vohcolab/TREC-Clinical-Workshop/blob/main/Workshop/ClinicalTrialsMatching-Part2.ipynb)
- [Part 3 Notebook](https://colab.research.google.com/github/vohcolab/TREC-Clinical-Workshop/blob/main/Workshop/ClinicalTrialsMatching-Part3.ipynb)


## Environment

To reproduce and work with this code, create a new conda environment using the following bash command:
```bash
conda env create -n <env_name> -f environment.yml
```
To save new modules, use the following command to update the ``environment.yml`` file:
```bash
conda env export > environment.yml
```

### Jupytext

This environment uses [jupytext](https://github.com/mwouts/jupytext) to pair notebooks with their equivalent in markdown files so that code is easier to check. That's why some files have duplicate names but with different extensions.
