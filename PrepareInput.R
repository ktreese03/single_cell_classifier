library(Seurat)


# Import the target Seurat dataset
target <- readRDS("P96_TargetDataset.rds")


# Log-normalize to 10,000
target <- NormalizeData(target, normalization.method = "LogNormalize", scale.factor = 10000)


# Load the stage-specific set of markers for the stage closest to the target dataset
markers <- readRDS("Adult_RNA-NNmarkers.rds")
# markers <- readRDS("P48_RNA-NNmarkers.rds")
# markers <- readRDS("P24_RNA-NNmarkers.rds")


# Determine which of the markers the target dataset contains, and which are missing
compatible.markers <- intersect(rownames(target),markers)
missing.markers <- setdiff(markers, rownames(target))


# Subset the target dataset for the compatible markers
target.markers <- as.matrix(target[["RNA"]]@data[compatible.markers,])


# Impute any missing markers with 0 
for(i in 1:length(missing.markers)){
  target.markers<-rbind(target.markers,c(rep(0,ncol(target.markers))))
  rownames(target.markers)[nrow(target.markers)]<-missing.markers[i]
}


# Ensure the order of markers match
target.markers <- target.markers[match(markers, rownames(target.markers)), ]

saveRDS(target.markers, file = "target_expressionMatrix.rds")

sessionInfo()