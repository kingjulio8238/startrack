import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

csv_file_path = 'sample_contact_data.csv'
df = pd.read_csv(csv_file_path)

# Create contact table visualization
def create_contact_table(df):
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Email', 'Twitter', 'LinkedIn'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.Email, df.Twitter, df.LinkedIn],
                   fill_color='lavender',
                   align='left'))
    ])
    fig.update_layout(title='Contact Information')
    return fig

contact_table = create_contact_table(df)
contact_table.show()

def create_location_map(df):
    fig = px.scatter_geo(df, locations='Location', locationmode='country names', 
                         hover_name='Email', projection='natural earth')
    fig.update_layout(title='User Locations')
    return fig

location_map = create_location_map(df)
location_map.show()

contact_table.write_html("contact_table.html")
location_map.write_html("location_map.html")
print("Visualizations saved as HTML files")