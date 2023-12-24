## Thesis Assignment API

Assignment solver using GA(Genetic algorithm), available at localhost:8000/assignment/v2, see more endpoints at localhost:8000/docs

## Install

Recommend to create a new python virtual environment to maintain the integrity global packages, avoiding messing up

This is tested in Python 3.8

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

uvicorn main:app --reload

## API Specs

localhost:8000/docs
