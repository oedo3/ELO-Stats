# Import Flask libraries and NBA stats package
from flask import Flask, request, jsonify
from flask_cors import CORS
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd

# Create Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Endpoint to fetch a player’s career stats by full name
@app.route('/api/player-stats')
def player_stats():
    name = request.args.get('name')
    search_result = players.find_players_by_full_name(name)

    if not search_result:
        return jsonify({'error': 'Player not found'}), 404

    player_id = search_result[0]['id']
    player_name = search_result[0]['full_name']
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]

    # Calculate simple ELO using total points, assists, and rebounds
    total_pts = df['PTS'].sum()
    total_ast = df['AST'].sum()
    total_reb = df['REB'].sum() if 'REB' in df.columns else 0
    elo = int(1000 + (total_pts + total_ast + total_reb) * 0.1)

    return jsonify({
        'name': player_name,
        'elo': elo,
        'jersey': '00',  # placeholder
        'stats': df.to_dict(orient='records')
    })

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
