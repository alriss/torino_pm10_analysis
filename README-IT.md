
![](img/turin_skyline.jpg)  
*Immagine di [Fabio Fistarol](https://unsplash.com/it/@fabiofistarol?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) su [Unsplash](https://unsplash.com/it/foto/veduta-aerea-degli-edifici-della-citta-durante-il-giorno-VjA_PSSsOHI?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)*  

# Analisi dell'Inquinamento Atmosferico: PM10 a Torino (2024)  
![GitHub pull requests](https://img.shields.io/github/issues-pr/alriss/torino_pm10_analysis)
![GitHub](https://img.shields.io/github/license/alriss/torino_pm10_analysis)
![contributors](https://img.shields.io/github/contributors/alriss/torino_pm10_analysis)
![codesize](https://img.shields.io/github/languages/code-size/alriss/torino_pm10_analysis)

[English](README.md)  

Questo progetto ha l'obiettivo di visualizzare efficacemente i livelli giornalieri di PM10 a Torino nel 2024. I dati sono analizzati in relazione alle precipitazioni e all'uso degli impianti di riscaldamento. Sono stati inoltre condotti test statistici per valutare l'impatto di questi fattori sull'inquinamento atmosferico.  

## Indice  

- [Struttura del Repository](#struttura-del-repository)  
- [Installazione e Configurazione](#installazione-e-configurazione)  
   - [Risorse Utilizzate](#risorse-utilizzate)  
   - [Librerie Python](#librerie-python)  
- [Dati](#dati)  
- [Analisi e Risultati](#analisi-e-risultati)  
   - [Pulizia dei Dati](#pulizia-dei-dati)  
   - [Visualizzazione dei Dati](#visualizzazione-dei-dati)  
   - [Analisi](#analisi)  
   - [Risultati](#risultati)  
- [Sviluppi Futuri](#sviluppi-futuri)  
- [Licenza](#licenza)  

## Struttura del Repository  

La struttura del repository è la seguente:  

```bash
│── data/                                       # Cartella contenente file CSV
│   │── Torino_Lingotto_PM10_2024.csv           # Dati PM10 
│   │── Torino_Vallere_precipitazioni_2024.csv  # Dati sulle precipitazioni
│   └── Torino_Vallere_temperature_2024.csv     # Dati sulle temperature
│── src/                                        # Contiene script Python
│   │── main.py                                 # Script principale
│   │── utils.py                                # Funzioni utili (es. caricamento e pulizia dati)
│   │── visualization.py                        # Funzioni per la creazione di grafici
│   └── statistical_tests.py                    # Funzioni per test statistici e modelli
│── img/                                        # Immagini
│── .gitignore                                  # File da ignorare
│── LICENSE                                     # Licenza MIT
│── output.log                                  # File di log
│── requirements.txt                            # Dipendenze Python
│── README.md                                   # Documentazione del progetto
└── README-IT.md                                # Documentazione del progetto in italiano
```

## Installazione e Configurazione  

1. Clona il repository:  
   ```bash
   git clone https://github.com/alriss/torino_pm10_analysis.git
   cd torino_pm10_analysis
   ```  
2. Installa le dipendenze:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Esegui lo script principale:  
   ```bash
   python src/main.py
   ```  

### Risorse Utilizzate  

Software:  
- **Editor:** Visual Studio Code  
- **Python:** Python 3.13.1  

### Librerie Python  

Le librerie necessarie sono elencate in `requirements.txt` e possono essere suddivise in:  
- **Manipolazione dati:** `pandas, numpy`  
- **Visualizzazione dati:** `matplotlib, missingno`  
- **Analisi dei dati:** `statsmodels, scipy`  

## Dati  

- **Torino_Lingotto_PM10_2024.csv:** Livelli giornalieri di PM10 misurati con metodo gravimetrico presso la stazione [Torino - Lingotto](https://webgis.arpa.piemonte.it/secure_apps/qualita_aria/dati_anagrafici/index.php?NUMCODICE=001272-806) (fonte: [ARPA](https://aria.ambiente.piemonte.it/qualita-aria/dati)).  

- **Torino_Vallere_precipitazioni_2024.csv:** Altezza giornaliera delle precipitazioni dalla stazione Torino - Vallere (fonte: [ARPA](https://www.arpa.piemonte.it/rischi_naturali/snippets_arpa_graphs/dati_giornalieri_meteo/?statid=PIE-001272-904-2001-05-17&param=P)). Per maggiori dettagli, consulta questa [guida](https://www.arpa.piemonte.it/rischi_naturali/document/Guida_alla_lettura_dati_meteo_-_Banca_Dati_Storica.pdf).  

- **Torino_Vallere_temperature_2024.csv:** Temperatura giornaliera registrata dalla stazione Torino - Vallere (fonte: [ARPA](https://www.arpa.piemonte.it/rischi_naturali/snippets_arpa_graphs/dati_giornalieri_meteo/?statid=PIE-001272-904-2001-05-17&param=T)).  

## **Analisi e Risultati**  

### **Pulizia dei Dati**  
Prima di procedere con l'analisi, i dati sono stati elaborati per garantirne completezza e affidabilità.

1. **Gestione dei valori mancanti:**  
   - I valori nulli di PM10 sono stati visualizzati con `missingno` per conoscerne frequenza e distribuzione.  
   - Questi valori sono stati sostituiti con misurazioni PM10 beta, che sono meno accurate ma forniscono un'approssimazione utile.
   - Per le analisi statistiche che richiedevano un dataset completo, sono stati applicati interpolazione lineare e backfilling.  

2. **Allineamento dei dataset:**  
   - I dataset sono stati uniti in base ai timestamp per garantire coerenza.  

3. **Pre-elaborazione dei dati:**  
   - **PM10:** Filtrato per `Id Parametro='PM10_GBV'`.  
   - **Precipitazioni:** `Precipitazione (mm)` è stata convertita in una variabile binaria (0 = nessuna pioggia, 1 = pioggia).  
   - **Temperature:** `Temperatura minima` è stata convertita in una variabile binaria (0 = sopra soglia, 1 = sotto soglia). LA soglia è stata impostata arbitrariamente a 6 °C ma può essere modificata nello script.  

#### **Visualizzazione dei Dati**  
Per comprendere l'andamento dei livelli di PM10 e la loro relazione con le precipitazioni e la temperatura, sono state generate delle visualizzazioni:

1. **Serie temporale PM10:** 
   - Livello di PM10 nel tempo, con annotazioni per le piogge e la temperatura minima sotto la soglia.  
   - Sono stati utilizzati diversi marker per distinguere tra i valori misurati, i valori beta imputati e i livelli che superano i limiti legali. 

![](img/pm10_torino_beta.png)  

2. **Analisi dei valori mancanti:**  
   - Dalle matrici dei valori mancanti e daii grafici a barre si è visto che le misurazioni di PM10 presentavano alcune lacune, successivamente colmate tramite sostituzione con valori beta e interpolazione.

3. **Analisi della correlazione incrociata:**  
   - Studio della correlazione tra PM10 e fattori esterni (precipitazioni e temperatura) per studiare il loro impatto sui livelli di PM10 nel tempo.  

#### **Analisi**  
L'analisi si è concentrata sul determinare le correlazioni, le relazioni causali e l'impatto dei fattori esterni sui livelli di PM10.

1. **Analisi della Correlazione di Spearman:**  
   - **PM10 vs Precipitazioni:** È stata osservata una correlazione negativa di Spearman **(rho = -0.383, p-value < 0.0001)**. Questo suggerisce che le precipitazioni giochino un ruolo nella riduzione dei livelli di PM10, probabilmente a causa dell'effetto washout.  
   - **PM10 vs Temperatura:** È stata trovata una correlazione positiva **(rho = 0.504, p-value < 0.0001)**, indicando che temperature più basse sono associate a concentrazioni più alte di PM10. Questo risultato è atteso, poiché temperature più basse generalmente indicano un maggiore utilizzo dei sistemi di riscaldamento.

2. **Analisi di Regressione Multivariata:**  
   - È stato costruito un modello di regressione lineare multipla per quantificare l'impatto delle precipitazioni e della temperatura sui livelli di PM10.  
   - L'equazione del modello è:  
     \[
     PM10 = \beta_0 + \beta_1 \times \text{Precipitazioni} + \beta_2 \times \text{Temperatura}
     \]
   - **Risultati:**  
     - R² = **0.399**, indicando che circa il 40% della varianza nei livelli di PM10 può essere spiegata da precipitazioni e temperatura.  
     - Entrambi i predittori sono risultati statisticamente significativi (p < 0.001).  
     - Il coefficiente negativo per le precipitazioni conferma il loro ruolo nella riduzione del PM10, mentre il coefficiente positivo per la temperatura suggerisce che l'uso dei sistemi di riscaldamento porta a concentrazioni più alte di PM10.

3. **Test di Causalità di Granger:**  
   - Questo test è stato eseguito per verificare se le precipitazioni e la temperatura potessero essere utilizzate per prevedere i valori futuri di PM10.  
   - I risultati indicano che i valori passati di entrambe le variabili migliorano la previsione dei livelli di PM10.

4. **Analisi di Correlazione Incrociata:**  
   - Questa analisi ha aiutato a identificare potenziali effetti di ritardo tra le variazioni di precipitazioni/temperatura e i cambiamenti nei livelli di PM10.  
   - I risultati suggeriscono che le precipitazioni hanno un impatto immediato sui livelli di PM10, mentre le variazioni di temperatura influenzano il PM10 in modo più graduale nel tempo.

#### **Risultati**
- **Le precipitazioni hanno un effetto mitigante sui livelli di PM10**, a supporto dell'ipotesi che la pioggia rimuova le particelle sospese nell'aria.
- **Le temperature più basse sono correlate a concentrazioni più alte di PM10**, probabilmente a causa delle emissioni derivanti dall'uso dei sistemi di riscaldamento.
- **Il modello di regressione spiega il 40% della varianza del PM10**, il che implica che altri fattori (come la velocità del vento, le emissioni del traffico o l'attività industriale) possano anche giocare un ruolo significativo.
- **I test di correlazione incrociata e di causalità di Granger suggeriscono che le precipitazioni influenzano quasi immediatamente i livelli di PM10**, mentre la temperatura ha un effetto con un certo ritardo.

Questi risultati forniscono utili informazioni sulle dinamiche dell'inquinamento atmosferico a Torino e possono aiutare nella progettazione di politiche di controllo dell'inquinamento, specialmente durante i mesi più freddi.

## Sviluppi Futuri

- **Dati sul Traffico:** Integrazione di ulteriori informazioni sul traffico per migliorare il modello e analizzare il suo impatto sull'inquinamento atmosferico.
- **Modello Previsionale:** Implementazione di un modello basato su `prophet` per prevedere i livelli di PM10 utilizzando i dati storici.
- **Previsione Giornaliera:** Sviluppo di un modello predittivo utilizzando dati su pioggia e temperatura per stimare i livelli di PM10 in tempo reale. Questo sarebbe utile per emettere avvisi rapidi, considerando che le misurazioni accurate richiedono l'analisi di laboratorio.

## Licenza  

Licenza MIT  

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