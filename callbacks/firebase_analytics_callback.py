from dash.dependencies import Input, Output
from dash import html, ctx
from dash.exceptions import PreventUpdate

from functions import get_fixtures_from_DB
from functions.player_statistics_functions import analyze_data_quality, analyze_team_statistics, create_data_quality_report, create_player_statistics, create_player_statistics_table, create_team_analysis_report


def setup_firebase_analysis_callbacks(app, db):
    @app.callback(
       [Output('data-quality-container', 'children'),
        Output('player-stats-container', 'children'),
        Output('team-stats-container', 'children'),
        Output('cache-info', 'children')], 
       [Input('analyze-data-button', 'n_clicks'),
        Input('force-refresh-button', 'n_clicks')],
       prevent_initial_call=True
   )
    def update_analysis(n_clicks, refresh_clicks):
       if not n_clicks and not refresh_clicks:
           raise PreventUpdate
       
       print("Starting Firebase data fetch...")
       
       # Check if db connection exists
       if not db:
           print("No Firebase connection!")
           return ["No Firebase connection"] * 4
           
       # Try to get collection reference
       fixtures_ref = db.collection('fixtures')
       if not fixtures_ref:
           print("Cannot access fixtures collection!")
           return ["Cannot access fixtures collection"] * 4
       
       try:
    
              # Get fixtures using cache
           fixtures_data = get_fixtures_from_DB(db)
           print(f"Retrieved {len(fixtures_data)} fixtures")

           if not fixtures_data:
               print("No fixtures data found!")
               return ["No fixtures data found in database"] * 4
           
           # Process data quality
           quality_stats = analyze_data_quality(fixtures_data)
           quality_report = create_data_quality_report(quality_stats)
           
           # Process player statistics
           player_stats = create_player_statistics(fixtures_data)
           player_table = create_player_statistics_table(player_stats)
           
           # Process team statistics
           team_stats, team_quality = analyze_team_statistics(fixtures_data)
           team_report = create_team_analysis_report(team_stats, team_quality)
           
           return quality_report, player_table, team_report
           
       except Exception as e:
           print(f"Error in analysis: {e}")
           return (
               html.Div(f"Error: {str(e)}"),
               html.Div("Error loading player stats"),
               html.Div("Error loading team stats"),
               html.Div("Error getting cache info")
           )
