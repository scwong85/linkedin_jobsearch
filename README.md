# linkedin_jobsearch
LinkedIn job searching for the pass 24h, hybrid or onsite, mid senior position.

## Prerequisite:
- Install [ollama](https://github.com/ollama/ollama/blob/main/README.md) and download ollama language model, ie phi3, llama3, etc. Check [here](https://github.com/ollama/ollama/blob/main/README.md#model-library) for available models.
- Run ollama server `ollama serve`

## Init
- `python -m venv <your_environment>`
- `source <your_environment>/bin/activate`
- `pip install -r requirements.txt`

## Skill ingestion
- Create a `skills_data` folder and put your skills in a txt file in this folder.
- Run `python ingest.py <language_model>`
- Example: `python ingest.py llama3`

## Job searching
- `python main.py <job_keyword> <location> <language_model>`
- Example: `python main.py "Bioinformatics" "Germany" llama3`

## Results
- The results are written in `<keyword>_<location>_<language_model>` file.