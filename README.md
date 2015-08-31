# Genemap
A python library + command line tool for mapping gene ids between different types and species. Ids are translated using Ensembl, which is accessed via the pybiomart.
## Examples

### Library

Translating human gene symbols to ensembl ids:
```{python}
map_ids(['FGFR2', 'MYH9'], from_type='symbol', cache=False))
```

Mapping human gene symbols to mouse gene symbols:
```{python}
map_homology(['FGFR2', 'MYH9'], from_org='hsapiens', to_org='mmusculus',
             to_type='symbol', from_type='symbol', cache=False))
```

### Command line tool

Mapping human gene symbols to ensembl ids:
```{bash}
genemap id --no-cache --from-type symbol FGFR2 MYH9
```

Mapping human gene symbols to mouse gene symbols:
```{bash}
genemap homology --no-cache --from-type symbol --to-type symbol --to-org mmusculus FGFR2 MYH9
```

## Dependencies
- Python 2.7 or 3.3+
- pandas
- pybiomart (<https://github.com/jrderuiter/pybiomart>)

## Installation

```{bash}
pip install git+git://github.com/jrderuiter/genemap.git#egg=genemap
```

## License
Released under the MIT license.
