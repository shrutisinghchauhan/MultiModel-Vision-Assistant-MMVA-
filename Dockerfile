# Use Python 3.9.18 as the base image
FROM python:3.9.18

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
