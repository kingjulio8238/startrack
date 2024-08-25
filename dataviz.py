import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

csv_file_path = 'sample_data.csv'
df = pd.read_csv(csv_file_path)

#Create contact table 
def create_contact_table(df):
    fig = go.Figure(data=[go.Table(
        header=dict(values=['<b>Email</b>', '<b>Twitter</b>', '<b>LinkedIn</b>'],
                    fill_color='#4A90E2',
                    align='center',
                    font=dict(color='white', size=12)),
        cells=dict(values=[
            [f'<a href="mailto:{email}">{email}</a>' for email in df.Email],
            [f'{url}' for url in df.Twitter],
            [f'{url}' for url in df.LinkedIn]
        ],
        fill_color=['white', 'white'],
        align='left',
        font=dict(color='#333', size=11)))
    ])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=400, width=800)
    return fig


#Create map 
def create_location_map(df):
    fig = px.scatter_geo(df, locations='Location', locationmode='country names', 
                         hover_name='Email', projection='natural earth',
                         color_discrete_sequence=['#4A90E2'])
    fig.update_geos(showcoastlines=True, coastlinecolor="RebeccaPurple", 
                    showland=True, landcolor="LightGreen",
                    showocean=True, oceancolor="LightBlue",
                    showlakes=True, lakecolor="Blue",
                    showrivers=True, rivercolor="Blue")
    fig.update_layout(height=400, width=600, margin=dict(l=0, r=0, t=0, b=50))
    return fig

# Create a combined figure
combined_fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4], 
                             specs=[[{"type": "table"}, {"type": "scattergeo"}]],
                             horizontal_spacing=0.02)

# Add contact table to the left subplot
contact_table = create_contact_table(df)
combined_fig.add_trace(contact_table.data[0], row=1, col=1)

# Add location map to the right subplot
location_map = create_location_map(df)
combined_fig.add_trace(location_map.data[0], row=1, col=2)

# Update layout for better aesthetics
combined_fig.update_layout(
    height=500,
    width=1400,
    showlegend=False,
    margin=dict(t=200, b=100, l=100, r=20),  # Increased left margin to move content right
    paper_bgcolor='white',
    plot_bgcolor='white'
)
# Add annotations for titles
combined_fig.add_annotation(
    x=0.25, y=-0.15,  # Adjusted x position for centering
    text="<b>Contact Info</b>", 
    showarrow=False, 
    xref="paper", yref="paper", 
    font=dict(size=14),
    align='center'
)
combined_fig.add_annotation(
    x=0.85, y=-0.15,  # Adjusted x position for centering
    text="<b>Global Stars</b>", 
    showarrow=False, 
    xref="paper", yref="paper", 
    font=dict(size=14),
    align='center'
)

# Update geo subplot properties
combined_fig.update_geos(projection_type="natural earth")

# Get the plot's div and script
plot_div = combined_fig.to_html(full_html=False, include_plotlyjs='cdn', config={'responsive': True})

#HTML template
custom_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Information and User Locations</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: white;
        }}
        .container {{
            width: 100%;
            max-width: 1400px;
            padding: 20px;
            box-sizing: border-box;
        }}
        .js-plotly-plot .plotly .modebar {{
            display: none !important;
        }}
        .js-plotly-plot .plotly .table-cell a {{
            color: #4A90E2;
            text-decoration: none;
        }}
        .js-plotly-plot .plotly .table-cell a:hover {{
            text-decoration: underline;
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }}
        .input-container {{
            text-align: center;
            margin-bottom: 20px;
        }}
        input[type="text"] {{
            width: 300px;
            padding: 10px;
            font-size: 16px;
        }}
        .visualization-container {{
            display: flex;
            justify-content: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Track your repo star gazers 👀</h1>
        <div class="input-container">
            <input type="text" placeholder="Search repo...">
        </div>
        <div class="visualization-container">
            {plot_div}
        </div>
    </div>
</body>
</html
"""

# Ensure links are clickable
config = {'displayModeBar': False}
plot_div = combined_fig.to_html(full_html=False, include_plotlyjs='cdn', config=config)

# Write the custom HTML to a file
with open("combined_visualization.html", "w") as f:
    f.write(custom_html)

#success message 
print("Combined visualization saved as combined_visualization.html")

# Optionally, display the combined figure
combined_fig.show()
