import json
from datetime import datetime

def export_chat_history():
    """Export this development chat history"""
    
    chat_history = [
        {
            "timestamp": "2024-12-01",
            "conversation": [
                {"role": "user", "content": "need build ai agent with UI , can be connected with any DB , Query Generator LangChain"},
                {"role": "assistant", "content": "Built complete AI agent with Streamlit UI, LangChain SQL integration, database connectivity"},
                {"role": "user", "content": "need to connect with DB SQL"},
                {"role": "assistant", "content": "Added SQL Server support with pyodbc, environment variables, UI configuration"},
                {"role": "user", "content": "can you make chat history in new tab like chat gpt"},
                {"role": "assistant", "content": "Created ChatGPT-style tabs: Chat tab for active conversation, History tab for all conversations"},
                {"role": "user", "content": "just change name of app to logx , and add option to set my logo"},
                {"role": "assistant", "content": "Changed app name to LogX, added logo upload functionality with file uploader"},
                {"role": "user", "content": "please remove Logo Path (optional)"},
                {"role": "assistant", "content": "Removed logo path input, kept only file uploader for cleaner interface"},
                {"role": "user", "content": "how to save source buckup for this app"},
                {"role": "assistant", "content": "Created backup.bat and backup.py scripts for timestamped source code backups"},
                {"role": "user", "content": "what about chat history with you"},
                {"role": "assistant", "content": "Creating export script for our development conversation history"}
            ]
        }
    ]
    
    filename = f"dev_chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(chat_history, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Development chat history exported: {filename}")
    return filename

if __name__ == "__main__":
    export_chat_history()