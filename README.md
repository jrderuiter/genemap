# Genemap
A python library + command line tool for mapping gene ids between different types and species. Ids are translated using Ensembl, which is accessed via the pybiomart.
## Examples

### Library

Translating human gene symbols to ensembl ids:
```{python}
map_ids(['FGFR2', 'MYH9'], from_type='symbol', to_type='ensembl', cache=False))
```

### Command line tool

## Dependencies
- Python 2.7, 3.3+
- future
- pandas
- pybiomart (<https://github.com/jrderuiter/pybiomart>)

## Installation

```{bash}
# Install genemap.
pip install git+git://github.com/jrderuiter/genemap.git#egg=genemap
```

## License
Released under the MIT license.
