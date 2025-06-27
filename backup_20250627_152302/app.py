import streamlit as st
import os
from ai_agent import DatabaseAIAgent
from database import create_sample_database

# Page config
st.set_page_config(
    page_title="LogX",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    # Logo section
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=100)
        else:
            st.write("📊")
    
    with col2:
        st.title("LogX")
        st.markdown("Ask questions about your data in natural language!")
    

    
    # Tab navigation
    tab1, tab2 = st.tabs(["💬 Chat", "📝 History"])
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Logo upload
        st.subheader("🎨 Branding")
        uploaded_logo = st.file_uploader("Upload Logo", type=['png', 'jpg', 'jpeg'])
        if uploaded_logo:
            with open("logo.png", "wb") as f:
                f.write(uploaded_logo.getbuffer())
            st.success("Logo uploaded!")
            st.rerun()
        
        st.divider()
        
        # API Key input
        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        
        # Database selection
        db_type = st.selectbox("Database Type", ["SQLite (Demo)", "SQL Server"])
        
        if db_type == "SQL Server":
            st.text_input("Server", key="db_server", value=os.getenv("SQL_SERVER", ""))
            st.text_input("Database", key="db_database", value=os.getenv("SQL_DATABASE", ""))
            st.text_input("Username", key="db_username", value=os.getenv("SQL_USERNAME", ""))
            st.text_input("Password", key="db_password", type="password", value=os.getenv("SQL_PASSWORD", ""))
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            
            # Set DB environment variables if SQL Server
            if db_type == "SQL Server":
                os.environ["DB_SERVER"] = st.session_state.get("db_server", os.getenv("SQL_SERVER", ""))
                os.environ["DB_DATABASE"] = st.session_state.get("db_database", os.getenv("SQL_DATABASE", ""))
                os.environ["DB_USERNAME"] = st.session_state.get("db_username", os.getenv("SQL_USERNAME", ""))
                os.environ["DB_PASSWORD"] = st.session_state.get("db_password", os.getenv("SQL_PASSWORD", ""))
            
            # Initialize agent button
            if st.button("Initialize Agent"):
                try:
                    if db_type == "SQLite (Demo)":
                        if not os.path.exists("business.db"):
                            create_sample_database()
                            st.success("Sample database created!")
                        st.session_state.agent = DatabaseAIAgent()
                    else:
                        st.session_state.agent = DatabaseAIAgent(use_sql_server=True)
                    
                    st.success("Agent initialized successfully!")
                except Exception as e:
                    st.error(f"Error initializing agent: {str(e)}")
            
        # Database info
        if st.session_state.agent:
            with st.expander("Database Schema"):
                st.text(st.session_state.agent.get_table_info())
            
            st.markdown(f"**Total Conversations:** {len(st.session_state.chat_history)}")
        else:
            st.warning("Please enter your OpenAI API key to continue")
    
    # Chat Tab
    with tab1:
        if st.session_state.agent:
            # Sample questions
            st.subheader("Try these sample questions:")
            sample_questions = [
                "Show me total sales this month",
                "Give me last week's stock movement",
                "What are the top 5 selling products?",
                "Show me sales by product",
                "What's the current stock level for each product?"
            ]
            
            cols = st.columns(len(sample_questions))
            for i, question in enumerate(sample_questions):
                if cols[i].button(question, key=f"sample_{i}"):
                    process_question(question)
            
            # Chat input
            st.subheader("Ask your question:")
            user_question = st.text_input("Enter your question here...", key="user_input")
            
            if st.button("Ask") and user_question:
                process_question(user_question)
            
            # Show latest response
            if st.session_state.chat_history:
                question, response = st.session_state.chat_history[-1]
                st.subheader("Latest Response:")
                if response["success"]:
                    st.success(f"**Q:** {question}")
                    st.write(f"**A:** {response['answer']}")
                    if response.get("sql_query"):
                        st.code(response["sql_query"], language="sql")
                else:
                    st.error(f"**Q:** {question}")
                    st.error(response["answer"])
        else:
            st.info("Please configure your API key and initialize the agent to start asking questions.")
    
    # History Tab
    with tab2:
        if st.session_state.chat_history:
            st.subheader(f"Chat History ({len(st.session_state.chat_history)} conversations)")
            
            # Clear history button
            if st.button("🗑️ Clear History"):
                st.session_state.chat_history = []
                st.rerun()
            
            # Display all conversations
            for i, (question, response) in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"#{len(st.session_state.chat_history)-i}: {question[:50]}...", expanded=False):
                    st.write(f"**Question:** {question}")
                    if response["success"]:
                        st.write(f"**Answer:** {response['answer']}")
                        if response.get("sql_query"):
                            st.code(response["sql_query"], language="sql")
                    else:
                        st.error(response["answer"])
        else:
            st.info("No chat history yet. Start asking questions in the Chat tab!")

def process_question(question):
    """Process user question and display response"""
    with st.spinner("Processing your question..."):
        response = st.session_state.agent.query(question)
        st.session_state.chat_history.append((question, response))
        st.rerun()

if __name__ == "__main__":
    main()