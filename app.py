from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DATA_FILE = 'data/games.json'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('data', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_games():
    try:
        with open(DATA_FILE, 'r') as f:
            games = json.load(f)
            print(f"DEBUG: Loaded {len(games)} games from file")
            for game in games:
                print(f"DEBUG: Game - {game['title']}")
            return games
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"DEBUG: Error loading games: {e}")
        return []

def save_games(games):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(games, f, indent=2)
        print(f"DEBUG: Saved {len(games)} games to file")
        return True
    except Exception as e:
        print(f"DEBUG: Error saving games: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games')
def games():
    games_list = load_games()
    print(f"DEBUG: Passing {len(games_list)} games to template")
    return render_template('games.html', games=games_list)

@app.route('/games/<game_id>')
def game_detail(game_id):
    games_list = load_games()
    game = next((g for g in games_list if g['id'] == game_id), None)
    if game:
        return render_template('game_detail.html', game=game)
    else:
        flash('Game not found!')
        return redirect(url_for('games'))

@app.route('/create-game', methods=['GET', 'POST'])
def create_game():
    if request.method == 'POST':
        print("DEBUG: Form submitted")
        
        # Get form data
        title = request.form.get('title')
        age_range = request.form.get('age_range')
        setup_difficulty = request.form.get('setup_difficulty')
        play_difficulty = request.form.get('play_difficulty')
        duration = request.form.get('duration')
        fun_rating = request.form.get('fun_rating')
        description = request.form.get('description')
        resources = request.form.get('resources')
        
        print(f"DEBUG: Form data - Title: {title}, Age: {age_range}")
        
        # Handle file upload
        image_filename = 'default.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                image_filename = unique_filename
                print(f"DEBUG: Saved image as {image_filename}")
        
        # Create new game object
        new_game = {
            'id': str(uuid.uuid4()),
            'title': title,
            'image': image_filename,
            'age_range': age_range,
            'setup_difficulty': int(setup_difficulty),
            'play_difficulty': int(play_difficulty),
            'duration': float(duration),
            'fun_rating': int(fun_rating),
            'description': description,
            'resources': resources
        }
        
        print(f"DEBUG: New game created: {new_game['title']}")
        
        # Save to JSON file
        games_list = load_games()
        games_list.append(new_game)
        if save_games(games_list):
            flash('Game created successfully!')
        else:
            flash('Error saving game!')
        
        return redirect(url_for('games'))
    
    return render_template('create_game.html')

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)