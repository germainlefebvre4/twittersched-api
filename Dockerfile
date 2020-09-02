FROM python:3.6
WORKDIR /usr/src/app

COPY Pipfile* ./
RUN pip install pipenv && \
    pipenv lock --requirements > requirements.txt && \
    pip install -r requirements.txt

COPY . ./

ENTRYPOINT ["python", "main.py"]
