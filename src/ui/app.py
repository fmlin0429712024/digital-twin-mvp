import streamlit as st
import time
import sys
import os

# Add project root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.simulator import Simulator
from src.core.normalizer import IntelligentMembrane
from src.backend.firebase_manager import FirebaseManager
from src.ui.dashboard import render_dashboard

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Holistic Digital Twin",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZATION (Singleton Pattern using Session State) ---
if 'simulator' not in st.session_state:
    st.session_state.simulator = Simulator()
    st.session_state.normalizer = IntelligentMembrane()
    st.session_state.firebase = FirebaseManager()
    st.session_state.history = [] # In-memory history for MVP charts
    st.session_state.is_running = False

# --- SIDEBAR CONTROLS ---
st.sidebar.title("🏭 Digital Twin Control")
st.sidebar.markdown("---")

# Simulation Controls
st.sidebar.header("Simulation Override")
if st.sidebar.button("🚨 SIMULATE CRITICAL FAILURE", type="primary"):
    st.session_state.simulator.trigger_anomaly(True)
    st.toast("🔥 Critical Failure Injected!", icon="⚠️")

if st.sidebar.button("✅ RESTORE NORMAL OPERATIONS"):
    st.session_state.simulator.trigger_anomaly(False)
    st.toast("System Restored.", icon="✅")

st.sidebar.markdown("---")
auto_refresh = st.sidebar.checkbox("Actively Monitor (Poll)", value=True)

# --- MAIN APP LOGIC ---
st.title("Holistic Industrial Digital Twin")
st.markdown("### Real-time Asset Health Monitoring")

# --- SOLUTION OVERVIEW ---
with st.expander("ℹ️ Solution Overview & Demo Guide", expanded=False):
    st.markdown("""
    ### 🎯 Vision: From Chaos to Order
    This project demonstrates a **"Holistic Digital Twin"** that transforms raw, chaotic industrial data into actionable business value using a **Metadata-Driven Architecture**.

    ### 🏗️ Architecture
    1.  **The Chaos (Simulator)**: Generates raw, unstandardized sensor packets (e.g., `id: 0x5A, val: 400`).
    2.  **The Intelligent Membrane (Spec Kit)**: A metadata registry that identifies the data signature and applies the correct "Spec" (specification).
    3.  **The Value (Dashboard)**: Automatically renders the correct visualization (Gauge vs. Chart) based on the asset type.

    ### 🕹️ Demo Experience
    1.  **Observe Normal Operations**: Notice the "Drift" in temperature and "Vibration" noise.
    2.  **Inject Chaos**: Open the Sidebar 👈 and click **"🚨 SIMULATE CRITICAL FAILURE"**.
    3.  **Witness Real-Time Impact**: 
        - The **Spec Kit** captures the anomaly.
        - The **Dashboard** turns red instantly (<1s latency).
    """)

# Placeholder for the main dashboard
dashboard_placeholder = st.empty()

def update_loop():
    # 1. Generate Chaos
    raw_packets = list(st.session_state.simulator.run_tick())
    
    # 2. Apply Order (Normalize)
    normalized_batch = []
    for packet in raw_packets:
        norm_data = st.session_state.normalizer.normalize(packet)
        if norm_data:
            normalized_batch.append(norm_data)
            # Log to Backend
            st.session_state.firebase.log_state(norm_data)
    
    # Update History (Keep last 100 points per asset for charts)
    st.session_state.history.extend(normalized_batch)
    # Pruning could happen here to prevent memory overflow in long-running app
    if len(st.session_state.history) > 500:
        st.session_state.history = st.session_state.history[-500:]

    # 3. Render Value
    with dashboard_placeholder.container():
        render_dashboard(normalized_batch, st.session_state.history)
    
    # Indication of last update
    # st.caption(f"Last heartbeat: {time.ctime()}")

# Loop Logic
if auto_refresh:
    update_loop()
    time.sleep(2.0) # Refresh rate (simulate <1s latency)
    st.rerun()
else:
    st.info("Monitoring paused. Use sidebar to resume.")
    # Run once to show static state
    update_loop()
