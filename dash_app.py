import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)

# Load data
df = pd.read_csv('netflix_data.csv')

# App layout
app.layout = html.Div([
    html.H1('Netflix Content Analysis Dashboard'),
    html.Label('Select Genre:'),
    dcc.Dropdown(
        id='genre-filter',
        options=[{'label': g, 'value': g} for g in df['Genre'].unique() if g],
        value=df['Genre'].iloc[0]
    ),
    dcc.Graph(id='ratings-plot')
])

# Callback to update plot based on genre
@app.callback(
    Output('ratings-plot', 'figure'),
    [Input('genre-filter', 'value')]
)
def update_graph(selected_genre):
    filtered_df = df[df['Genre'] == selected_genre]
    fig = px.histogram(
        filtered_df,
        x='Viewer_Rating',
        title=f'Viewer Ratings Distribution for {selected_genre}',
        labels={'Viewer_Rating': 'Viewer Rating (1-10)'}
    )
    fig.update_layout(xaxis_title='Viewer Rating (1-10)', yaxis_title='Count')
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)