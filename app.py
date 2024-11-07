from datetime import datetime
from PIL import Image
import os
import uuid
from flask import Flask, flash, jsonify, render_template, request, redirect, send_from_directory, url_for, session
import pyodbc
import magic
from werkzeug.utils import secure_filename
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'}

# Configuração da conexão com o SQL Server
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def get_db_connection():
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_HOST};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"
    return pyodbc.connect(conn_str)

def format_time(timestamp):
    now = datetime.now()
    diff = now - timestamp

    minutes = diff.total_seconds() // 60
    hours = diff.total_seconds() // 3600
    days = diff.days
    months = days // 30  # Aproximação de meses com base em 30 dias

    if minutes < 60:
        return f"{int(minutes)}m"
    elif hours < 24:
        return f"{int(hours)}h"
    elif days < 30:
        return f"{int(days)}d"
    else:
        return f"{int(months)}mês" if months == 1 else f"{int(months)}meses"

def allowed_file(filename, filetype, file):
    # Verifica a extensão
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if filetype == 'image':
        allowed_exts = {'png', 'jpg', 'jpeg', 'gif'}
    elif filetype == 'video':
        allowed_exts = {'mp4', 'webm'}
    else:
        return False
    if ext not in allowed_exts:
        return False
    # Verifica o mime type
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)  # Reseta o cursor do arquivo
    if filetype == 'image' and mime.startswith('image/'):
        return True
    elif filetype == 'video' and mime.startswith('video/'):
        return True
    else:
        return False

@app.route('/')
def home():
    if 'username' not in session:
        logger.info('User not logged in, redirecting to login page.')
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()

    # Recupera todos os posts e aplica a formatação de tempo
    cursor.execute("""
        SELECT id, username, content, timestamp, parent_post_id, media_filename, media_type
        FROM posts
        ORDER BY timestamp ASC
    """)
    posts_data = cursor.fetchall()

    # Formata os dados do post, incluindo o tempo resumido
    posts_dict = {}
    for row in posts_data:
        posts_dict[row.id] = {
            'id': row.id,
            'username': row.username,
            'content': row.content,
            'timestamp': row.timestamp,
            'formatted_time': format_time(row.timestamp),
            'parent_post_id': row.parent_post_id,
            'media_filename': row.media_filename,
            'media_type': row.media_type,
            'children': []
        }

    # Construir a árvore de posts
    tree_posts = []
    for post_id, post in posts_dict.items():
        parent_id = post['parent_post_id']
        if parent_id:
            parent_post = posts_dict.get(parent_id)
            if parent_post:
                parent_post['children'].append(post)
        else:
            tree_posts.append(post)

    # Recupera os likes do usuário logado
    cursor.execute("SELECT post_id FROM likes WHERE username = ?", (session['username'],))
    liked_posts = [row.post_id for row in cursor.fetchall()]
    # Recupera a contagem de likes para cada post
    cursor.execute("SELECT post_id, COUNT(username) as like_count FROM likes GROUP BY post_id")
    likes_data = cursor.fetchall()
    likes_count = {row.post_id: row.like_count for row in likes_data}
    conn.close()

    logger.info('Rendering home page for user: %s', session['username'])
    return render_template('home.html', posts=tree_posts, liked_posts=liked_posts, likes_count=likes_count)

@app.route('/reply/<int:post_id>', methods=['GET', 'POST'])
def reply(post_id):
    if 'username' not in session:
        logger.info('User not logged in, redirecting to login page.')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Busca o nome do autor e conteúdo do post original
    cursor.execute("SELECT username, content FROM posts WHERE id = ?", (post_id,))
    original_post = cursor.fetchone()

    if request.method == 'POST':
        content = request.form['content']
        cursor.execute("""
            INSERT INTO posts (username, content, parent_post_id)
            VALUES (?, ?, ?)
        """, (session['username'], content, post_id))
        conn.commit()
        conn.close()
        logger.info('User %s replied to post %d', session['username'], post_id)
        return redirect(url_for('home'))
    else:
        conn.close()
        logger.info('Rendering reply page for post %d', post_id)
        return render_template('reply.html', post_id=post_id, username=original_post.username, original_content=original_post.content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica se o usuário já existe
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        # Insere o usuário somente se ele não existir
        if user is None:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            conn.commit()
        
        conn.close()
        session['username'] = username
        logger.info('User %s logged in', username)
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logger.info('User %s logged out', session.get('username'))
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'username' not in session:
        logger.info('User not logged in, redirecting to login page.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        content = request.form['content']
        media_filename = None
        media_type = None

        # Verifica se o arquivo foi enviado
        if 'media' in request.files:
            file = request.files['media']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in {'png', 'jpg', 'jpeg', 'gif'}:
                    filetype = 'image'
                elif ext in {'mp4', 'webm'}:
                    filetype = 'video'
                else:
                    flash('Tipo de arquivo não permitido.')
                    logger.warning('Invalid file type uploaded by user %s', session['username'])
                    return redirect(request.url)

                if allowed_file(filename, filetype, file):
                    unique_filename = str(uuid.uuid4()) + '.' + ext
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

                    if filetype == 'image':
                        # Redimensiona a imagem antes de salvar
                        image = Image.open(file)
                        max_width = 800  # Define uma largura máxima confortável para exibição
                        if image.width > max_width:
                            ratio = max_width / image.width
                            new_height = int(image.height * ratio)
                            image = image.resize((max_width, new_height), Image.LANCZOS)
                        image.save(file_path)
                    else:
                        # Salva diretamente se for um vídeo
                        file.save(file_path)

                    media_filename = unique_filename
                    media_type = filetype
                else:
                    flash('Arquivo inválido ou corrompido.')
                    logger.warning('Invalid or corrupted file uploaded by user %s', session['username'])
                    return redirect(request.url)
            elif file and file.filename == '':
                flash('Nenhum arquivo selecionado.')
                logger.warning('No file selected by user %s', session['username'])
                return redirect(request.url)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO posts (username, content, media_filename, media_type)
            VALUES (?, ?, ?, ?)
        """, (session['username'], content, media_filename, media_type))
        conn.commit()
        conn.close()
        logger.info('User %s created a new post', session['username'])
        return redirect(url_for('home'))
    return render_template('create_post.html')

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if 'username' not in session:
        logger.info('User not logged in, returning error.')
        return jsonify({'error': 'User not logged in'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verifica se o usuário já deu like no post
    cursor.execute("SELECT * FROM likes WHERE post_id = ? AND username = ?", (post_id, session['username']))
    like = cursor.fetchone()
    
    if like:
        # Remove o like se ele já existir (unlike)
        cursor.execute("DELETE FROM likes WHERE post_id = ? AND username = ?", (post_id, session['username']))
        liked = False
        logger.info('User %s unliked post %d', session['username'], post_id)
    else:
        # Adiciona o like se ele não existir
        cursor.execute("INSERT INTO likes (post_id, username) VALUES (?, ?)", (post_id, session['username']))
        liked = True
        logger.info('User %s liked post %d', session['username'], post_id)
    
    # Recontar o número de likes
    cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id = ?", (post_id,))
    likes_count = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()

    return jsonify({'liked': liked, 'likes_count': likes_count})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    logger.info('File %s requested for download', filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    logger.info('Starting the Flask application')
    app.run(host='0.0.0.0', debug=True)