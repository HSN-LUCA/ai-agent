import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
from ai_agent import DatabaseAIAgent
from database import create_sample_database
from voice_recognition import get_audio_processor
from text_to_speech import text_to_speech
import time

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
                try:
                    os.environ["DB_SERVER"] = st.session_state.get("db_server", os.getenv("SQL_SERVER", ""))
                    os.environ["DB_DATABASE"] = st.session_state.get("db_database", os.getenv("SQL_DATABASE", ""))
                    os.environ["DB_USERNAME"] = st.session_state.get("db_username", os.getenv("SQL_USERNAME", ""))
                    os.environ["DB_PASSWORD"] = st.session_state.get("db_password", os.getenv("SQL_PASSWORD", ""))
                except Exception as e:
                    st.error(f"Error setting database environment variables: {str(e)}")
                    st.info("Using values from .env file or UI inputs instead.")
            
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
            st.subheader("💬 Try these questions:")
            sample_questions = [
                "Show me sales by product",
                "Top 5 selling products",
                "Show me total sales by product",
                "Sales quantity by product name",
                "Stock levels by product"
            ]
            
            cols = st.columns(len(sample_questions))
            for i, question in enumerate(sample_questions):
                if cols[i].button(question, key=f"sample_{i}"):
                    process_question(question)
            
            # Chat input
            st.subheader("Ask your question:")
            
            # Initialize voice processing state
            if 'voice_text' not in st.session_state:
                st.session_state.voice_text = ""
            if 'is_listening' not in st.session_state:
                st.session_state.is_listening = False
                
            # Get audio processor
            audio_processor = get_audio_processor()
            
            # Voice input section
            voice_col1, voice_col2 = st.columns([3, 1])
            with voice_col1:
                user_question = st.text_input("Enter your question here...", 
                                             key="user_input", 
                                             value=st.session_state.voice_text)
            with voice_col2:
                if st.button("🎤 Voice Input"):
                    st.session_state.is_listening = True
                    audio_processor.start_listening()
            
            # Display listening status
            if st.session_state.is_listening:
                status_placeholder = st.empty()
                status_placeholder.info("🎤 Listening... Speak now")
                
                # Check for voice input results
                while audio_processor.is_listening:
                    time.sleep(0.1)
                    st.session_state.voice_text = audio_processor.get_text()
                    if st.session_state.voice_text:
                        break
                
                # Update UI when voice input is complete
                if st.session_state.voice_text:
                    status_placeholder.success(f"🎤 Recognized: {st.session_state.voice_text}")
                    st.session_state.is_listening = False
                    st.rerun()
                else:
                    status_placeholder.error("🎤 No speech detected. Try again.")
                    st.session_state.is_listening = False
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("💬 Ask") and user_question:
                    process_question(user_question)
            with col2:
                if st.button("📊 Ask + Chart") and user_question:
                    process_question(user_question)
            with col3:
                if st.button("🔊 Ask with Voice") and user_question:
                    # Process the question and enable text-to-speech for response
                    st.session_state.use_tts = True
                    process_question(user_question)

            
            # Show latest response
            if st.session_state.chat_history:
                question, response = st.session_state.chat_history[-1]
                st.subheader("Latest Response:")
                if response["success"]:
                    st.success(f"**Q:** {question}")
                    st.write(f"**A:** {response['answer']}")
                    if response.get('use_tts', False):
                        tts_html = text_to_speech(response['answer'])
                        st.markdown(tts_html, unsafe_allow_html=True)
                    #if response.get("sql_query"):
                        #st.code(response["sql_query"], language="sql")
                    
                    # Chart options - always show if data exists
                    if response.get("chart_data") is not None:
                        try:
                            data_len = len(response["chart_data"])
                            if data_len > 0:
                                st.success(f"📊 Chart data ready: {data_len} rows")
                                
                                # Auto-generate chart
                                st.subheader("📊 Visual Report")
                                create_chart(response["chart_data"], question)
                                
                                # Show data table in expander
                                with st.expander("📋 View Raw Data"):
                                    st.dataframe(response["chart_data"])
                            else:
                                st.warning("Chart data is empty")
                        except Exception as e:
                            st.error(f"Chart display error: {e}")
                            st.dataframe(response["chart_data"])
                    else:
                        st.info("No chart data available for this query")
                else:
                    st.error(f"**Q:** {question}")
                    st.error(response["answer"])
        else:
            st.info("Please configure your API key and initialize the agent to start asking questions.")
    
    # Charts Tab
    #with tab3:
        if st.session_state.chat_history:
            st.subheader("📊 Chart Gallery")
            
            # Filter conversations with chart data
            chart_conversations = [(q, r) for q, r in st.session_state.chat_history 
                                 if r.get("success") and r.get("chart_data") is not None]
            
            # Filter out empty dataframes
            valid_chart_conversations = []
            for q, r in chart_conversations:
                try:
                    if len(r["chart_data"]) > 0:
                        valid_chart_conversations.append((q, r))
                except:
                    pass
            chart_conversations = valid_chart_conversations
            
            if chart_conversations:
                st.write(f"Found {len(chart_conversations)} conversations with chart data")
                
                for i, (question, response) in enumerate(chart_conversations):
                    st.subheader(f"Chart {i+1}: {question}")
                    create_chart(response["chart_data"], question)
                    st.divider()
            else:
                st.info("No chart data available. Ask questions that return data to generate charts!")
        else:
            st.info("No conversations yet. Start asking questions in the Chat tab!")
    
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
                        #if response.get("sql_query"):
                            #st.code(response["sql_query"], language="sql")
                        if response.get("chart_data") is not None:
                            try:
                                if len(response["chart_data"]) > 0:
                                    st.write("📊 **Chart Available**")
                                    create_chart(response["chart_data"], question)
                            except:
                                st.write("📋 **Data Available**")
                                st.dataframe(response["chart_data"])
                    else:
                        st.error(response["answer"])
        else:
            st.info("No chat history yet. Start asking questions in the Chat tab!")

def create_chart(data, question):
    """Create appropriate chart based on data"""
    try:
        st.write(f"📊 Generating chart for {len(data)} records...")
        
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        text_cols = data.select_dtypes(include=['object', 'string']).columns.tolist()
        
        # Limit data for better visualization
        if len(data) > 15:
            data = data.head(15)
        
        # Choose chart type based on data structure
        if len(numeric_cols) >= 1 and len(text_cols) >= 1:
            # Bar chart for categorical + numeric
            fig = px.bar(
                data, 
                x=text_cols[0], 
                y=numeric_cols[0],
                title=f"📊 {question[:40]}...",
                color=numeric_cols[0]
            )
        elif len(numeric_cols) >= 2:
            # Scatter plot for numeric vs numeric
            fig = px.scatter(
                data,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title=f"📈 {question[:40]}..."
            )
        elif len(data.columns) >= 2:
            # Default bar chart
            fig = px.bar(
                data,
                x=data.columns[0],
                y=data.columns[1],
                title=f"📊 {question[:40]}..."
            )
        else:
            # Single column - show as histogram
            fig = px.histogram(
                data,
                x=data.columns[0],
                title=f"📊 {question[:40]}..."
            )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show data table below chart
        with st.expander("📋 View Data Table"):
            st.dataframe(data)
            
    except Exception as e:
        st.error(f"Chart generation failed: {str(e)}")
        st.write("📋 **Raw Data:**")
        st.dataframe(data)

def process_question(question):
    """Process user question and display response"""
    # Check if text-to-speech is requested
    use_tts = st.session_state.get('use_tts', False)
    
    with st.spinner("Processing your question..."):
        response = st.session_state.agent.query(question)
        st.session_state.chat_history.append((question, response))
        
        # Store TTS flag in the response for later use
        if use_tts:
            response['use_tts'] = True
            # Reset the flag for next question
            st.session_state.use_tts = False
            
        st.rerun()
if __name__ == "__main__":
    main()