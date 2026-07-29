FROM python:3.11-slim

WORKDIR /app

# Rendszerfüggőségek (scikit-learn/pandas fordításhoz némelyik wheel-hez kellhet)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Függőségek telepítése (külön layer, hogy a cache jól működjön)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projekt fájlok bemásolása
COPY . .

# Modellek betanítása build időben, hogy a konténer induláskor
# már azonnal használható legyen (nem kell külön lépés indításkor)
RUN python train_models.py

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true"]
