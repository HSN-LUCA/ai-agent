from ai_agent import DatabaseAIAgent

# Debug chart data extraction
agent = DatabaseAIAgent()
response = agent.query("Top 5 selling products")

print("=== DEBUG CHART DATA ===")
print(f"Success: {response['success']}")
print(f"Answer: {response['answer']}")
print(f"SQL Query type: {type(response['sql_query'])}")
print(f"SQL Query: {response['sql_query']}")
print(f"Chart data type: {type(response.get('chart_data'))}")
print(f"Has chart: {response.get('has_chart')}")

if response.get('chart_data') is not None:
    print(f"Chart data shape: {response['chart_data'].shape}")
    print(f"Chart data columns: {list(response['chart_data'].columns)}")
    print("Chart data preview:")
    print(response['chart_data'])
else:
    print("No chart data extracted")

# Try manual SQL execution
try:
    import pandas as pd
    manual_data = pd.read_sql("""
    SELECT product_name, SUM(quantity) AS total_quantity
    FROM sales
    GROUP BY product_name
    ORDER BY total_quantity DESC
    LIMIT 5
    """, agent.engine)
    print("\n=== MANUAL SQL EXECUTION ===")
    print(manual_data)
except Exception as e:
    print(f"Manual SQL failed: {e}")