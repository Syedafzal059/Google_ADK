# Google ADK - Basic Agent

A simple Google ADK (Agent Development Kit) project demonstrating a basic LLM agent setup.

## Prerequisites

- Python 3.11+
- Virtual environment (recommended)

## Installation

1. Clone this repository
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Agent

To start the agent in web mode, simply run:

```bash
adk web
```

This will start the ADK web interface where you can interact with your agent.

## Project Structure

```
Google_ADK/
├── 1-basic-agent/
│   ├── __init__.py
│   └── agent.py
├── requirements.txt
└── README.md
```

## Features

- Basic LLM agent using GPT-4O
- Environment variable configuration
- Simple instruction-based agent setup

## Documentation

For more information about Google ADK, visit the [official documentation](https://github.com/google/adk).

