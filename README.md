# single_cell_classifier

## 1. Requirements

The following Python packages and their dependencies are required for this analysis: numpy (version 1.21.0) for numerical operations, tensorflow (version 2.7.0) and keras (version 2.7.0) for building and loading deep learning models, matplotlib (version 3.5.1) for data visualization, pandas (version 1.3.4) for data manipulation, pyreadr (version 0.4.0) for reading R data files, scikit-learn (version 1.0.1) for machine learning utilities, and joblib (version 1.1.0) for model saving and loading. Additionally, the R package Seurat is recommended for normalizing input data, particularly if you are working with single-cell RNA sequencing datasets.

All required files, as well as an example input dataset are provided with the appendix

## 2. Gene Names

We provide lists of marker genes to be used as input features for different stages as .rds files. We use the gene symbols from BDGP6.88 build. If your genes names are from a different build, or if you use FBgn numbers instead, you can convert the marker gene lists using the "ConversionTable.rds" we also provide. The first column, "reference_symbol" is what we use, the last two columns correspond to, up-to-date, FBgn numbers or symbols. However, these are not guaranteed to match your datasets either

## 3. Stage

You can classify optic lobe cells sequenced from any stage, but you need to use the correct set of markers as input features and uncomment the correct stage of model and means lines in the Predict.py file We recommend using the stage closest to your target dataset.

For P15 and P30 sequencing stage P24 was used

For P40, P50 and P70 stage P48 was used

For late larval stages (after P70) use Adult stage

## 4. Preparation of the input

The classification script (Predict.py) requires a log-normalized expression matrix, subsetted for the marker genes provided. If your data is in Seurat format, you can use the included "PrepareInput.R" script to do this. Just uncomment the marker load line for the correct stage. Make sure the gene names in the marker list and your dataset match. Do NOT modify in any way the order of the marker genes. If your cells are missing any of the genes, you need to create that row in your dataset and pad it with zeros BEFORE subsetting with the provided files

## 5. Classification

Uncomment the lines loading the "model" and "mean" for the correct stage in the Predictionscript.py file. This script is designed to load a matrix saved in .rds format as exampled in PrepareInput.R. However, you can load your input dataset in any way you like (if you're not loading an R file, you don't need the pyreadr package), as long as the format matches the example dataset provided. Make sure it's log-normalized in the same way and the columns (input features) are in the exact same order as in the provided marker files provided. The script will then classify your data, determine confidence scores and save them in .txt files. The .txt file will contain two columns, in the first one labelled "Cluster" you will have the number of cluster you are predicting and in the second column named "Confidence" you will have the confidence score with which the cluster has been predicted. The rows will not be labeled but order will match the order of cells you provided. Please refer to Table S1 for correspondances of the predicted cluster numbers to cell types.

The function generates 500 predictions (with dropout) per cell for determining confidence scores. These are calculated for all cells simultenously to maximize parallelization in GPU-equipped machines. But it can also require significant amount of RAM for larger datasets. If this is an issue, you can use the alternative function provided below, which will be slower but should reduce the maximum RAM required five-fold.
