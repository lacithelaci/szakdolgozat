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

## Ismert korlátok / továbbfejlesztési ötletek

- A `mother_has_degree` / `father_has_degree` szűrő a notebookból átvett
  `[2, 3, 4, 5, 40, 41, 43, 44]` kódlistát használja. Ebben a konkrét
  adathalmazban a szülői végzettség kódok csak 1-34-ig terjednek, tehát a
  `40, 41, 43, 44` kódok a gyakorlatban sosem fordulnak elő - érdemes lehet
  átnézni, hogy szeretnéd-e bővíteni a listát a 29-34 közötti (technológiai
  szakosító / felsőfokú technikusi stb.) kódokkal is.
- A `StandardScaler` a notebookban a teljes (train+test) adathalmazon lett
  illesztve a felosztás előtt - ez enyhe adatszivárgás, ami a szakdolgozat
  módszertani fejezetében érdemes megemlíteni, de a jelenlegi eredményeket
  (F1 0.69 / 0.88) nem érinti drasztikusan.
- Jelenleg a predikciós modellek csak pontbecslést adnak vissza (nincs
  konfidencia-intervallum) - ha szeretnéd, bővíthető bootstrap-alapú
  bizonytalansági sávval.
- Nincs adatperzisztencia (pl. korábbi predikciók naplózása) - ha ez kell a
  szakdolgozathoz (pl. "hány hallgatót elemeztünk eddig"), egyszerűen
  hozzáadható egy helyi SQLite vagy CSV napló.
