# linkedin_jobsearch
LinkedIn job searching for the pass 24h, hybrid or onsite, mid senior position.

## Prerequisite:
- Install ollama and download ollama language model, ie phi3, llama3, etc. Check [here](https://github.com/ollama/ollama/blob/main/README.md#model-library) for available models.
- Run ollama server `ollama serve`

## Skill ingestion
- Create a skill_data folder and put your skills in a txt file.
- Run `python ingest.py <language_model>`
- Example: `python ingest.py llama3`

## Job searching
- `python main.py <job_keyword> <location> <language_model>`
- Example: `python main.py "Bioinformatics" "Germany" llama3`