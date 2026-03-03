📊 Slack AI Data Bot MVP
🚀 Overview

This project is a minimal Slack application that converts natural language questions into SQL queries using LangChain, executes them on a PostgreSQL database, and returns formatted results directly in Slack.

The bot supports interactive features such as CSV export and conditional chart visualization for date range queries.

🎯 Features

✅ Slack Slash Command /ask-data

✅ Natural Language → SQL using LangChain

✅ Local LLM integration via Ollama

✅ PostgreSQL execution

✅ Formatted Slack responses

✅ Async handling to avoid Slack timeout

✅ CSV export via interactive button

✅ Conditional chart visualization (date range queries)

✅ Basic in-memory caching (optional enhancement)

🏗 Architecture
Slack (/ask-data)
        ↓
Flask Server (/slack endpoint)
        ↓
Background Thread (Async processing)
        ↓
LangChain + Ollama (NL → SQL)
        ↓
PostgreSQL
        ↓
Slack Response (via response_url)
🛠 Tech Stack

Python 3.10

Flask

LangChain

Ollama (phi3:mini model)

PostgreSQL

Slack API (Slash Commands + Block Kit)

ngrok (for local testing)

QuickChart API (for chart generation)

🗄 Database Schema
CREATE TABLE IF NOT EXISTS public.sales_daily (
    date date NOT NULL,
    region text NOT NULL,
    category text NOT NULL,
    revenue numeric(12,2) NOT NULL,
    orders integer NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (date, region, category)
);
How to Run
1️⃣ Start Ollama
ollama serve

Ensure the model is installed:

ollama pull phi3:mini
2️⃣ Start Flask App
python app.py
3️⃣ Expose Local Server Using ngrok
ngrok http 3000

Copy the HTTPS forwarding URL and configure it in Slack:

Slash Command Request URL:

https://your-ngrok-url/slack

Interactivity Request URL:

https://your-ngrok-url/slack
💬 Example Usage

In Slack:

/ask-data show revenue by region for 2025-09-01
Output:

Formatted table

📊 Chart (if date range query)

"Export CSV" interactive button

📈 Chart Visualization

If a user asks a date range query:

/ask-data show revenue by date between 2025-09-01 and 2025-09-02

The bot:

Generates SQL

Returns table

Displays a line chart using QuickChart API

📤 CSV Export

After results are displayed, users can click:

Export CSV

The bot generates a CSV version of the last query result and sends it as a formatted message.

⚡ Handling Slack Timeout

Slack requires responses within 3 seconds.

To handle this:

The bot immediately acknowledges the request.

Heavy processing runs in a background thread.

Final result is sent using Slack’s response_url.

This prevents operation_timeout errors.

