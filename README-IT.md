![](img/turin_skyline.jpg)
*Foto di [Fabio Fistarol](https://unsplash.com/it/@fabiofistarol?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) su [Unsplash](https://unsplash.com/it/foto/veduta-aerea-degli-edifici-della-citta-durante-il-giorno-VjA_PSSsOHI?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)*

# Analisi dell'inquinamento atmosferico: PM10 a Torino (2024)
![GitHub last commit](https://img.shields.io/github/last-commit/alriss/torino_pm10_analysis)
![GitHub pull requests](https://img.shields.io/github/issues-pr/alriss/torino_pm10_analysis)
![GitHub](https://img.shields.io/github/license/alriss/torino_pm10_analysis)
![contributors](https://img.shields.io/github/contributors/alriss/torino_pm10_analysis) 
![codesize](https://img.shields.io/github/languages/code-size/alriss/torino_pm10_analysis) 

Questo progetto ha l'obiettivo di visualizzare in modo efficace i livelli giornalieri di PM10 a Torino nel 2024. I dati sono analizzati in relazione alle precipitazioni e all'uso degli impianti di riscaldamento. Sono stati inoltre effettuati test statistici per valutare l'impatto di questi fattori sull'inquinamento atmosferico.

## Indice

- [Struttura della repository](#struttura-della-repository)
- [Installazione e setup](#installazione-e-setup)
   - [Risorse utilizzate](#risorse-utilizzate)
   - [Librerie Python](#librerie-python)
- [Dati](#dati)
- [Analisi e risultati](#analisi-e-risultati)
   - [Pulizia dei dati](#pulizia-dei-dati)
   - [Visualizzazione dei dati](#visualizzazione-dei-dati)
   - [Analisi](#analisi)
   - [Risultati](#risultati)
- [Sviluppi futuri](#sviluppi-futuri)
- [Licenza](#licenza)

## Struttura della repository
La struttura della repository è la seguente:

```bash
│── data/                                       # Cartella con i file CSV
│── src/                                        # Contiene gli script Python
│   │── main.py                                 # Script principale
│   │── utils.py                                # Funzioni utili (es. caricamento e pulizia dei dati)
│   │── visualization.py                        # Funzioni per la creazione dei grafici
│   │── statistical_tests.py                    # Funzioni per test statistici e modelli
│── img/                                        # Immagini
│   │── cross_correlation_chart_Pioggia.pdf                
│   │── cross_correlation_chart_Pioggia.png                
│   │── cross_correlation_chart_Temperatura.pdf            
│   │── cross_correlation_chart_Temperatura.png            
│   │── pm10_torino.pdf                
│   │── pm10_torino.png                
│── requirements.txt                            # Dipendenze Python
│── README.md                                   # Documentazione del progetto
│── .gitignore                 
```

## Installazione e setup
1. Clona la repository:
   ```bash
   git clone https://github.com/alriss/torino_pm10_analysis.git
   cd torino_pm10_analysis
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
3. Esegui lo script principale:
   ```bash
   python src/main.py
 
### Risorse utilizzate
Informazioni sui software:
- **Editor:**  Visual Studio Code
- **Python:** Python 3.13.1

### Librerie Python
Le librerie necessarie sono elencate nel file `requirements.txt`. Si possono suddividere in:
- **Manipolazione dei dati:** `pandas, numpy`
- **Visualizzazione dei dati:** `matplotlib`
- **Analisi dei dati:** `statsmodels, scipy`

## Dati

- **Torino_Lingotto_PM10_2024.csv:**: Livelli giornalieri di PM10 misurati con metodo gravimetrico dalla stazione [Torino - Lingotto](https://webgis.arpa.piemonte.it/secure_apps/qualita_aria/dati_anagrafici/index.php?NUMCODICE=001272-806) (fonte: [ARPA](https://aria.ambiente.piemonte.it/qualita-aria/dati)).

- **Torino_Vallere_precipitazioni_2024.csv:** Altezza della pioggia caduta giornalmente dalla stazione Torino - Vallere (fonte: [ARPA](https://www.arpa.piemonte.it/rischi_naturali/snippets_arpa_graphs/dati_giornalieri_meteo/?statid=PIE-001272-904-2001-05-17&param=P)). Questa [guida](https://www.arpa.piemonte.it/rischi_naturali/document/Guida_alla_lettura_dati_meteo_-_Banca_Dati_Storica.pdf) fornisce informazioni aggiuntive.

- **Torino_Vallere_temperature_2024.csv:** Temperatura giornaliera registrata dalla stazione Torino - Vallere (fonte: [ARPA](https://www.arpa.piemonte.it/rischi_naturali/snippets_arpa_graphs/dati_giornalieri_meteo/?statid=PIE-001272-904-2001-05-17&param=T)). Questa [guida](https://www.arpa.piemonte.it/rischi_naturali/document/Guida_alla_lettura_dati_meteo_-_Banca_Dati_Storica.pdf) fornisce informazioni aggiuntive.

### Data Preprocessing
- **PM10:** Il dataset è stato filtrato per `Id Parametro='PM10_GBV'` in modo da tenere solo le misurazioni ottenute con metodo gravimetrico. Le colonne utilizzate sono `Data rilevamento` e `Valore`.
- **Precipitazioni:** Le colonne utilizzate sono `DATA` e `Precipitazione (mm)`. Per le analisi la misura `Precipitazione (mm)` è stata trasformata in un flag in modo da creare una nuova feature: la nuova colonna presenta il valore 1 se la misura è > 0 altrimenti 0, in questo modo si distinguono i giorni in cui ha piovuto, a prescindere dalla quantità di pioggia, da quelli in cui non ha piovuto.
- **Temperatura:** Le colonne utilizzate sono `DATA` e `Temperatura minima`. Per le analisi la misura `Temperatura minima` è stata trasformata in un flag in modo da creare una nuova feature: la nuova colonna presenta il valore 1 se la misura è <`temp_thr` (soglia arbitrariamente impostata a 6 modificabile nello script) altrimenti 0, in questo modo si distinguono i giorni in cui la temperatura minima è scesa al di sotto della soglia, a prescindere dalla temperatura raggiunta, da quelli in cui ciò non è accaduto.

## Analisi e risultati

### Pulizia dei dati
- Rimozione dei valori nulli e gestione delle anomalie.

<div style="display: flex; justify-content: space-around;">
   <img src="img/nullvalues_matrix.png" alt="Null Values Matrix" style="width: 45%;">
   <img src="img/nullvalues_bars.png" alt="Null Values Bars" style="width: 45%;">
</div>

- Conversione delle colonne temporali in formato datetime per una migliore manipolazione.
- Creazione di nuove feature binarie per precipitazioni (>0 mm) e presunto utilizzo del riscaldamento (temperatura minima<6°C), utili per le analisi successive.

### Visualizzazione dei dati
- Grafico a linee per evidenziare l'andamento dei livelli di PM10 nel tempo.
- Aggiunta di event plot per visualizzare la distribuzione di precipitazioni e temperatura minima sotto la soglia scelta.
- Lollipop plot per visualizzare la correlazione tra le variabili per diversi valori di lag (sfasamento temporale).

![](img/pm10_torino_beta.png)

### Analisi
- **Regressione lineare** per stimare l'impatto delle precipitazioni e della temperatura sui livelli di PM10.
- **Analisi di correlazione**:
  - Test di Spearman per valutare la relazione diretta tra variabili (lag = 0).
  - Cross-correlation function (CCF) per verificare effetti ritardati (lag > 0).
  - Test di Granger per determinare causalità temporale tra temperatura, pioggia e PM10.

### Risultati
- **Effetto combinato:** L'analisi suggerisce che la combinazione di basse temperature e assenza di precipitazioni aumenta significativamente i livelli di PM10.
- **Effetti della pioggia:** Nei giorni di pioggia si osserva una riduzione media della concentrazione di PM10.
- **Effetti del riscaldamento:** I giorni con temperatura minima inferiore a 6°C mostrano una tendenza all'aumento dell'inquinamento atmosferico.

## Sviluppi futuri

- **Modello di previsione:** Implementazione di un modello basato su `prophet` per prevedere i livelli di PM10 sfruttando i dati storici.
- **Predizione giornaliera:** Sviluppo di un modello predittivo che utilizzi i dati di pioggia e temperatura per stimare i livelli di PM10 in tempo reale, utile per fornire allerte rapide considerando che le misurazioni ufficiali richiedono analisi di laboratorio.

## Licenza
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
