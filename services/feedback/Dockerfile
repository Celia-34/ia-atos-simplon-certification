FROM python:3.11-slim

WORKDIR /app

# Dépendances d'abord (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# `data/` (prod_scored.csv + feedbacks.db) et `scripts/` (feedback_store) sont
# montés par le compose : la base de feedbacks doit survivre au conteneur.
ENV DATA_DIR=/data \
    SCRIPTS_DIR=/scripts \
    FEEDBACK_DB=/data/feedbacks.db

EXPOSE 8002

HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8002/health').status==200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
