import plotly.graph_objects as go
import pandas as pd

def create_gauge_chart(score, title):
    """
    Create a gauge chart for match scores
    """
    # Determine color based on score
    if score >= 80:
        color = "#00CC66"  # Green
    elif score >= 60:
        color = "#3399FF"  # Blue
    elif score >= 40:
        color = "#FFB84D"  # Orange
    else:
        color = "#FF6666"  # Red
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#FFE6E6'},
                {'range': [40, 60], 'color': '#FFF4E6'},
                {'range': [60, 80], 'color': '#E6F3FF'},
                {'range': [80, 100], 'color': '#E6FFE6'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        font={'family': "Arial"}
    )
    
    return fig

def create_skill_comparison_chart(matched_count, missing_count, extra_count):
    """
    Create a bar chart comparing skill categories
    """
    categories = ['Matched Skills', 'Missing Skills', 'Extra Skills']
    values = [matched_count, missing_count, extra_count]
    colors = ['#00CC66', '#FF6666', '#3399FF']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            text=values,
            textposition='auto',
            marker=dict(
                color=colors,
                line=dict(color='rgba(0,0,0,0.3)', width=2)
            ),
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Skill Distribution Analysis",
        xaxis_title="Skill Category",
        yaxis_title="Number of Skills",
        height=400,
        showlegend=False,
        font={'family': "Arial", 'size': 14},
        hovermode='x'
    )
    
    return fig

def create_category_breakdown_chart(categorized_skills):
    """
    Create a horizontal bar chart showing skills by category
    """
    if not categorized_skills:
        return None
    
    categories = []
    counts = []
    
    for category, skills in categorized_skills.items():
        categories.append(category.replace('_', ' ').title())
        counts.append(len(skills))
    
    # Sort by count
    sorted_data = sorted(zip(categories, counts), key=lambda x: x[1], reverse=True)
    categories, counts = zip(*sorted_data) if sorted_data else ([], [])
    
    fig = go.Figure(data=[
        go.Bar(
            y=categories,
            x=counts,
            orientation='h',
            text=counts,
            textposition='auto',
            marker=dict(
                color='#3399FF',
                line=dict(color='rgba(0,0,0,0.3)', width=2)
            ),
            hovertemplate='<b>%{y}</b><br>Skills: %{x}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Skills Breakdown by Category",
        xaxis_title="Number of Skills",
        yaxis_title="Category",
        height=max(300, len(categories) * 40),
        showlegend=False,
        font={'family': "Arial", 'size': 12}
    )
    
    return fig
