import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any

def render_metric_card(data: Dict[str, Any]):
    """Renders a single metric card with status encoding."""
    # Determine color based on status
    color = "red" if data["status"] == "CRITICAL" else "green"
    
    st.markdown(f"""
    <div style="
        border-left: 5px solid {color};
        padding: 10px;
        background-color: #262730;
        border-radius: 5px;
        margin-bottom: 10px;
    ">
        <h4 style="margin: 0; color: #fafafa;">{data['display_name']} {data['ui_config']['icon']}</h4>
        <h2 style="margin: 0; color: {color};">{data['value']} {data['unit']}</h2>
        <p style="margin: 0; color: #9c9d9f; font-size: 0.8em;">Status: {data['status']}</p>
    </div>
    """, unsafe_allow_html=True)

def render_gauge(data: Dict[str, Any]):
    """Renders a Plotly gauge chart."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = data["value"],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"{data['display_name']} {data['ui_config']['icon']}"},
        gauge = {
            'axis': {'range': [data['ui_config']['min'], data['ui_config']['max']]},
            'bar': {'color': "red" if data["status"] == "CRITICAL" else "green"},
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': data['ui_config']['max']
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

def render_line_chart(data: Dict[str, Any], history: List[Dict[str, Any]]):
    """Renders a sparkline/chart for historical data."""
    # Filter history for this asset
    asset_history = [d for d in history if d['id'] == data['id']]
    if not asset_history:
        return
        
    df = pd.DataFrame(asset_history)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'], 
        y=df['value'],
        mode='lines',
        name=data['display_name'],
        line=dict(color='firebrick' if data['status'] == 'CRITICAL' else 'royalblue', width=2)
    ))
    
    fig.update_layout(
        title=f"{data['display_name']} {data['ui_config']['icon']}",
        height=250,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis=dict(range=[data['ui_config']['min'] - 5, data['ui_config']['max'] + 5]),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

def render_dashboard(latest_data: List[Dict[str, Any]], history: List[Dict[str, Any]]):
    """Main dashboard renderer."""
    if not latest_data:
        st.warning("Waiting for data stream...")
        return

    # Dynamic Grid Layout driven by Spec "ui_component"
    cols = st.columns(len(latest_data))
    
    for i, data in enumerate(latest_data):
        with cols[i]:
            component_type = data['ui_config']['component']
            
            if component_type == "gauge":
                render_gauge(data)
            elif component_type == "chart":
                render_line_chart(data, history)
            elif component_type == "metric_card":
                render_metric_card(data)
            else:
                st.write(data)
