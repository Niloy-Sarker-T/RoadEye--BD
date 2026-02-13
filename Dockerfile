FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install streamlit

COPY app/ ./app

EXPOSE 8501
EXPOSE 8000

# Run FastAPI + Streamlit together
CMD bash -c "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0"
