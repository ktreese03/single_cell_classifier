# single_cell_classifier

## 1. Requirements

The following Python/R packages and their dependencies are required for this analysis: 
  - numpy (version >= 2.2.4, < 3) for numerical operations.
  - keras (version >= 3.9.0, < 4) for building and loading deep learning models
  - matplotlib (version >= 3.10.1, < 4) for data visualization, pandas (version 1.3.4) for data manipulation.
  - pyreadr (version >= 0.5.3, < 0.6) for reading R data files.
  - scikit-learn (version 1.5.0) for machine learning utilities.
  - joblib (version >= 1.4.2, < 2) for model saving and loading.
  - pandas (version >= 2.2.3, < 3)
  - Seurat (version 4.3.0) and SeuratObject (version 4.1.3) are recommended for normalizing input data, particularly if you are working with single-cell RNA sequencing datasets.

All required files are provided with the appendix.
The pixi.toml file outlines the Python package requirements for recreating the necessary Python environment. 

## 2. Gene Names

We provide lists of marker genes to be used as input features for different stages as .rds files. We use the gene symbols from the BDGP6.88 build. If your genes names are from a different build, or if you use FBgn numbers instead, you can convert the marker gene lists using the "ConversionTable.rds" object we also provide. The first column, "reference_symbol" is what we use, the last two columns correspond to up-to-date FBgn numbers/symbols. However, these are not guaranteed to match your datasets either.

## 3. Stage

You can classify optic lobe cells sequenced from any stage, but you need to use the correct set of markers as input features and uncomment the correct stage of model and means lines in the Predict.py file We recommend using the stage closest to your target dataset. For example:

For P15 and P30 stages, use P24.
For P40, P50 and P70 stages, use P48.
For late pupal stages (after P70) use Adult.


## Classifying your Drosophila optic lobe dataset
### Step 1. Preparation of the input: PrepareInput.R

Because the classification script (Predict.py) requires a subsetted, log-normalized expression matrix, we've provided the PrepareInput.R script that can be ran on a Seurat object by simply loading the correct stage-specific markers and your dataset. It is included in the script to ensure the gene names in the marker list and your dataset match, as this is necessary for our model. **Do NOT modify the order of the marker genes**. If a marker gene is not captured in your dataset, it's also included in the script to add the marker gene to the generated expression file and pad it with zeroes.

### Step 2. Classification: Predict.py

First, ensure the correct input objects are uncommented relative to your dataset. This script is designed to load a matrix saved in .rds format, as outputted from PrepareInput.R. However, you can load your input dataset in any way you like (if you're not loading an R file, you don't need the pyreadr package), as long as the dataset structure matches expected input. As explained, be sure it's log-normalized in the same way and the columns (input features) are in the exact same order as in the provided marker files provided. This script will then classify your data, determine confidence scores and save them in .txt files. The .txt file will contain two columns, in the first one labelled "Cluster" you will have the cluster identity you are predicting and in the second column, named "Confidence", you will have the confidence score with which the cluster has been predicted. **The rows are labeled, but the order will match the order of cells you provided**. Please refer to Table S1 for correspondances of the predicted cluster numbers to cell types.

The function generates 500 predictions (with dropout) per cell for determining confidence scores. These are calculated for all cells simultenously to maximize parallelization in GPU-equipped machines. But it can also require significant amount of RAM for larger datasets. If this is an issue, you can use the alternative function provided below, which will be slower but should reduce the maximum RAM required five-fold.

This script can also be ran using the pixi.toml file, which makes recreating the Python environment easier: \n
      * ml pixi \n
      * git clone https://github.com/ktreese03/single_cell_classifier \n
      * cd single_cell_classifer \n
      * pixi install \n 
      * Rscript PrepareInput.R (if necessary) \n
      * pixi run python Predict.py \n
