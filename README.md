# Hallgatói Lemorzsolódás Elemző - Streamlit App

Szakdolgozati kiegészítő alkalmazás az `elemzes.ipynb` notebookban elvégzett
elemzésre és két gépi tanulási modellre (beiratkozás előtti / 1. félév utáni
dropout-predikció) épülve.

## Gyors indítás

```bash
# 1. Függőségek telepítése
pip install -r requirements.txt

# 2. Modellek betanítása és mentése (ELSŐ HASZNÁLAT ELŐTT KÖTELEZŐ, kb. 10-20 mp)
python train_models.py

# 3. Alkalmazás indítása
streamlit run app.py
```

A böngésző automatikusan megnyílik a `http://localhost:8501` címen.

## Miért kell külön `train_models.py`-t futtatni?

Az eredeti notebookban a modellek csak a Jupyter kernel memóriájában léteztek,
sosem lettek lemezre mentve. A `train_models.py` reprodukálja pontosan
ugyanazt a pipeline-t (ugyanazok a feature-ök, ugyanaz a `random_state=42`),
és elmenti:

- `models/early_model.pkl`, `models/midterm_model.pkl` - a győztes Gradient
  Boosting modellek
- `models/scaling_params.json` - a numerikus oszlopok átlaga/szórása, hogy
  az élő űrlapon beírt új hallgatói adatok ugyanúgy legyenek skálázva, mint
  amivel a modell tanult
- `models/metrics.json` - minden modell (LR / RF / GB) Accuracy, F1-score
  és konfúziós mátrixa, ez táplálja a "Modell információ" oldalt

Ha módosítod a `student_data.csv`-t vagy a `config.py`-ban a feature
listákat, futtasd újra a `train_models.py`-t.

## Projektstruktúra

```
dropout_app/
├── app.py                        # Főoldal / navigáció
├── config.py                     # Feature listák, kód → magyar címke szótárak
├── train_models.py               # Modellek betanítása és mentése
├── requirements.txt
├── data/
│   └── student_data.csv
├── models/                       # train_models.py generálja
├── modules/
│   ├── data_processing.py        # Adatbetöltés + feature engineering
│   ├── predictor.py              # Modell betöltés + predikció (helyes skálázással)
│   └── charts.py                 # Újrafelhasználható Plotly ábrák
└── pages/
    ├── 1_📊_Leiro_statisztikak.py
    ├── 2_🎯_Dropout_elorejelzes.py
    └── 3_🤖_Modell_informacio.py
```
