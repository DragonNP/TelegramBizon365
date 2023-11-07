FROM python:3.9-slim

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY database ./database/
COPY Bizon/ ./Bizon/
COPY const_variables.py ./
COPY main.py ./

CMD ["python", "./main.py"]