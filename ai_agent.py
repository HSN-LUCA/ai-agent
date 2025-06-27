import os
import pandas as pd
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
        # Get API key from multiple sources
        api_key = os.getenv("OPENAI_API_KEY")
        try:
            import streamlit as st
            api_key = api_key or st.secrets.get("OPENAI_API_KEY")
        except:
            pass
        
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=api_key
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
            sql_query = result["intermediate_steps"][0] if result["intermediate_steps"] else None
            
            # Get data for charts - always try to extract data
            chart_data = None
            if sql_query:
                try:
                    # Handle different types of sql_query (string or dict)
                    sql_to_execute = sql_query
                    if isinstance(sql_query, dict):
                        sql_to_execute = sql_query.get('sql', str(sql_query))
                    elif isinstance(sql_query, str) and "SELECT" in sql_query.upper():
                        # Find the actual SQL query
                        lines = sql_query.split('\n')
                        for line in lines:
                            if line.strip().upper().startswith('SELECT'):
                                sql_to_execute = line.strip()
                                break
                    
                    chart_data = pd.read_sql(sql_to_execute, self.engine)
                    print(f"Chart data extracted: {chart_data.shape}")
                except Exception as e:
                    print(f"Chart data extraction failed: {e}")
                    # Try direct SQL execution as fallback
                    try:
                        # Extract SQL from intermediate steps more carefully
                        if result.get("intermediate_steps"):
                            for step in result["intermediate_steps"]:
                                if isinstance(step, str) and "SELECT" in step.upper():
                                    chart_data = pd.read_sql(step, self.engine)
                                    print(f"Fallback chart data extracted: {chart_data.shape}")
                                    break
                    except Exception as fallback_error:
                        print(f"Fallback also failed: {fallback_error}")
                        pass
            
            return {
                "success": True,
                "answer": result["result"],
                "sql_query": sql_query,
                "chart_data": chart_data,
                "has_chart": chart_data is not None and len(chart_data) > 0 if chart_data is not None else False
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