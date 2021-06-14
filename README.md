# TREC-Clinical-Workshop


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
