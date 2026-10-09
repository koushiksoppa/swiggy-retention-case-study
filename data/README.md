# Data

The retention analysis uses the **UCI Online Retail dataset**: every transaction of a UK-based online retailer
between 1 December 2010 and 9 December 2011 (541,909 invoice lines).

Citation: Chen, D., Sain, S. L., & Guo, K. (2012). Data mining for the online retail industry: A case study of
RFM model-based customer segmentation using data mining. *Journal of Database Marketing and Customer Strategy
Management*, 19(3), 197–208. Licensed CC BY 4.0 by the UCI Machine Learning Repository.

The raw file is not committed. Download **either** format into `data/raw/`:

1. **Excel (UCI):** download from <https://archive.ics.uci.edu/dataset/352/online+retail> and save as
   `data/raw/Online Retail.xlsx`.
2. **R data file:** `data/onlineretail.rda` from the CRAN package source
   <https://github.com/allanvc/onlineretail>, saved as `data/raw/onlineretail.rda` (read with `pyreadr`).

Then run `python analysis/cohort_retention.py`. Its outputs are committed in `analysis/outputs/` and `charts/`.

## Why this dataset

Swiggy does not publish customer-level order data. This dataset is real, public and widely used for retention
analysis, so it can test the *pattern* behind the case study's argument: how repeat behaviour builds with each
order and how the speed of the second order relates to later loyalty. It is a gift-ware retailer with many
business customers, not a food-delivery platform, so its retention **levels** do not transfer to Swiggy.
