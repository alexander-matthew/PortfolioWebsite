# app.py
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = Dash(__name__)
server = app.server  # Needed for Heroku deployment

# Create some sample data
df = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'Sales': [1000, 1200, 900, 1500, 1300, 1700]
})

# Create a bar chart
fig = px.bar(df, x='Month', y='Sales', title='Monthly Sales Dashboard')

# Define the app layout
app.layout = html.Div(children=[
    html.H1(children='Sample Dash Application'),

    html.Div(children='''
        A simple dashboard showing monthly sales data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)