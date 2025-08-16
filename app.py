import os
import re
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
from PIL import Image
import mimetypes
from pathlib import Path
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import yt_dlp
import hashlib

app = Flask(__name__)

# Configuration for cloud deployment
class Config:
    DATABASE_PATH = os.environ.get('DATABASE_URL', 'media.db')
    IMAGES_FOLDER = os.environ.get('IMAGES_FOLDER', 'static/images')
    VIDEOS_FOLDER = os.environ.get('VIDEOS_FOLDER', 'static/videos')
    
    # For external storage
    EXTERNAL_IMAGE_BASE_URL = os.environ.get('EXTERNAL_IMAGE_BASE_URL', '')
    EXTERNAL_VIDEO_BASE_URL = os.environ.get('EXTERNAL_VIDEO_BASE_URL', '')
    USE_EXTERNAL_STORAGE = os.environ.get('USE_EXTERNAL_STORAGE', 'false').lower() == 'true'
    
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'}
    RESULTS_PER_PAGE = 20
    
    # Cloud settings
    PORT = int(os.environ.get('PORT', 5000))
    HOST = os.environ.get('HOST', '0.0.0.0')

def init_database():
    """Initialize the database with media tables."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Images table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            filepath TEXT NOT NULL,
            filesize INTEGER,
            width INTEGER,
            height INTEGER,
            orientation TEXT,
            category TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            external_url TEXT
        )
    ''')
    
    # Videos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            thumbnail_url TEXT,
            duration TEXT,
            site TEXT,
            category TEXT,
            tags TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            saved BOOLEAN DEFAULT FALSE,
            local_path TEXT,
            view_count INTEGER DEFAULT 0
        )
    ''')
    
    # Saved videos table (for downloaded content)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_video_id INTEGER,
            filename TEXT,
            filepath TEXT,
            filesize INTEGER,
            duration_seconds INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (original_video_id) REFERENCES videos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_video_info(url):
    """Extract video information from URL using yt-dlp."""
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                'title': info.get('title', 'Unknown Title'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': format_duration(info.get('duration', 0)),
                'description': info.get('description', '')[:500] if info.get('description') else '',
                'site': info.get('extractor_key', get_site_from_url(url)),
                'view_count': info.get('view_count', 0)
            }
    except Exception as e:
        print(f"Error extracting video info for {url}: {e}")
        return {
            'title': 'Unknown Title',
            'thumbnail': '',
            'duration': '00:00',
            'description': '',
            'site': get_site_from_url(url),
            'view_count': 0
        }

def get_site_from_url(url):
    """Extract site name from URL."""
    domain = urlparse(url).netloc.lower()
    
    site_mapping = {
        'youtube.com': 'YouTube',
        'youtu.be': 'YouTube',
        'pornhub.com': 'Pornhub',
        'xhamster.com': 'xHamster',
        'chaturbate.com': 'Chaturbate',
        'xnxx.com': 'XNXX',
        'xvideos.com': 'Xvideos',
        'redtube.com': 'RedTube',
        'spankbang.com': 'SpankBang'
    }
    
    for domain_key, site_name in site_mapping.items():
        if domain_key in domain:
            return site_name
    
    return domain.replace('www.', '').split('.')[0].title()

def format_duration(seconds):
    """Convert seconds to HH:MM:SS format."""
    if not seconds:
        return "00:00"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def add_sample_images():
    """Add sample images for demonstration."""
    sample_images = [
        {
            'filename': 'nature_sunset.jpg',
            'filepath': 'nature/sunset.jpg',
            'filesize': 245760,
            'width': 1920,
            'height': 1080,
            'orientation': 'landscape',
            'category': 'nature',
            'tags': 'sunset, sky, beautiful',
            'external_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400'
        },
        {
            'filename': 'urban_street.jpg',
            'filepath': 'urban/street.jpg',
            'filesize': 189432,
            'width': 1080,
            'height': 1920,
            'orientation': 'portrait',
            'category': 'urban',
            'tags': 'city, street, night',
            'external_url': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400'
        },
        {
            'filename': 'abstract_art.jpg',
            'filepath': 'art/abstract.jpg',
            'filesize': 156789,
            'width': 800,
            'height': 800,
            'orientation': 'square',
            'category': 'art',
            'tags': 'abstract, colorful, art',
            'external_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400'
        }
    ]
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    for img in sample_images:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO images (filename, filepath, filesize, width, height, orientation, category, tags, external_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (img['filename'], img['filepath'], img['filesize'], img['width'], 
                 img['height'], img['orientation'], img['category'], img['tags'], img['external_url']))
        except Exception as e:
            print(f"Error inserting sample image {img['filename']}: {e}")
    
    conn.commit()
    conn.close()

def search_images(query='', category='', orientation='', page=1):
    """Search images based on filters."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    conditions = []
    params = []
    
    if query:
        conditions.append('(filename LIKE ? OR tags LIKE ?)')
        params.extend([f'%{query}%', f'%{query}%'])
    
    if category:
        conditions.append('category = ?')
        params.append(category)
    
    if orientation:
        conditions.append('orientation = ?')
        params.append(orientation)
    
    where_clause = 'WHERE ' + ' AND '.join(conditions) if conditions else ''
    
    # Get total count
    cursor.execute(f'SELECT COUNT(*) FROM images {where_clause}', params)
    total_count = cursor.fetchone()[0]
    
    # Get paginated results
    offset = (page - 1) * Config.RESULTS_PER_PAGE
    cursor.execute(f'''
        SELECT filename, filepath, filesize, width, height, orientation, category, external_url
        FROM images {where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    ''', params + [Config.RESULTS_PER_PAGE, offset])
    
    results = cursor.fetchall()
    conn.close()
    
    return {
        'images': [
            {
                'filename': row[0],
                'filepath': row[1],
                'filesize': row[2],
                'width': row[3],
                'height': row[4],
                'orientation': row[5],
                'category': row[6],
                'url': row[7] or f'/image/{row[1]}'
            }
            for row in results
        ],
        'total': total_count,
        'page': page,
        'per_page': Config.RESULTS_PER_PAGE,
        'total_pages': (total_count + Config.RESULTS_PER_PAGE - 1) // Config.RESULTS_PER_PAGE
    }

def search_videos(query='', site='', category='', page=1):
    """Search videos based on filters."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    conditions = []
    params = []
    
    if query:
        conditions.append('(title LIKE ? OR tags LIKE ? OR description LIKE ?)')
        params.extend([f'%{query}%', f'%{query}%', f'%{query}%'])
    
    if site:
        conditions.append('site = ?')
        params.append(site)
    
    if category:
        conditions.append('category = ?')
        params.append(category)
    
    where_clause = 'WHERE ' + ' AND '.join(conditions) if conditions else ''
    
    # Get total count
    cursor.execute(f'SELECT COUNT(*) FROM videos {where_clause}', params)
    total_count = cursor.fetchone()[0]
    
    # Get paginated results
    offset = (page - 1) * Config.RESULTS_PER_PAGE
    cursor.execute(f'''
        SELECT id, title, url, thumbnail_url, duration, site, category, description, saved, view_count
        FROM videos {where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    ''', params + [Config.RESULTS_PER_PAGE, offset])
    
    results = cursor.fetchall()
    conn.close()
    
    return {
        'videos': [
            {
                'id': row[0],
                'title': row[1],
                'url': row[2],
                'thumbnail': row[3],
                'duration': row[4],
                'site': row[5],
                'category': row[6],
                'description': row[7],
                'saved': bool(row[8]),
                'view_count': row[9]
            }
            for row in results
        ],
        'total': total_count,
        'page': page,
        'per_page': Config.RESULTS_PER_PAGE,
        'total_pages': (total_count + Config.RESULTS_PER_PAGE - 1) // Config.RESULTS_PER_PAGE
    }

@app.route('/')
def index():
    """Homepage with media search interface."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get categories for both images and videos
    cursor.execute('SELECT DISTINCT category FROM images WHERE category IS NOT NULL ORDER BY category')
    image_categories = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT DISTINCT category FROM videos WHERE category IS NOT NULL ORDER BY category')
    video_categories = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT DISTINCT site FROM videos ORDER BY site')
    video_sites = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('index.html', 
                         image_categories=image_categories,
                         video_categories=video_categories,
                         video_sites=video_sites)

@app.route('/search_images')
def search_images_route():
    """Image search API endpoint."""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    orientation = request.args.get('orientation', '')
    page = int(request.args.get('page', 1))
    
    results = search_images(query, category, orientation, page)
    return jsonify(results)

@app.route('/search_videos')
def search_videos_route():
    """Video search API endpoint."""
    query = request.args.get('q', '')
    site = request.args.get('site', '')
    category = request.args.get('category', '')
    page = int(request.args.get('page', 1))
    
    results = search_videos(query, site, category, page)
    return jsonify(results)

@app.route('/add_video', methods=['POST'])
def add_video():
    """Add a video from URL."""
    data = request.get_json()
    url = data.get('url', '').strip()
    category = data.get('category', 'uncategorized')
    tags = data.get('tags', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Get video information
        video_info = get_video_info(url)
        
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if video already exists
        cursor.execute('SELECT id FROM videos WHERE url = ?', (url,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Video already exists'}), 409
        
        # Insert video
        cursor.execute('''
            INSERT INTO videos (title, url, thumbnail_url, duration, site, category, tags, description, view_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (video_info['title'], url, video_info['thumbnail'], video_info['duration'],
              video_info['site'], category, tags, video_info['description'], video_info['view_count']))
        
        video_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'video_id': video_id, 'title': video_info['title']})
        
    except Exception as e:
        return jsonify({'error': f'Failed to add video: {str(e)}'}), 500

@app.route('/toggle_save_video', methods=['POST'])
def toggle_save_video():
    """Toggle save status of a video."""
    data = request.get_json()
    video_id = data.get('video_id')
    
    if not video_id:
        return jsonify({'error': 'Video ID is required'}), 400
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get current save status
    cursor.execute('SELECT saved FROM videos WHERE id = ?', (video_id,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return jsonify({'error': 'Video not found'}), 404
    
    # Toggle save status
    new_status = not bool(result[0])
    cursor.execute('UPDATE videos SET saved = ? WHERE id = ?', (new_status, video_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'saved': new_status})

@app.route('/image/<path:filepath>')
def serve_image(filepath):
    """Serve images from the images folder."""
    return send_from_directory(Config.IMAGES_FOLDER, filepath)

@app.route('/stats')
def stats():
    """Get database statistics."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM images')
    total_images = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM videos')
    total_videos = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM videos WHERE saved = 1')
    saved_videos = cursor.fetchone()[0]
    
    cursor.execute('SELECT site, COUNT(*) FROM videos GROUP BY site')
    site_stats = dict(cursor.fetchall())
    
    conn.close()
    
    return jsonify({
        'total_images': total_images,
        'total_videos': total_videos,
        'saved_videos': saved_videos,
        'sites': site_stats
    })

if __name__ == '__main__':
    print("Initializing database...")
    init_database()
    
    print("Adding sample images...")
    add_sample_images()
    
    print("Starting Flask app...")
    app.run(debug=True, host=Config.HOST, port=Config.PORT)
