"""
Axis Bank Control Testing - Web Dashboard Generator
Creates professional audit/compliance analytics dashboard with chart explanations
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
    }

def create_charts(df):
    """Create all charts"""
    charts = {}

    # Chart 1: Deficiency Classification
    deficiency_data = df['Deficiency Class'].value_counts()
    colors = {'Critical': '#C00000', 'Major': '#FFC000', 'Minor': '#70AD47', 'None': '#1F4E78'}

    x_vals = [d for d in deficiency_data.index if d != 'None']
    y_vals = [int(deficiency_data[d]) for d in deficiency_data.index if d != 'None']
    color_vals = [colors.get(d, '#666') for d in deficiency_data.index if d != 'None']

    charts['deficiency'] = {
        'x': x_vals,
        'y': y_vals,
        'colors': color_vals,
        'title': 'Deficiency Classification Breakdown',
        'description': 'Shows the distribution of control exceptions by severity level. Critical deficiencies represent failures of primary control objectives. Major deficiencies are significant deviations from control design. Minor deficiencies are isolated instances with minimal impact.'
    }

    # Chart 2: Control Effectiveness
    controls = ['C001\nMaker/Checker', 'C002\nAuth Limit', 'C003\nSOD', 'C004\n4-Eyes', 'C005\nDuplicate']
    pass_rates = [
        float(len(df[df['C001_Maker_Checker'] == 'Pass']) / len(df) * 100),
        float(len(df[df['C002_Auth_Limit'] == 'Pass']) / len(df) * 100),
        float(len(df[df['C003_SOD'] == 'Pass']) / len(df) * 100),
        float(len(df[df['C004_4Eyes'] == 'Pass']) / len(df) * 100),
        float(len(df[df['C005_Duplicate'] == 'Pass']) / len(df) * 100),
    ]

    charts['effectiveness'] = {
        'x': controls,
        'y': pass_rates,
        'colors': ['#1F4E78' if v > 99 else '#FFC000' if v > 95 else '#C00000' for v in pass_rates],
        'title': 'Control Operating Effectiveness (%)',
        'description': 'Operating effectiveness measures whether each control actually operated as designed throughout the testing period. Higher percentages indicate controls performed consistently. This metric validates that design intent translated to actual execution.'
    }

    # Chart 3: Risk Heat Map
    controls_list = ['C001', 'C002', 'C003', 'C004', 'C005']
    risk_data = []
    for control_col in ['C001_Maker_Checker', 'C002_Auth_Limit', 'C003_SOD', 'C004_4Eyes', 'C005_Duplicate']:
        critical = int(len(df[(df[control_col] != 'Pass') & (df['Deficiency Class'] == 'Critical')]))
        major = int(len(df[(df[control_col] != 'Pass') & (df['Deficiency Class'] == 'Major')]))
        minor = int(len(df[(df[control_col] != 'Pass') & (df['Deficiency Class'] == 'Minor')]))
        risk_data.append([critical, major, minor])

    charts['heatmap'] = {
        'z': risk_data,
        'x': ['Critical', 'Major', 'Minor'],
        'y': controls_list,
        'title': 'Risk Heat Map: Control vs Deficiency Class',
        'description': 'This heat map visualizes the intersection of control failures and deficiency severity. Darker red cells indicate higher concentration of critical failures. It helps prioritize remediation efforts by identifying which controls have the most severe impacts.'
    }

    # Chart 4: Transaction Volume
    daily_volume = df.groupby(df['Date'].dt.date).size()
    charts['volume'] = {
        'x': [str(d) for d in daily_volume.index],
        'y': [int(v) for v in daily_volume.values],
        'title': 'Daily Transaction Volume Trend',
        'description': 'Shows transaction processing volume over the testing period. Consistent volume indicates steady-state operations. Spikes may indicate month-end or special processing periods where control failures are more likely.'
    }

    # Chart 5: Exception Trend
    daily_exceptions = df[df['Deficiency Class'] != 'None'].groupby(df['Date'].dt.date).size()
    charts['exceptions'] = {
        'x': [str(d) for d in daily_exceptions.index],
        'y': [int(v) for v in daily_exceptions.values],
        'title': 'Daily Exception Trend',
        'description': 'Tracks the number of control exceptions (failures) detected daily. This trend reveals whether control breakdowns are clustered (systemic issue) or scattered (isolated incidents). Consistent low-level exceptions suggest design weaknesses; sudden spikes suggest operational failures.'
    }

    # Chart 6: Exceptions by Type
    exc_by_type = df[df['Deficiency Class'] != 'None']['Transaction Type'].value_counts()
    charts['by_type'] = {
        'x': [int(v) for v in exc_by_type.values],
        'y': list(exc_by_type.index),
        'title': 'Exceptions by Transaction Type',
        'description': 'Identifies which transaction types are most prone to control failures. This helps determine if certain processes need stronger controls or additional training. For example, if remittances have more exceptions than sweeps, remediation can be targeted accordingly.'
    }

    return charts

def generate_html_dashboard(df, kpis, charts):
    """Generate HTML with explanatory text"""

    chart_explanations = {
        'deficiency': charts['deficiency']['description'],
        'effectiveness': charts['effectiveness']['description'],
        'heatmap': charts['heatmap']['description'],
        'volume': charts['volume']['description'],
        'exceptions': charts['exceptions']['description'],
        'by_type': charts['by_type']['description'],
    }

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
            }}

            .header p {{
                font-size: 1.3em;
                opacity: 0.95;
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
                transition: all 0.3s;
            }}

            .kpi-card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 20px 50px rgba(31, 78, 120, 0.3);
            }}

            .kpi-label {{
                font-size: 0.85em;
                color: #94a3b8;
                margin-bottom: 12px;
                font-weight: 600;
                text-transform: uppercase;
            }}

            .kpi-value {{
                font-size: 2.5em;
                font-weight: 800;
                color: #1F4E78;
            }}

            .kpi-value.success {{
                color: #70AD47;
            }}

            .kpi-value.warning {{
                color: #FFC000;
            }}

            .kpi-value.critical {{
                color: #C00000;
            }}

            .section-title {{
                font-size: 1.8em;
                font-weight: 700;
                color: #e2e8f0;
                margin: 50px 0 30px 0;
                padding: 20px;
                border-left: 4px solid #1F4E78;
            }}

            .chart-with-explanation {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 50px;
            }}

            .chart-container {{
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                padding: 30px;
                border-radius: 12px;
                border: 1px solid #334155;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}

            .explanation {{
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                padding: 30px;
                border-radius: 12px;
                border: 1px solid #334155;
                border-left: 4px solid #1F4E78;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }}

            .explanation h3 {{
                font-size: 1.2em;
                margin-bottom: 15px;
                color: #1F4E78;
            }}

            .explanation p {{
                font-size: 1em;
                line-height: 1.6;
                color: #cbd5e1;
            }}

            .full-width {{
                grid-column: 1 / -1;
            }}

            footer {{
                text-align: center;
                color: #94a3b8;
                margin-top: 60px;
                padding: 30px;
                border-top: 1px solid #334155;
            }}

            @media (max-width: 1024px) {{
                .chart-with-explanation {{
                    grid-template-columns: 1fr;
                }}

                .header h1 {{
                    font-size: 2em;
                }}

                .kpi-section {{
                    grid-template-columns: repeat(2, 1fr);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏦 Axis Bank Control Testing Dashboard</h1>
                <p>Internal Audit & Compliance Testing Analysis</p>
                <div style="margin-top: 20px; opacity: 0.9;">Testing Period: Jan 2024 - Dec 2024 | Report Generated: {datetime.now().strftime('%B %d, %Y')}</div>
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

            <div class="section-title">📊 Control Testing Analysis</div>

            <div class="chart-with-explanation">
                <div class="chart-container">
                    <div id="deficiency-chart" style="height: 400px;"></div>
                </div>
                <div class="explanation">
                    <h3>Deficiency Classification</h3>
                    <p>{chart_explanations['deficiency']}</p>
                </div>
            </div>

            <div class="chart-with-explanation">
                <div class="explanation">
                    <h3>Control Operating Effectiveness</h3>
                    <p>{chart_explanations['effectiveness']}</p>
                </div>
                <div class="chart-container">
                    <div id="control-effectiveness" style="height: 400px;"></div>
                </div>
            </div>

            <div class="chart-with-explanation full-width">
                <div class="chart-container full-width">
                    <div id="risk-heatmap" style="height: 400px;"></div>
                </div>
            </div>
            <div class="explanation full-width">
                <h3>Risk Heat Map Explanation</h3>
                <p>{chart_explanations['heatmap']}</p>
            </div>

            <div class="chart-with-explanation">
                <div class="chart-container">
                    <div id="volume-trend" style="height: 400px;"></div>
                </div>
                <div class="explanation">
                    <h3>Transaction Volume Analysis</h3>
                    <p>{chart_explanations['volume']}</p>
                </div>
            </div>

            <div class="chart-with-explanation">
                <div class="explanation">
                    <h3>Exception Trends</h3>
                    <p>{chart_explanations['exceptions']}</p>
                </div>
                <div class="chart-container">
                    <div id="exception-trend" style="height: 400px;"></div>
                </div>
            </div>

            <div class="chart-with-explanation">
                <div class="chart-container">
                    <div id="exception-by-type" style="height: 400px;"></div>
                </div>
                <div class="explanation">
                    <h3>Transaction Type Analysis</h3>
                    <p>{chart_explanations['by_type']}</p>
                </div>
            </div>

            <footer>
                <p><strong>Axis Bank Internal Audit & Compliance</strong></p>
                <p>Control Testing & Effectiveness Assessment Dashboard</p>
            </footer>
        </div>

        <script>
            // Chart 1: Deficiency Breakdown
            var deficiency_data = {{
                x: {json.dumps(charts['deficiency']['x'])},
                y: {json.dumps(charts['deficiency']['y'])},
                type: 'bar',
                marker: {{color: {json.dumps(charts['deficiency']['colors'])}}}
            }};
            Plotly.newPlot('deficiency-chart', [deficiency_data], {{'title': 'Deficiency Classification Breakdown', 'xaxis': {{'title': 'Deficiency Class'}}, 'yaxis': {{'title': 'Count'}}, 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}}, {{responsive: true}});

            // Chart 2: Control Effectiveness
            var effectiveness_data = {{
                x: {json.dumps(charts['effectiveness']['x'])},
                y: {json.dumps(charts['effectiveness']['y'])},
                type: 'bar',
                marker: {{color: {json.dumps(charts['effectiveness']['colors'])}}}
            }};
            Plotly.newPlot('control-effectiveness', [effectiveness_data], {{'title': 'Control Operating Effectiveness (%)', 'xaxis': {{'title': 'Control'}}, 'yaxis': {{'title': 'Effectiveness %'}}, 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}}, {{responsive: true}});

            // Chart 3: Heat Map
            var heatmap_data = {{
                z: {json.dumps(charts['heatmap']['z'])},
                x: {json.dumps(charts['heatmap']['x'])},
                y: {json.dumps(charts['heatmap']['y'])},
                type: 'heatmap',
                colorscale: 'Reds'
            }};
            Plotly.newPlot('risk-heatmap', [heatmap_data], {{'title': 'Risk Heat Map', 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}}, {{responsive: true}});

            // Chart 4: Volume Trend
            var volume_data = {{
                x: {json.dumps([str(d) for d in charts['volume']['x']])},
                y: {json.dumps(charts['volume']['y'])},
                type: 'scatter',
                mode: 'lines+markers',
                line: {{color: '#1F4E78'}},
                fill: 'tozeroy'
            }};
            Plotly.newPlot('volume-trend', [volume_data], {{'title': 'Daily Transaction Volume', 'xaxis': {{'title': 'Date'}}, 'yaxis': {{'title': 'Transactions'}}, 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}}, {{responsive: true}});

            // Chart 5: Exception Trend
            var exception_data = {{
                x: {json.dumps([str(d) for d in charts['exceptions']['x']])},
                y: {json.dumps(charts['exceptions']['y'])},
                type: 'scatter',
                mode: 'lines+markers',
                line: {{color: '#C00000'}},
                fill: 'tozeroy'
            }};
            Plotly.newPlot('exception-trend', [exception_data], {{'title': 'Daily Exceptions', 'xaxis': {{'title': 'Date'}}, 'yaxis': {{'title': 'Exceptions'}}, 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}}, {{responsive: true}});

            // Chart 6: By Type
            var by_type_data = {{
                x: {json.dumps(charts['by_type']['x'])},
                y: {json.dumps(charts['by_type']['y'])},
                type: 'bar',
                orientation: 'h',
                marker: {{color: '#FFC000'}}
            }};
            Plotly.newPlot('exception-by-type', [by_type_data], {{'title': 'Exceptions by Type', 'xaxis': {{'title': 'Count'}}, 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}}, {{responsive: true}});
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
    charts = create_charts(df)

    print("Generating HTML...")
    html = generate_html_dashboard(df, kpis, charts)

    output_path = 'website/index.html'
    with open(output_path, 'w') as f:
        f.write(html)

    print(f"✓ Dashboard saved to {output_path}")
    print(f"✓ Charts embedded with explanatory text")

if __name__ == '__main__':
    main()
