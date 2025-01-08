from dash import html, dcc


def create_about_me_page():
    return html.Div([
        # Main container
        html.Div([
            # Profile Header Card
            html.Div([
                html.Div([
                    # Left side - Name and Status
                    html.Div([
                        html.H1('Alexander Matthew, CFA',
                                className='profile-name'),
                        html.P('Manager, Investment Strategies',
                               className='profile-title'),
                        html.Div([
                            html.Div(className='status-dot'),
                            html.Span('Active', className='status-text')
                        ], className='status-container')
                    ], className='profile-info'),

                    # Right side - Avatar
                    html.Div('AM', className='profile-avatar')
                ], className='profile-header-content')
            ], className='modern-card profile-card'),

            # Main Grid
            html.Div([
                # Education Section
                html.Div([
                    html.Div([
                        html.I(className='fas fa-graduation-cap section-icon'),
                        html.H2('Education', className='section-title')
                    ], className='section-header'),
                    html.Div([
                        html.H3('University of North Carolina at Chapel Hill',
                                className='education-school'),
                        html.P('B.S. Mathematical Decision Sciences (Statistics)',
                               className='education-degree')
                    ], className='education-content')
                ], className='modern-card'),

                # Skills Section
                html.Div([
                    html.Div([
                        html.I(className='fas fa-code section-icon'),
                        html.H2('Technical Proficiencies', className='section-title')
                    ], className='section-header'),
                    html.Div([
                        html.Span(skill, className='skill-tag')
                        for skill in ['Python', 'MATLAB', 'Derivatives', 'Portfolio Management']
                    ], className='skills-container')
                ], className='modern-card'),


                html.Div([
                    html.Div([
                        html.I(className='fas fa-target section-icon'),
                        html.H2('Mission Statement', className='section-title')
                    ], className='section-header'),
                    html.P('''[Your professional summary and mission statement here. 
                          Describe your journey, passions, and what drives you in your field.]''',
                           className='mission-text')
                ], className='modern-card full-width')
            ], className='main-grid')
        ], className='content-container')
    ], className='modern-page')