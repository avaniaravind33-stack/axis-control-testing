"""
Axis Bank Control Testing - Web Dashboard Generator
Creates professional audit/compliance analytics dashboard
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

def load_data():
    """Load control testing data"""
    df = pd.read_csv('data/control_testing_transactions.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def create_kpi_metrics(df):
    """Create KPI metrics"""
    return {
        'total_tested': len(df),
        'compliant': len(df[df['Deficiency Class'] == 'None']),
        'exceptions': len(df[df['Deficiency Class'] != 'None']),
        'compliance_rate': (len(df[df['Deficiency Class'] == 'None']) / len(df) * 100),
        'critical': len(df[df['Deficiency Class'] == 'Critical']),
        'major': len(df[df['Deficiency Class'] == 'Major']),
        'minor': len(df[df['Deficiency Class'] == 'Minor']),
        'c001_pass': len(df[df['C001_Maker_Checker'] == 'Pass']),
        'c002_pass': len(df[df['C002_Auth_Limit'] == 'Pass']),
        'c003_pass': len(df[df['C003_SOD'] == 'Pass']),
        'c004_pass': len(df[df['C004_4Eyes'] == 'Pass']),
        'c005_pass': len(df[df['C005_Duplicate'] == 'Pass']),
    }

def create_deficiency_breakdown(df):
    """Create deficiency breakdown chart"""
    deficiency_data = df['Deficiency Class'].value_counts()
    colors = {'Critical': '#C00000', 'Major': '#FFC000', 'Minor': '#70AD47', 'None': '#1F4E78'}

    fig = go.Figure(data=[
        go.Bar(
            x=[d for d in deficiency_data.index if d in colors],
            y=[deficiency_data[d] for d in deficiency_data.index if d in colors],
            marker=dict(color=[colors[d] for d in deficiency_data.index if d in colors]),
            text=[deficiency_data[d] for d in deficiency_data.index if d in colors],
            textposition='auto',
        )
    ])
    fig.update_layout(
        title="Deficiency Classification Breakdown",
        xaxis_title="Deficiency Class",
        yaxis_title="Number of Exceptions",
        height=400,
        showlegend=False,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#1e293b',
        font=dict(color='#e2e8f0'),
    )
    return fig

def create_control_effectiveness(df):
    """Create control-wise effectiveness"""
    controls = {
        'C001\nMaker/Checker': len(df[df['C001_Maker_Checker'] == 'Pass']),
        'C002\nAuth Limit': len(df[df['C002_Auth_Limit'] == 'Pass']),
        'C003\nSOD': len(df[df['C003_SOD'] == 'Pass']),
        'C004\n4-Eyes': len(df[df['C004_4Eyes'] == 'Pass']),
        'C005\nDuplicate': len(df[df['C005_Duplicate'] == 'Pass']),
    }

    effectiveness = {k: (v / len(df) * 100) for k, v in controls.items()}

    fig = go.Figure(data=[
        go.Bar(
            x=list(effectiveness.keys()),
            y=list(effectiveness.values()),
            marker=dict(color=['#1F4E78' if v > 99 else '#FFC000' if v > 95 else '#C00000' for v in effectiveness.values()]),
            text=[f'{v:.1f}%' for v in effectiveness.values()],
            textposition='auto',
        )
    ])
    fig.update_layout(
        title="Control Operating Effectiveness (%)",
        xaxis_title="Control",
        yaxis_title="Effectiveness %",
        height=400,
        showlegend=False,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#1e293b',
        font=dict(color='#e2e8f0'),
    )
    return fig

def create_transaction_volume_trend(df):
    """Create transaction volume trend"""
    daily_volume = df.groupby(df['Date'].dt.date).size()

    fig = go.Figure(data=[
        go.Scatter(
            x=daily_volume.index,
            y=daily_volume.values,
            mode='lines+markers',
            line=dict(color='#1F4E78', width=2),
            fill='tozeroy',
            hovertemplate='<b>%{x}</b><br>Transactions: %{y}<extra></extra>'
        )
    ])
    fig.update_layout(
        title="Daily Transaction Volume Trend",
        xaxis_title="Date",
        yaxis_title="Transactions",
        height=400,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#1e293b',
        font=dict(color='#e2e8f0'),
    )
    return fig

def create_exception_trend(df):
    """Create exception trend"""
    daily_exceptions = df[df['Deficiency Class'] != 'None'].groupby(df['Date'].dt.date).size()

    fig = go.Figure(data=[
        go.Scatter(
            x=daily_exceptions.index,
            y=daily_exceptions.values,
            mode='lines+markers',
            line=dict(color='#C00000', width=2),
            fill='tozeroy',
            hovertemplate='<b>%{x}</b><br>Exceptions: %{y}<extra></extra>'
        )
    ])
    fig.update_layout(
        title="Daily Exception Trend",
        xaxis_title="Date",
        yaxis_title="Exceptions",
        height=400,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#1e293b',
        font=dict(color='#e2e8f0'),
    )
    return fig

def create_exception_by_txn_type(df):
    """Create exceptions by transaction type"""
    exc_by_type = df[df['Deficiency Class'] != 'None']['Transaction Type'].value_counts()

    fig = go.Figure(data=[
        go.Bar(
            x=exc_by_type.values,
            y=exc_by_type.index,
            orientation='h',
            marker=dict(color='#FFC000'),
            text=exc_by_type.values,
            textposition='auto',
        )
    ])
    fig.update_layout(
        title="Exceptions by Transaction Type",
        xaxis_title="Count",
        yaxis_title="Transaction Type",
        height=400,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#1e293b',
        font=dict(color='#e2e8f0'),
    )
    return fig

def create_risk_heatmap(df):
    """Create risk heat map by control and deficiency"""
    controls = ['C001_Maker_Checker', 'C002_Auth_Limit', 'C003_SOD', 'C004_4Eyes', 'C005_Duplicate']
    risk_data = []

    for control in controls:
        critical = len(df[(df[control] != 'Pass') & (df['Deficiency Class'] == 'Critical')])
        major = len(df[(df[control] != 'Pass') & (df['Deficiency Class'] == 'Major')])
        minor = len(df[(df[control] != 'Pass') & (df['Deficiency Class'] == 'Minor')])
        risk_data.append([critical, major, minor])

    fig = go.Figure(data=go.Heatmap(
        z=risk_data,
        x=['Critical', 'Major', 'Minor'],
        y=['C001', 'C002', 'C003', 'C004', 'C005'],
        colorscale='Reds',
        text=risk_data,
        texttemplate='%{text}',
        textfont={"size": 12},
    ))
    fig.update_layout(
        title="Risk Heat Map: Control vs Deficiency Class",
        height=400,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#1e293b',
        font=dict(color='#e2e8f0'),
    )
    return fig

def generate_html_dashboard(df, kpis, charts):
    """Generate complete HTML dashboard with embedded charts"""

    # Convert charts to JSON for embedding
    chart_json = {}
    for name, fig in charts.items():
        chart_json[name] = fig.to_json()

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Axis Bank Control Testing Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
                min-height: 100vh;
                padding: 40px 20px;
                color: #e2e8f0;
            }}

            .container {{
                max-width: 1800px;
                margin: 0 auto;
            }}

            .header {{
                background: linear-gradient(135deg, #1F4E78 0%, #2d5a96 50%, #1F4E78 100%);
                color: white;
                padding: 50px 40px;
                border-radius: 16px;
                margin-bottom: 50px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 80px rgba(31, 78, 120, 0.3);
                position: relative;
                overflow: hidden;
                border: 1px solid rgba(255,255,255,0.1);
            }}

            .header::before {{
                content: '';
                position: absolute;
                top: -50%;
                right: -10%;
                width: 600px;
                height: 600px;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                border-radius: 50%;
            }}

            .header h1 {{
                font-size: 3.5em;
                margin-bottom: 15px;
                font-weight: 800;
                position: relative;
                z-index: 1;
                letter-spacing: -1px;
            }}

            .header p {{
                font-size: 1.3em;
                opacity: 0.95;
                position: relative;
                z-index: 1;
                font-weight: 300;
            }}

            .reporting-date {{
                font-size: 0.95em;
                opacity: 0.85;
                margin-top: 20px;
                position: relative;
                z-index: 1;
            }}

            .kpi-section {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 25px;
                margin-bottom: 50px;
            }}

            .kpi-card {{
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                padding: 30px;
                border-radius: 12px;
                border: 1px solid #334155;
                text-align: center;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }}

            .kpi-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
                transition: left 0.5s;
            }}

            .kpi-card:hover {{
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 20px 50px rgba(31, 78, 120, 0.3);
                border-color: #3b82f6;
            }}

            .kpi-label {{
                font-size: 0.85em;
                color: #94a3b8;
                margin-bottom: 12px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1.5px;
            }}

            .kpi-value {{
                font-size: 2.5em;
                font-weight: 800;
                color: #1F4E78;
                margin-bottom: 5px;
            }}

            .kpi-value.critical {{
                color: #C00000;
            }}

            .kpi-value.warning {{
                color: #FFC000;
            }}

            .kpi-value.success {{
                color: #70AD47;
            }}

            .charts-section {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 35px;
                margin-bottom: 50px;
            }}

            .chart-container {{
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                padding: 30px;
                border-radius: 12px;
                border: 1px solid #334155;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                transition: all 0.3s ease;
            }}

            .chart-container:hover {{
                border-color: #1F4E78;
                box-shadow: 0 20px 50px rgba(31, 78, 120, 0.3);
            }}

            .full-width {{
                grid-column: 1 / -1;
            }}

            footer {{
                text-align: center;
                color: #94a3b8;
                margin-top: 60px;
                padding: 30px;
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                border-radius: 12px;
                border: 1px solid #334155;
                font-size: 0.95em;
            }}

            footer p {{
                margin: 8px 0;
            }}

            @media (max-width: 768px) {{
                .header {{
                    padding: 40px 20px;
                }}

                .header h1 {{
                    font-size: 2em;
                }}

                .charts-section {{
                    grid-template-columns: 1fr;
                    gap: 25px;
                }}

                .kpi-section {{
                    grid-template-columns: repeat(2, 1fr);
                    gap: 15px;
                }}

                .kpi-card {{
                    padding: 20px;
                }}

                .kpi-value {{
                    font-size: 1.8em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏦 Axis Bank Control Testing Dashboard</h1>
                <p>Internal Audit & Compliance Testing Analysis</p>
                <div class="reporting-date">Testing Period: Jan 2024 - Dec 2024 | Report Generated: {datetime.now().strftime('%B %d, %Y')}</div>
            </div>

            <div class="kpi-section">
                <div class="kpi-card">
                    <div class="kpi-label">Total Transactions Tested</div>
                    <div class="kpi-value">{kpis['total_tested']:,}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Compliant Transactions</div>
                    <div class="kpi-value success">{kpis['compliant']:,}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Compliance Rate</div>
                    <div class="kpi-value success">{kpis['compliance_rate']:.2f}%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Total Exceptions</div>
                    <div class="kpi-value warning">{kpis['exceptions']:,}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Critical Deficiencies</div>
                    <div class="kpi-value critical">{kpis['critical']}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Major Deficiencies</div>
                    <div class="kpi-value warning">{kpis['major']}</div>
                </div>
            </div>

            <div class="charts-section">
                <div class="chart-container">
                    <div id="deficiency-chart"></div>
                </div>
                <div class="chart-container">
                    <div id="control-effectiveness"></div>
                </div>
                <div class="chart-container full-width">
                    <div id="risk-heatmap"></div>
                </div>
                <div class="chart-container">
                    <div id="volume-trend"></div>
                </div>
                <div class="chart-container">
                    <div id="exception-trend"></div>
                </div>
                <div class="chart-container">
                    <div id="exception-by-type"></div>
                </div>
            </div>

            <footer>
                <p><strong>Axis Bank Internal Audit & Compliance</strong></p>
                <p>Control Testing & Effectiveness Assessment Dashboard</p>
                <p>Professional Control Testing Simulation for Audit & Compliance Functions</p>
            </footer>
        </div>

        <script>
            var chartsData = {chart_json};

            // Render each chart
            Plotly.newPlot('deficiency-chart', chartsData['deficiency'].data, chartsData['deficiency'].layout, {{responsive: true}});
            Plotly.newPlot('control-effectiveness', chartsData['effectiveness'].data, chartsData['effectiveness'].layout, {{responsive: true}});
            Plotly.newPlot('risk-heatmap', chartsData['risk_heatmap'].data, chartsData['risk_heatmap'].layout, {{responsive: true}});
            Plotly.newPlot('volume-trend', chartsData['volume_trend'].data, chartsData['volume_trend'].layout, {{responsive: true}});
            Plotly.newPlot('exception-trend', chartsData['exception_trend'].data, chartsData['exception_trend'].layout, {{responsive: true}});
            Plotly.newPlot('exception-by-type', chartsData['exception_type'].data, chartsData['exception_type'].layout, {{responsive: true}});
        </script>
    </body>
    </html>
    """

    return html_content

def main():
    print("Loading data...")
    df = load_data()

    print("Computing KPIs...")
    kpis = create_kpi_metrics(df)

    print("Creating charts...")
    charts = {
        'deficiency': create_deficiency_breakdown(df),
        'effectiveness': create_control_effectiveness(df),
        'volume_trend': create_transaction_volume_trend(df),
        'exception_trend': create_exception_trend(df),
        'exception_type': create_exception_by_txn_type(df),
        'risk_heatmap': create_risk_heatmap(df),
    }

    print("Generating HTML...")
    html = generate_html_dashboard(df, kpis, charts)

    # Save
    output_path = 'website/index.html'
    with open(output_path, 'w') as f:
        f.write(html)

    print(f"✓ Dashboard saved to {output_path}")

if __name__ == '__main__':
    main()
