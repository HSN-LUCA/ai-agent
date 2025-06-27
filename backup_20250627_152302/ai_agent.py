import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine

load_dotenv()

class DatabaseAIAgent:
    def __init__(self, db_path="business.db", use_sql_server=False):
        if use_sql_server:
            # SQL Server connection
            server = os.getenv("DB_SERVER")
            database = os.getenv("DB_DATABASE")
            username = os.getenv("DB_USERNAME")
            password = os.getenv("DB_PASSWORD")
            driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
            
            connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
            self.engine = create_engine(connection_string)
        else:
            # SQLite connection (default)
            self.engine = create_engine(f"sqlite:///{db_path}")
        
        self.db = SQLDatabase(self.engine)
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.db_chain = SQLDatabaseChain.from_llm(
            llm=self.llm,
            db=self.db,
            verbose=True,
            return_intermediate_steps=True
        )
    
    def query(self, question):
        """Process natural language question and return answer"""
        try:
            result = self.db_chain(question)
            return {
                "success": True,
                "answer": result["result"],
                "sql_query": result["intermediate_steps"][0] if result["intermediate_steps"] else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": "Sorry, I couldn't process your question. Please try rephrasing it."
            }
    
    def get_table_info(self):
        """Get database schema information"""
        return self.db.get_table_info()