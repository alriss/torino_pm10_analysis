![](img/turin_skyline.jpg)
*Picture by [Fabio Fistarol](https://unsplash.com/it/@fabiofistarol?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/it/foto/veduta-aerea-degli-edifici-della-citta-durante-il-giorno-VjA_PSSsOHI?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)*

# Air Pollution Analysis: PM10 in Turin (2024)
![GitHub pull requests](https://img.shields.io/github/issues-pr/alriss/torino_pm10_analysis)
![GitHub](https://img.shields.io/github/license/alriss/torino_pm10_analysis)
![contributors](https://img.shields.io/github/contributors/alriss/torino_pm10_analysis)
![codesize](https://img.shields.io/github/languages/code-size/alriss/torino_pm10_analysis)

[Italiano](README-IT.md)

This project aims to effectively visualize the daily PM10 levels in Turin in 2024. Data is analyzed in relation to precipitation and heating system usage. Statistical tests have also been conducted to evaluate the impact of these factors on air pollution.

## Table of Contents

- [Repository Structure](#repository-structure)
- [Installation and Setup](#installation-and-setup)
   - [Resources Used](#resources-used)
   - [Python Libraries](#python-libraries)
- [Data](#data)
- [Analysis and Results](#analysis-and-results)
   - [Data Cleaning](#data-cleaning)
   - [Data Visualization](#data-visualization)
   - [Analysis](#analysis)
   - [Results](#results)
- [Future Developments](#future-developments)
- [License](#license)

## Repository Structure
The repository structure is as follows:

```bash
│── data/                                       # Folder containing CSV files
│   │── Torino_Lingotto_PM10_2024.csv           # PM10 data 
│   │── Torino_Vallere_precipitazioni_2024.csv  # Rainfall data
│   │── Torino_Vallere_temperature_2024.csv     # Temperature data
│── src/                                        # Contains Python scripts
│   │── main.py                                 # Main script
│   │── utils.py                                # Useful functions (e.g., data loading and cleaning)
│   │── visualization.py                        # Functions for creating charts
│   │── statistical_tests.py                    # Functions for statistical tests and models
│── img/                                        # Images
│── .gitignore                                  # List of files to ignorepip              
│── LICENSE                                     # MIT License
│── output.log                                  # Log file
│── requirements.txt                            # Python dependencies
│── README.md                                   # Project documentation
│── README-IT.md                                # Project documentation in Italian
```

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/alriss/torino_pm10_analysis.git
   cd torino_pm10_analysis
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```bash
   python src/main.py
   ```

### Resources Used
Software Information:
- **Editor:** Visual Studio Code
- **Python:** Python 3.13.1

### Python Libraries
The required libraries are listed in the `requirements.txt` file. They can be categorized as follows:
- **Data Manipulation:** `pandas, numpy`
- **Data Visualization:** `matplotlib`,`missingno`
- **Data Analysis:** `statsmodels, scipy`

## Data

- **Torino_Lingotto_PM10_2024.csv:** Daily PM10 levels measured using the gravimetric method from the [Torino - Lingotto](https://webgis.arpa.piemonte.it/secure_apps/qualita_aria/dati_anagrafici/index.php?NUMCODICE=001272-806) station (source: [ARPA](https://aria.ambiente.piemonte.it/qualita-aria/dati)).

- **Torino_Vallere_precipitazioni_2024.csv:** Daily rainfall height from the Torino - Vallere station (source: [ARPA](https://www.arpa.piemonte.it/rischi_naturali/snippets_arpa_graphs/dati_giornalieri_meteo/?statid=PIE-001272-904-2001-05-17&param=P)). This [guide](https://www.arpa.piemonte.it/rischi_naturali/document/Guida_alla_lettura_dati_meteo_-_Banca_Dati_Storica.pdf) provides additional information.

- **Torino_Vallere_temperature_2024.csv:** Daily temperature recorded by the Torino - Vallere station (source: [ARPA](https://www.arpa.piemonte.it/rischi_naturali/snippets_arpa_graphs/dati_giornalieri_meteo/?statid=PIE-001272-904-2001-05-17&param=T)). This [guide](https://www.arpa.piemonte.it/rischi_naturali/document/Guida_alla_lettura_dati_meteo_-_Banca_Dati_Storica.pdf) provides additional information.

## **Analysis and Results**

### **Data Cleaning**
Before performing any statistical analysis, data preprocessing steps were undertaken to ensure completeness and reliability.

1. **Handling Missing Values:**  
   - Missing PM10 values were visualized using `missingno` to assess their frequency and distribution.
   - These missing values were replaced with corresponding PM10 beta measurements, which are less accurate but provide useful approximations.
   - For statistical tests requiring complete datasets, linear interpolation and backfilling were applied to further fill missing PM10 values.

2. **Dataset Alignment:**  
   - The datasets were merged based on timestamps to ensure alignment.

3. **Data Preprocessing**
   - **PM10:** Filtered for `Id Parametro='PM10_GBV'`.  
   - **Precipitation:** `Precipitazione (mm)` was converted into a binary variable (0 = no rain, 1 = rain).  
   - **Temperature:** `Temperatura minima` was converted into a binary variable (0 = above threshold, 1 = below threshold). The threshold was arbitrarily set to 6°C but can be adjusted in the script.

#### **Data Visualization**
To understand the trends in PM10 levels and their relationship with precipitation and temperature, visualizations were generated:

1. **Time Series of PM10 Levels:**  
   - PM10 levels over time, with event plot for the rainfall and temperature below threshold.
   - Different markers were used to distinguish between measured values, imputed beta values, and legally exceeding levels.

![](img/pm10_torino_beta.png)

2. **Missing Value Analysis:**  
   - Missing value matrices and bar plots revealed that PM10 measurements had some gaps, later addressed through beta substitution and interpolation.

3. **Cross-Correlation Visualizations:**  
   - The cross-correlation between PM10 and external factors (precipitation, temperature) was plotted to analyze potential time delays in their impact.

#### **Analysis**
The analysis focused on determining correlations, causal relationships, and the impact of external factors on PM10 levels.

1. **Spearman Correlation Analysis:**  
   - **PM10 vs Precipitation:** A negative Spearman correlation coefficient **(rho = -0.383, p-value < 0.0001)** was observed. This suggests that precipitation plays a role in reducing PM10 levels, likely due to the washout effect.  
   - **PM10 vs Temperature:** A positive correlation **(rho = 0.504, p-value < 0.0001)** was found, indicating that lower temperatures are associated with higher PM10 concentrations. This outcome is expected, as lower temperatures typically indicate increased use of heating systems.

2. **Multivariate Regression Analysis:**  
   - A multiple linear regression model was built to quantify the impact of precipitation and temperature on PM10 levels.
   - The model equation was:  
     \[
     PM10 = \beta_0 + \beta_1 \times \text{Precipitation} + \beta_2 \times \text{Temperature}
     \]
   - **Results:**  
     - R² = **0.399**, indicating that about 40% of the variance in PM10 can be explained by precipitation and temperature.
     - Both predictors were statistically significant (p < 0.001).
     - The negative coefficient for precipitation confirms its role in reducing PM10, while the positive coefficient for temperature suggests that usage of heating systems leads to higher PM10 concentrations.

3. **Granger Causality Test:**  
   - This test was performed to check whether precipitation and temperature could be used to predict future PM10 values.
   - The results indicate that past values of both variables improve the prediction of PM10 levels.

4. **Cross-Correlation Analysis:**  
   - This analysis helped to identify potential lag effects between precipitation/temperature and PM10 changes.
   - The results suggest that precipitation has an immediate impact on PM10 levels, whereas temperature variations influence PM10 more gradually over time.

#### **Results**
- **Precipitation has a mitigating effect on PM10 levels**, supporting the hypothesis that rainfall removes particulate matter from the air.
- **Lower temperatures are linked to higher PM10 concentrations**, possibly due to increased heating emissions.
- **The regression model explains 40% of the variance in PM10**, meaning other factors (such as wind speed, traffic emissions, or industrial activity) may also play a significant role.
- **Cross-correlation and Granger causality tests suggest that precipitation affects PM10 levels almost immediately**, while temperature influences PM10 with some lag.

These findings provide useful insights into air pollution dynamics in Torino and can help in designing policies for pollution control, especially during colder months.

## Future Developments

- **Traffic Data:** Incorporating additional traffic information to enhance the model and analyze its impact on air pollution.
- **Forecasting Model:** Implementation of a `prophet`-based model to predict PM10 levels using historical data.
- **Daily Prediction:** Development of a predictive model using rain and temperature data to estimate real-time PM10 levels. This would be useful for issuing rapid alerts, considering that official measurements require laboratory analysis.

## License
MIT License

Copyright (c) 2025 Alberto Rissone

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.