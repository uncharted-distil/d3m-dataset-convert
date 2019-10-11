D3M Data Convert
================

Converts tab separated input files into D3M datasets, with support for:
1. overriding column names
1. re-mapping values
1. setting column type
1. adding column descriptions

Takes a mapping file, source file and output location as input args, and produces a D3M `datasetDoc.json` and `learningData.csv` as its output.

To run:
```console
python convert.py mapping.csv source.tsv new_dataset
```
A simple mappping CSV file is used to transform the input csv data.  Example:

```
southern_state,categorical,"{'0.0':'non-south','1.0':'south'}",Southern state
borders_mexico,categorical,"{'0.0':'not border district','1.0':'border district'}",District that borders Mexico
immigration_impact,categorical,"{'0.0':'expansive bill','1.0':'restrictive bill'}",Bill impact on immigration
state_control,categorical,"{'0.0':'republican','1.0':'democratic'}",Party control of state legislature
legislator_party,categorical,"{'0':'republican','1':'democratic'}",Legislator party affiliation
```

Using the first entry above as an example:

```southern_state,categorical,"{'0.0':'non-south','1.0':'south'}",Southern state```

The first column will be renamed to `southern_state`, will be assigned a type of `categorical`, and will re-map `0.0` and `1.0` values to be `non-south` and `south`.  The description `Southern state` will be applied.


