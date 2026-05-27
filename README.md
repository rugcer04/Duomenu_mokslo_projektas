# Duomenų mokslo projektas

## Summary

Review of the literature has revealed that the concentration of particulate matter in the atmosphere influences meteorological conditions and, consequently, errors in model predictions. Aerosol particles act as condensation nuclei, contributing to the formation of cloud and ice particles. However, the main weather forecast model for European countries, the ECMWF, does not account for chemical changes in the atmosphere and can only provide a resolution of $9$ km, which is half that of local national models. Therefore, in this study, to improve the accuracy of the global model’s weather forecasts for the city of Vilnius, it combines data from a local automatic weather station and atmospheric pollution data obtained from the Sentinel--5P and MetOp--B and the Copernicus Atmosphere Monitoring Service (CAMS) European Regional Air Quality Reanalysis Ensemble. To achieve this goal, machine learning models are used, such as random forests (RF), extreme gradient boosting (XGB) algorithms, and a more complex method—singular spectrum analysis integrated with a long short-term memory (SSA-LSTM). An ensemble of these models is also tested, which is trained using the forecasts from the mentioned models, with the final forecast provided by the Extreme Gradient Boosting algorithm. The study found that individual machine learning models (evaluated over a $365$-day period): RF $(MAE=1.42,\ RMSE=3.17 \text{ mm})$ and SSA--LSTM $(MAE=1.69,\ RMSE=3.41 \text{ mm})$ did not reduce the forecast errors of ECMWF $(MAE=1.45,\ RMSE=3.15 \text{ mm})$ forecasting without pollution data, with the exception of the XGB algorithm $(MAE=1.41, RMSE=3.07 \text{ mm})$. With the addition of pollution data, the results changed significantly. All models analyzed improved the errors made by the global model: RF $(MAE=1.39,\ RMSE=2.94 \text{ mm})$, SSA--LSTM $(MAE=1.37, RMSE=2.99 \text{ mm})$, while the XGB algorithm $(MAE=1.36, RMSE=2.94 \text{ mm})$ reduced them the most. Although SSA--LSTM underestimates precipitation, it most accurately predicted non-rainy days. The ensemble was evaluated on a smaller set of $108$ days, where the ECMWF errors are: $MAE=1.14\text{ mm}$ and $RMSE=2.45\text{ mm}$. In this sample, individual machine learning algorithms did not improve the performance of the global model, but their ensemble reduced the errors to $MAE=1.09\text{ mm}$ and $RMSE=2.32\text{ mm}$. The study also found that among the most important pollution factors in precipitation forecasting are the concentration of water vapor in the atmospheric column, nitrogen dioxide ($NO_2$) measurements, the concentration of $PM_{10}$ particulate matter at a height of $500$ m, ammonia ($NH_3$), and secondary inorganic aerosols.

**Keywords:** Pollution analysis, machine learning, Random Forest, Extreme Gradient Boosting, Singular Spectrum Analysis, Long Short-Term Memory, precipitation forecast, time series

## Used Packages

### Python
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/) [![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/) [![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/) [![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/) [![XGBoost](https://img.shields.io/badge/XGBoost-black?style=flat&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/) [![LightGBM](https://img.shields.io/badge/LightGBM-blue?style=flat)](https://lightgbm.readthedocs.io/) [![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org/) [![Matplotlib](https://img.shields.io/badge/Matplotlib-ffffff?style=flat&logo=matplotlib&logoColor=black)](https://matplotlib.org/) [![Seaborn](https://img.shields.io/badge/Seaborn-444444?style=flat)](https://seaborn.pydata.org/) [![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/) [![Xarray](https://img.shields.io/badge/Xarray-blue?style=flat)](https://xarray.pydata.org/) [![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat&logo=scipy&logoColor=white)](https://scipy.org/) [![Dask](https://img.shields.io/badge/Dask-orange?style=flat&logo=dask&logoColor=white)](https://dask.org/) [![Statsmodels](https://img.shields.io/badge/Statsmodels-blue?style=flat)](https://www.statsmodels.org/) [![Pmdarima](https://img.shields.io/badge/Pmdarima-blue?style=flat)](https://alkaline-ml.com/pmdarima/) [![Cartopy](https://img.shields.io/badge/Cartopy-blue?style=flat)](https://scitools.org.uk/cartopy/) [![EUMDAC](https://img.shields.io/badge/EUMDAC-blue?style=flat)](https://eumdac.readthedocs.io/) [![Google Earth Engine](https://img.shields.io/badge/Earth--Engine-blue?style=flat&logo=google-earth)](https://earthengine.google.com/) [![Tqdm](https://img.shields.io/badge/Tqdm-blue?style=flat)](https://tqdm.github.io/)

### R
[![R](https://img.shields.io/badge/R-%23276DC3.svg?style=flat&logo=r&logoColor=white)](https://www.r-project.org/) [![Tidyverse](https://img.shields.io/badge/Tidyverse-%23276DC3.svg?style=flat&logo=r&logoColor=white)](https://www.tidyverse.org/) [![GGally](https://img.shields.io/badge/GGally-blue?style=flat)](https://ggobi.github.io/ggally/) [![Corrplot](https://img.shields.io/badge/Corrplot-blue?style=flat)](https://github.com/taiyun/corrplot) [![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/r/) [![Forecast](https://img.shields.io/badge/Forecast-blue?style=flat)](https://pkg.robjhyndman.com/forecast/) [![Zoo](https://img.shields.io/badge/Zoo-blue?style=flat)](https://cran.r-project.org/web/packages/zoo/index.html) [![Patchwork](https://img.shields.io/badge/Patchwork-blue?style=flat)](https://patchwork.data-imaginist.com/) [![funtimes](https://img.shields.io/badge/funtimes-blue?style=flat)](https://cran.r-project.org/web/packages/funtimes/index.html) [![scales](https://img.shields.io/badge/scales-blue?style=flat)](https://scales.r-lib.org/) [![here](https://img.shields.io/badge/here-blue?style=flat)](https://here.r-lib.org/)

---

## Folder Summaries

### Python Project (`code/python/`)

#### **Code Modules**
- **`ACSAF/`**: Scripts and notebooks for MetOp-B GOME-2 data retrieval and preprocessing, including MPI-based parallel processing in `MPI/`.
- **`CAMS/`**: Specialized Python scripts for downloading and preparing atmospheric data from the Copernicus Atmosphere Monitoring Service (CAMS) for various pollutants (NH3, CH4, PM10, PM2.5, etc.).
- **`datasets_prep/`**: Core data engineering notebooks for merging, cleaning, and imputing air quality, meteorological (ECMWF), and Sentinel-5P datasets.
- **`ecmwf/`**: Tools for automated retrieval of yearly and monthly meteorological data using the ECMWF API.
- **`EUMDAC/`**: Scripts for testing and interacting with EUMETSAT Data Access Client (EUMDAC) for satellite data tailoring and downloads.
- **`Models/`**: Implementation of machine learning models including Random Forest, XGBoost, SSA-LSTM, and Lasso feature selection. Contains notebooks for model training, ensemble creation, and error analysis.
- **`sentinel/`**: Automated preprocessing and location-specific (Lithuania, Ryga) retrieval scripts for Sentinel-5P data products.
- **`visuals/`**: Notebooks for generating spatial heatmaps and time-series visualizations for satellite datasets.

#### **Data & Logs**
- **Satellite Data**: HDF5 structures (`hdf5_structure.txt`), large MetOp-B CSV datasets (`METOPB_full_set.csv`), and Sentinel-5P CSVs for various regions.
- **Processed Datasets**: Final project datasets (`dm_project_dataset.csv`) and prediction outputs (`All_predictions.csv`, `RF_prediction.csv`, `xgboost_pred.csv`).
- **Models & Logs**: Serialized PyTorch models (`params.pt`, `optimizer.pt`), training history (`history.json`), and detailed HPC/MPI execution logs (`.log`).

### R Project (`code/R/`)

#### **Code Modules**
- **`EDA/`**: Comprehensive Exploratory Data Analysis notebooks and RMarkdown files focusing on dependency analysis, outlier detection, and seasonality/tendency studies.



---

With Gemini CLI c0.34.0 (Model: Gemini 3, 2026-03-19 version), Wednesday, May 27, 2026.