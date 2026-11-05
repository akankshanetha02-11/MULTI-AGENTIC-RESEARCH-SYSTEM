# Multi-Agent Research Assistant

A Streamlit application that researches a topic with a multi-stage AI workflow. It searches the web, extracts content from a relevant page, writes a structured report, and asks a critic model to review the result.

## Features

- **Search agent:** Finds recent web results with Tavily.
- **Reader agent:** Scrapes a selected result and extracts readable page content.
- **Writer:** Creates a report with an introduction, key findings, conclusion, and sources.
- **Critic:** Scores the report and lists strengths, improvement areas, and a verdict.
- **Streamlit interface:** Shows pipeline progress and results, with an option to download the report as Markdown.

## Requirements

- Python 3.10 or later
- An [OpenRouter API key](https://openrouter.ai/keys)
- A [Tavily API key](https://app.tavily.com/)

## Setup

1. Clone or download this repository and open a terminal in the project directory.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS or Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:

   ```dotenv
   OPENROUTER_API_KEY=your_openrouter_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

   Keep `.env` private; do not commit API keys to version control.

## Run the application

From the project root, with the virtual environment activated:

```bash
streamlit run app.py
```

Streamlit will print a local URL (typically `http://localhost:8501`). Open it in a browser, enter a research topic, and select **Run Research Pipeline**. The report can be downloaded from the results section.

## How it works

The app runs four stages in order:

1. A search agent calls Tavily and returns search results.
2. A reader agent selects a relevant URL and calls the scraping tool.
3. The writer combines the search results and scraped content into a report.
4. The critic reviews the report and returns a score, strengths, areas to improve, and a verdict.

The language model is configured in `src/agents/agents.py` to use `nvidia/nemotron-3-ultra-550b-a55b:free` through OpenRouter. The workflow depends on external APIs and network access; provider availability, rate limits, and model access may affect runs.

## Project structure

```text
.
├── app.py                    # Streamlit user interface and pipeline execution
├── main.py                   # Currently empty
├── requirements.txt          # Python dependencies
└── src/
    ├── agents/
    │   └── agents.py         # Agent and writer/critic chain definitions
    ├── pipelines/
    │   └── pipeline.py       # Programmatic research pipeline
    └── tools/
        └── tools.py          # Tavily search and web-page scraping tools
```

The programmatic pipeline is available as `run_research_pipeline(topic)` from `src.pipelines.pipeline`; the Streamlit interface is the project's main runnable application.

## Troubleshooting

- **Missing API key:** Check that `.env` is in the project root and that both `OPENROUTER_API_KEY` and `TAVILY_API_KEY` are set.
- **Model or provider error:** Verify OpenRouter account access and availability for the configured model.
- **Search or scraping errors:** Confirm internet access. Some websites block automated requests or do not expose extractable article text.
