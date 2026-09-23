FROM python:3.11-slim

WORKDIR /app

# Dépendances d'abord (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code + modèle. Le contexte de build est `services/model/` : depuis la
# suppression du NLP, le pipeline sérialisé n'est plus qu'un assemblage de
# transformeurs scikit-learn standards (ColumnTransformer / OneHotEncoder /
# SimpleImputer / RandomForest). Il ne référence plus aucun callable maison
# (`src.pipeline_texte._to_dense` a disparu avec le TF-IDF), donc `src/` n'a
# plus à être embarqué dans l'image.
COPY app/ ./app/
COPY models/ ./models/

EXPOSE 8000

# Healthcheck : le compose attend que /health réponde 200 avant de marquer healthy
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
