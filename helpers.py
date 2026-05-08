import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

PALETTE = {
    'crimson': '#C0152B',
    'rose': '#E8304A',
    'blush': '#F07080',
    'cream': '#FFF5F5',
    'charcoal': '#1A1A2E',
    'slate': '#2D2D44',
    'silver': '#8892A4',
    'white': '#FFFFFF',
    'green': '#22C55E',
    'amber': '#F59E0B',
}

def plotly_theme():
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,46,0.6)',
        font=dict(family='Syne, sans-serif', color='#E8E8F0', size=13),
        xaxis=dict(gridcolor='rgba(255,255,255,0.07)', linecolor='rgba(255,255,255,0.15)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.07)', linecolor='rgba(255,255,255,0.15)'),
        margin=dict(t=40, b=40, l=40, r=20),
    )

def bar_chart(labels, values, title, color='#C0152B', orientation='v'):
    if orientation == 'h':
        fig = go.Figure(go.Bar(x=values, y=labels, orientation='h',
                               marker_color=color, marker_line_width=0))
    else:
        fig = go.Figure(go.Bar(x=labels, y=values,
                               marker_color=color, marker_line_width=0))
    fig.update_layout(title=title, **plotly_theme())
    return fig

def confusion_matrix_fig(cm, labels=['Low Risk', 'High Risk']):
    z = cm[::-1]
    x_labels = labels
    y_labels = labels[::-1]

    annotations = []
    for i, row in enumerate(z):
        for j, val in enumerate(row):
            annotations.append(dict(
                x=x_labels[j], y=y_labels[i],
                text=str(val), showarrow=False,
                font=dict(color='white', size=18, family='Syne')
            ))

    fig = go.Figure(go.Heatmap(
        z=z, x=x_labels, y=y_labels,
        colorscale=[[0, '#1A1A2E'], [0.5, '#6B1020'], [1, '#C0152B']],
        showscale=True,
    ))
    fig.update_layout(
        title='Confusion Matrix',
        annotations=annotations,
        **plotly_theme()
    )
    return fig

def risk_gauge(probability):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        number={'suffix': '%', 'font': {'size': 40, 'family': 'Syne', 'color': '#E8E8F0'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#8892A4', 'tickfont': {'color': '#8892A4'}},
            'bar': {'color': '#C0152B'},
            'bgcolor': 'rgba(26,26,46,0.8)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 33], 'color': 'rgba(34,197,94,0.3)'},
                {'range': [33, 66], 'color': 'rgba(245,158,11,0.3)'},
                {'range': [66, 100], 'color': 'rgba(192,21,43,0.3)'},
            ],
            'threshold': {
                'line': {'color': 'white', 'width': 2},
                'thickness': 0.8,
                'value': probability * 100
            }
        },
        title={'text': 'RISK PROBABILITY', 'font': {'size': 14, 'family': 'Syne', 'color': '#8892A4'}}
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(t=30, b=10, l=20, r=20))
    return fig
