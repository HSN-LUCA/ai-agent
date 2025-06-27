# AI Database Query Agent

A natural language to SQL query AI agent with web UI that can connect to any database.

## Features

- 🤖 Natural language to SQL conversion using LangChain
- 💬 Interactive web UI built with Streamlit
- 🗄️ Database connectivity (SQLite demo, easily extensible)
- 📊 Sample business data (sales & stock)
- 🔍 Query history and SQL preview

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key:**
   - Add your API key to `.env` file
   - Or enter it in the UI sidebar

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Ask questions like:**
   - "Show me total sales this month"
   - "Give me last week's stock movement"
   - "What are the top 5 selling products?"

## Database Connection

To connect to your own database, modify `ai_agent.py`:

```python
# For PostgreSQL
engine = create_engine("postgresql://user:password@localhost/dbname")

# For MySQL
engine = create_engine("mysql://user:password@localhost/dbname")
```

## Architecture

- `app.py` - Streamlit UI
- `ai_agent.py` - LangChain SQL agent
- `database.py` - Sample data generator
- `requirements.txt` - Dependencies