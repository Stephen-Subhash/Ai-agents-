import streamlit as st
import time
import random
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Agent Building Hub",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Better Visualization ---
st.markdown("""
<style>
    .agent-card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .agent-card:hover {
        transform: scale(1.02);
    }
    .status-badge {
        font-weight: bold;
        background-color: rgba(255,255,255,0.2);
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.9em;
    }
    .log-box {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
        font-family: monospace;
        font-size: 0.85em;
        height: 150px;
        overflow-y: auto;
        text-align: left;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Agent Management ---
st.sidebar.title("🏗️ Control Panel")
st.sidebar.markdown("Add new AI agents to the building.")

with st.sidebar.form("add_agent_form"):
    agent_name = st.text_input("Agent Name")
    agent_role = st.selectbox(
        "Role / Department", 
        ["Manager", "Developer", "Designer", "Data Analyst", "Security", "Custom"]
    )
    submitted = st.form_submit_button("➕ Deploy Agent")

if submitted and agent_name:
    if 'agents' not in st.session_state:
        st.session_state.agents = []
    
    # Define colors based on role
    role_colors = {
        "Manager": "#FF4B4B",
        "Developer": "#2E86C1",
        "Designer": "#F39C12",
        "Data Analyst": "#27AE60",
        "Security": "#8E44AD",
        "Custom": "#95a5a6"
    }
    
    new_agent = {
        "id": len(st.session_state.agents),
        "name": agent_name,
        "role": agent_role,
        "color": role_colors.get(agent_role, "#95a5a6"),
        "status": "Idle",
        "logs": []
    }
    st.session_state.agents.append(new_agent)
    st.sidebar.success(f"✅ {agent_name} deployed successfully!")
    st.rerun()
elif submitted and not agent_name:
    st.sidebar.error("⚠️ Please enter an agent name.")

# --- Main Dashboard ---
st.title("🏢 Virtual AI Office Building")
st.markdown("Visualize your autonomous agents working in real-time. No external APIs required.")

if 'agents' not in st.session_state or len(st.session_state.agents) == 0:
    st.info("👋 The building is empty. Use the sidebar to deploy your first AI Agent.")
    st.stop()

# Create columns dynamically based on number of agents
cols = st.columns(len(st.session_state.agents))

# Simulation Tasks
tasks_db = {
    "Manager": ["Reviewing KPIs", "Approving Budgets", "Team Meeting", "Strategic Planning"],
    "Developer": ["Writing Code", "Debugging Module", "Code Review", "Deploying Build"],
    "Designer": ["Sketching UI", "Optimizing Assets", "Client Feedback", "Prototyping"],
    "Data Analyst": ["Cleaning Data", "Running Models", "Generating Reports", "Visualizing Trends"],
    "Security": ["Scanning Ports", "Updating Firewall", "Audit Logs", "Penetration Test"],
    "Custom": ["Processing Request", "Learning New Task", "Optimizing Workflow", "Executing Script"]
}

# Update Logic & Rendering
for i, agent in enumerate(st.session_state.agents):
    with cols[i]:
        # Simulate Activity
        if random.random() > 0.2: # 80% chance to update status
            possible_tasks = tasks_db.get(agent['role'], ["Working on task"])
            current_task = random.choice(possible_tasks)
            agent['status'] = f"🟢 {current_task}"
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {current_task}"
            
            # Keep only last 5 logs to save memory
            agent['logs'].insert(0, log_entry)
            if len(agent['logs']) > 5:
                agent['logs'].pop()
        
        # Render Card
        st.markdown(f"""
        <div class="agent-card" style="background-color: {agent['color']};">
            <h3>{agent['name']}</h3>
            <p><b>{agent['role']}</b></p>
            <span class="status-badge">{agent['status']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Render Log Box
        st.markdown('<div class="log-box">', unsafe_allow_html=True)
        for log in agent['logs']:
            st.write(log)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer / Refresh Mechanism
st.divider()
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    if st.button("🔄 Refresh Simulation State", use_container_width=True):
        st.rerun()

st.caption("System Status: 🟢 Localhost | Mode: Lightweight Simulation | Version 1.0")
