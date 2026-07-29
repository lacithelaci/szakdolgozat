"""
Konfigurációs modul a modellhez és a Streamlit alkalmazáshoz.

Tartalmazza:
- kód -> címke megfeleltetéseket
- modell feature listákat
- skálázási oszlopokat
- fájlútvonalakat
"""

# Szakok
COURSE_LABELS = {
    1: "Biofuel Production Technologies",
    2: "Animation and Multimedia Design",
    3: "Social Service (evening attendance)",
    4: "Agronomy",
    5: "Communication Design",
    6: "Veterinary Nursing",
    7: "Informatics Engineering",
    8: "Equinculture",
    9: "Management",
    10: "Social Service",
    11: "Tourism",
    12: "Nursing",
    13: "Oral Hygiene",
    14: "Advertising and Marketing Management",
    15: "Journalism and Communication",
    16: "Basic Education",
    17: "Management (evening attendance)",
}

# Családi állapot
MARITAL_STATUS_LABELS = {
    1: "Egyedülálló",
    2: "Házas",
    3: "Özvegy",
    4: "Elvált",
    5: "Élettársi kapcsolat",
    6: "Külön élő (jogilag)",
}

# Jelentkezési módok
APPLICATION_MODE_LABELS = {
    1: "1. fázis - általános kontingens",
    2: "612/93 rendelet",
    3: "1. fázis - speciális kontingens (Azori-szigetek)",
    4: "Más felsőfokú végzettséggel rendelkezők",
    5: "854-B/99 rendelet",
    6: "Nemzetközi hallgató (alapképzés)",
    7: "1. fázis - speciális kontingens (Madeira)",
    8: "2. fázis - általános kontingens",
    9: "3. fázis - általános kontingens",
    10: "533-A/99 rendelet, b2) pont (más terv)",
    11: "533-A/99 rendelet, b3) pont (más intézmény)",
    12: "23 év felettiek",
    13: "Átvétel (transfer)",
    14: "Szakváltás",
    15: "Technológiai szakosító diplomával rendelkezők",
    16: "Intézmény-/szakváltás",
    17: "Rövid ciklusú diplomával rendelkezők",
    18: "Intézmény-/szakváltás (nemzetközi)",
}

# Szülői végzettség
QUALIFICATION_LABELS = {
    1: "Középiskola (12. évfolyam)",
    2: "Felsőfokú - BSc",
    3: "Felsőfokú - egyetemi diploma",
    4: "Felsőfokú - MSc",
    5: "Felsőfokú - PhD",
    6: "Felsőoktatásban tanul (befejezetlen)",
    7: "12. évfolyam - nem fejezte be",
    8: "11. évfolyam - nem fejezte be",
    9: "7. évfolyam (régi rendszer)",
    10: "Egyéb - 11. évfolyam",
    11: "2. kiegészítő középiskolai év",
    12: "10. évfolyam",
    13: "Általános kereskedelmi kurzus",
    14: "Alapfok 3. ciklus (9-11. évfolyam)",
    15: "Kiegészítő középiskolai kurzus",
    16: "Technikai-szakmai kurzus",
    17: "Kiegészítő középiskola - nem fejezte be",
    18: "7. évfolyam",
    19: "Általános középiskola 2. ciklusa",
    20: "9. évfolyam - nem fejezte be",
    21: "8. évfolyam",
    22: "Igazgatási és kereskedelmi általános kurzus",
    23: "Kiegészítő könyvelés és igazgatás",
    24: "Ismeretlen",
    25: "Nem tud írni-olvasni",
    26: "Tud olvasni, 4. évfolyam nélkül",
    27: "Alapfok 1. ciklus (4-5. évfolyam)",
    28: "Alapfok 2. ciklus (6-8. évfolyam)",
    29: "Technológiai szakosító kurzus",
    30: "Felsőfokú diploma (1. ciklus)",
    31: "Speciális felsőfokú tanulmányok",
    32: "Felsőfokú technikusi képzés",
    33: "Felsőfokú - MSc (2. ciklus)",
    34: "Felsőfokú - PhD (3. ciklus)",
}

# Felsőfokú végzettséghez tartozó kódok
HIGHER_EDU_CODES = [
    2,
    3,
    4,
    5,
    40,
    41,
    43,
    44,
]

# Bináris mezők
YES_NO = {
    0: "Nem",
    1: "Igen",
}

GENDER_LABELS = {
    0: "Nő",
    1: "Férfi",
}

# Modell feature listák

# Beiratkozás előtti modell változói
EARLY_FEATURES = [
    "Age at enrollment",
    "Gender",
    "Scholarship holder",
    "Debtor",
    "Tuition fees up to date",
    "Displaced",
    "Application order",
    "mother_has_degree",
    "father_has_degree",
    "International",
    "Application mode",
    "Course",
    "Marital status",
]

# Első féléves adatokkal kiegészített változók
MIDTERM_EXTRA_FEATURES = [
    "Curricular units 1st sem (credited)",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 1st sem (without evaluations)",
]

MIDTERM_FEATURES = EARLY_FEATURES + MIDTERM_EXTRA_FEATURES

# StandardScaler által használt numerikus oszlopok
NUMERIC_COLS = [
    "Application order",
    "Age at enrollment",
    "Curricular units 1st sem (credited)",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 1st sem (without evaluations)",
    "Curricular units 2nd sem (credited)",
    "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (evaluations)",
    "Curricular units 2nd sem (approved)",
    "Curricular units 2nd sem (grade)",
    "Curricular units 2nd sem (without evaluations)",
    "Unemployment rate",
    "Inflation rate",
    "GDP",
]

# Fájlútvonalak
DATA_PATH = "data/student_data.csv"
MODELS_DIR = "models"
