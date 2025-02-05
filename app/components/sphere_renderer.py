from dash import html, dcc
import numpy as np
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from scipy.spatial.transform import Rotation


def generate_sphere_points(num_slices=30, num_points=100):
    heights, angles = np.meshgrid(
        1 - (2 * np.linspace(0, 1, num_slices)),
        2 * np.pi * np.linspace(0, 1, num_points),
        indexing='ij'
    )
    circle_radii = np.sqrt(1 - heights ** 2)
    x = circle_radii * np.cos(angles)
    y = heights
    z = circle_radii * np.sin(angles)
    return np.stack([x, y, z], axis=-1)


def create_sphere_traces(base_points, rotation):
    rotated = Rotation.from_euler('xyz', rotation).apply(base_points)
    return [
        go.Scatter3d(
            x=slice_points[:, 0],
            y=slice_points[:, 1],
            z=slice_points[:, 2],
            mode='lines',
            line=dict(color='white', width=2),
            showlegend=False
        )
        for slice_points in rotated
    ]


def create_sphere_component(app=None):
    base_points = generate_sphere_points()

    layout = html.Div([
        dcc.Graph(
            id='sphere-graph',
            style={'height': '600px', 'backgroundColor': 'black'},
            config={'displayModeBar': False}
        ),
        dcc.Store(id='rotation-state', data={'x': 0, 'y': 0, 'z': 0}),
        dcc.Interval(
            id='animation-interval',
            interval=50,
            n_intervals=0
        ),
        html.Div([
            dcc.Checklist(
                id='auto-rotate',
                options=[{'label': 'Auto Rotate', 'value': 'enabled'}],
                value=['enabled'],
                className='mb-3'
            ),
            html.Div([
                html.Label('X Rotation Speed', className='text-white'),
                dcc.Slider(
                    id='x-speed',
                    min=-2, max=2, step=0.1,
                    value=0.5,
                    marks={i: str(i) for i in range(-2, 3)}
                )
            ], className='mb-3'),
            html.Div([
                html.Label('Y Rotation Speed', className='text-white'),
                dcc.Slider(
                    id='y-speed',
                    min=-2, max=2, step=0.1,
                    value=1.0,
                    marks={i: str(i) for i in range(-2, 3)}
                )
            ], className='mb-3'),
            html.Div([
                html.Label('Z Rotation Speed', className='text-white'),
                dcc.Slider(
                    id='z-speed',
                    min=-2, max=2, step=0.1,
                    value=0.3,
                    marks={i: str(i) for i in range(-2, 3)}
                )
            ])
        ], className='w-96 mx-auto p-4')
    ], className='container mx-auto py-4')

    if app is not None:
        @app.callback(
            Output('rotation-state', 'data'),
            Input('animation-interval', 'n_intervals'),
            Input('auto-rotate', 'value'),
            Input('x-speed', 'value'),
            Input('y-speed', 'value'),
            Input('z-speed', 'value'),
            State('rotation-state', 'data')
        )
        def update_rotation(n, auto_rotate, x_speed, y_speed, z_speed, rotation):
            if not auto_rotate:
                return rotation

            dt = 0.05
            return {
                'x': rotation['x'] + x_speed * dt,
                'y': rotation['y'] + y_speed * dt,
                'z': rotation['z'] + z_speed * dt
            }

        @app.callback(
            Output('sphere-graph', 'figure'),
            Input('rotation-state', 'data')
        )
        def update_graph(rotation):
            traces = create_sphere_traces(base_points, [rotation['x'], rotation['y'], rotation['z']])

            return {
                'data': traces,
                'layout': {
                    'template': 'plotly_dark',
                    'paper_bgcolor': 'rgba(0,0,0,0)',
                    'plot_bgcolor': 'rgba(0,0,0,0)',
                    'scene': {
                        'camera': {
                            'eye': {'x': 0, 'y': 0, 'z': 2.5}
                        },
                        'aspectmode': 'cube',
                        'xaxis': {'showgrid': False, 'zeroline': False, 'visible': False},
                        'yaxis': {'showgrid': False, 'zeroline': False, 'visible': False},
                        'zaxis': {'showgrid': False, 'zeroline': False, 'visible': False},
                        'bgcolor': 'rgba(0,0,0,0)'
                    },
                    'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0},
                    'uirevision': True
                }
            }

    return layout