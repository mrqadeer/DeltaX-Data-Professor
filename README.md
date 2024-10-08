# DeltaX Data Professor

This project integrates multiple large language models (LLMs) like PandasAI, LangChain, OpenAI, Google Gemini, Anthropic, and Groq to allow users to interact with their data using natural language. Users can upload files in CSV, TSV, Excel formats or connect to databases like MySQL, SQLite, and PostgreSQL to perform data analysis, querying, and exploration. The chatbot supports both text and voice input, making it versatile for different interaction preferences.

## Table of Contents

- [DeltaX Data Professor](#deltax-data-professor)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
    - [Windows Setup](#windows-setup)
    - [Linux Setup](#linux-setup)
  - [Environment Setup](#environment-setup)
    - [Windows Environment](#windows-environment)
    - [Linux Environment](#linux-environment)
  - [Usage](#usage)
    - [File Upload](#file-upload)
    - [Database Connection](#database-connection)
    - [Text Input Interaction](#text-input-interaction)
    - [Voice Input Interaction](#voice-input-interaction)
  - [Contribution](#contribution)
  - [License](#license)

## Features

- **Multi-LLM Integration**: Supports PandasAI, LangChain, OpenAI, Google Gemini, Anthropic, and Groq models.
- **Data Formats**: Upload and analyze CSV, TSV, and Excel files.
- **Database Connections**: Connect to MySQL, SQLite, and PostgreSQL databases for analysis.
- **Text and Voice Input**: Users can interact with the chatbot via text or voice for a seamless experience.
- **Natural Language Data Analysis**: Perform data exploration, querying, and analysis using conversational language.

## Installation

### Windows Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/mrqadeer/DeltaX-Data-Professor.git
    cd DeltaX-Data-Professor
    ```

2. Install dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

3. Alternatively, set up a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

### Linux Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/mrqadeer/DeltaX-Data-Professor.git
    cd DeltaX-Data-Professor
    ```

2. Install dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

3. Alternatively, set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Environment Setup

### Windows Environment

1. Install Anaconda from [official site](https://www.anaconda.com/products/distribution).
2. Create a new environment:
    ```bash
    conda create --name chatbot_env python=3.12
    conda activate chatbot_env
    pip install -r requirements.txt
    ```

### Linux Environment

1. Install Anaconda:
    ```bash
    wget https://repo.anaconda.com/archive/Anaconda3-2023.07-Linux-x86_64.sh
    bash Anaconda3-2023.07-Linux-x86_64.sh
    ```

2. Create and activate a new environment:
    ```bash
    conda create --name chatbot_env python=3.12
    conda activate chatbot_env
    pip install -r requirements.txt
    ```

## Usage

### File Upload

1. Upload a CSV, TSV, or Excel file via the interface.
2. The chatbot will automatically parse the file and allow you to query the data in natural language.

### Database Connection

1. Connect to MySQL, SQLite, or PostgreSQL by providing the connection details.
2. Once connected, you can use natural language to query and analyze data from the database.

### Text Input Interaction

- Type your query related to data analysis or exploration, and the chatbot will respond using the connected LLM models.

### Voice Input Interaction

- Speak your query into the microphone, and the chatbot will process the speech and provide results based on the analysis of the data.

## Contribution

We welcome contributions to enhance the functionality of this chatbot. To contribute:
For detail please refer to [CONTRIBUTE.md](CONTRIBUTE.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
