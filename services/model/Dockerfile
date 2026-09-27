FROM python:3.11-slim

WORKDIR /app

# Dépendances d'abord (cache Docker)
COPY services/model/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code + modèle
COPY services/model/app/ ./app/
COPY services/model/models/ ./models/

# Le pipeline sérialisé référence src.pipeline_texte._to_dense (FunctionTransformer) :
# sans ce package, joblib.load lève ModuleNotFoundError: No module named 'src'.
COPY src/ ./src/

EXPOSE 8000

# Healthcheck : le compose attend que /health réponde 200 avant de marquer healthy
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
