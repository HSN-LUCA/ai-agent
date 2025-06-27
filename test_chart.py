from ai_agent import DatabaseAIAgent
import pandas as pd

# Test chart functionality
agent = DatabaseAIAgent()

# Test questions that should generate charts
test_questions = [
    "Show me sales by product",
    "Top 5 selling products",
    "Show me total sales this month"
]

for question in test_questions:
    print(f"\nTesting: {question}")
    response = agent.query(question)
    
    if response["success"]:
        print(f"Answer: {response['answer']}")
        print(f"SQL: {response['sql_query']}")
        
        if response.get("chart_data") is not None:
            print(f"Chart data shape: {response['chart_data'].shape}")
            print(f"Columns: {list(response['chart_data'].columns)}")
            print(response['chart_data'].head())
        else:
            print("No chart data generated")
    else:
        print(f"Error: {response['answer']}")
    print("-" * 50)