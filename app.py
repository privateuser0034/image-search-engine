<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Search Engine</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .nav-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
            gap: 10px;
        }

        .nav-tab {
            padding: 12px 24px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
        }

        .nav-tab.active {
            background: white;
            color: #667eea;
            font-weight: bold;
        }

        .search-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .search-bar {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            align-items: center;
        }

        #searchInput {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }

        #searchInput:focus {
            border-color: #667eea;
        }

        .search-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s;
        }

        .search-btn:hover {
            transform: translateY(-2px);
        }

        .filters {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            align-items: end;
        }

        .filter-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #555;
        }

        select, input[type="url"], input[type="text"] {
            width: 100%;
            padding: 8px 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }

        select:focus, input:focus {
            border-color: #667eea;
        }

        .add-video-section {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            display: none;
        }

        .add-video-section.active {
            display: block;
        }

        .add-video-form {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr auto;
            gap: 10px;
            align-items: end;
        }

        .add-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }

        .results-info {
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            padding: 15px 20px;
            margin-bottom: 20px;
            display: none;
        }

        .media-grid {
            display: grid;
            gap: 20px;
            margin-bottom: 30px;
        }

        .image-grid {
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        }

        .video-grid {
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        }

        .media-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }

        .media-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }

        .image-wrapper, .video-wrapper {
            position: relative;
            width: 100%;
            height: 200px;
            overflow: hidden;
            background: #f0f0f0;
        }

        .video-wrapper {
            height: 180px;
        }

        .media-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }

        .media-card:hover img {
            transform: scale(1.05);
        }

        .play-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.7);
            border-radius: 50%;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
        }

        .duration-badge {
            position: absolute;
            bottom: 8px;
            right: 8px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
        }

        .media-info {
            padding: 15px;
        }

        .media-title {
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            line-height: 1.3;
        }

        .media-meta {
            font-size: 12px;
            color: #666;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 5px;
        }

        .site-badge {
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: bold;
        }

        .save-btn {
            background: none;
            border: none;
            color: #666;
            cursor: pointer;
            font-size: 16px;
            transition: color 0.3s;
        }

        .save-btn.saved {
            color: #e74c3c;
        }

        .save-btn:hover {
            color: #e74c3c;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: white;
            font-size: 18px;
        }

        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 30px 0;
        }

        .pagination button {
            padding: 8px 16px;
            border: none;
            background: white;
            color: #667eea;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s;
        }

        .pagination button:hover:not(:disabled) {
            background: #667eea;
            color: white;
        }

        .pagination button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .pagination .current-page {
            background: #667eea;
            color: white;
        }

        /* Modal styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
        }

        .modal-content {
            position: relative;
            margin: auto;
            padding: 20px;
            width: 90%;
            max-width: 1200px;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .modal img {
            max-width: 100%;
            max-height: 90vh;
            object-fit: contain;
        }

        .modal iframe {
            width: 90vw;
            height: 90vh;
            max-width: 1200px;
            max-height: 675px;
            border: none;
            border-radius: 10px;
        }

        .close {
            position: absolute;
            top: 20px;
            right: 40px;
            color: white;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            z-index: 1001;
        }

        .close:hover {
            opacity: 0.7;
        }

        .video-info-panel {
            position: absolute;
            bottom: 20px;
            left: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 15px;
            border-radius: 10px;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: #28a745;
            color: white;
            border-radius: 8px;
            z-index: 2000;
            display: none;
        }

        .notification.error {
            background: #dc3545;
        }

        @media (max-width: 768px) {
            .search-bar, .add-video-form {
                flex-direction: column;
            }

            .filters {
                grid-template-columns: 1fr;
            }

            .media-grid {
                grid-template-columns: 1fr;
                gap: 15px;
            }

            .add-video-form {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎬 Media Search Engine</h1>
            <p>Search and discover images & videos from across the web</p>
        </header>

        <div class="nav-tabs">
            <button class="nav-tab active" onclick="switchTab('images')">🖼️ Images</button>
            <button class="nav-tab" onclick="switchTab('videos')">🎥 Videos</button>
        </div>

        <div class="search-container">
            <div class="search-bar">
                <input type="text" id="searchInput" placeholder="Search by title, tags, or description..." autocomplete="off">
                <button class="search-btn" onclick="performSearch(1)">Search</button>
            </div>

            <!-- Image Filters -->
            <div class="filters" id="imageFilters">
                <div class="filter-group">
                    <label for="imageCategoryFilter">Category:</label>
                    <select id="imageCategoryFilter">
                        <option value="">All Categories</option>
                        {% for category in image_categories %}
                        <option value="{{ category }}">{{ category.title() }}</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="filter-group">
                    <label for="orientationFilter">Orientation:</label>
                    <select id="orientationFilter">
                        <option value="">All Orientations</option>
                        <option value="landscape">Landscape</option>
                        <option value="portrait">Portrait</option>
                        <option value="square">Square</option>
                    </select>
                </div>
            </div>

            <!-- Video Filters -->
            <div class="filters" id="videoFilters" style="display: none;">
                <div class="filter-group">
                    <label for="siteFilter">Site:</label>
                    <select id="siteFilter">
                        <option value="">All Sites</option>
                        {% for site in video_sites %}
                        <option value="{{ site }}">{{ site }}</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="filter-group">
                    <label for="videoCategoryFilter">Category:</label>
                    <select id="videoCategoryFilter">
                        <option value="">All Categories</option>
                        {% for category in video_categories %}
                        <option value="{{ category }}">{{ category.title() }}</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="filter-group">
                    <label></label>
                    <button class="search-btn" onclick="showAddVideoForm()" style="background: #28a745;">➕ Add Video</button>
                </div>
            </div>

            <!-- Add Video Form -->
            <div class="add-video-section" id="addVideoSection">
                <h3 style="color: white; margin-bottom: 15px;">Add Video from URL</h3>
                <div class="add-video-form">
                    <div class="filter-group">
                        <label for="videoUrl" style="color: white;">Video URL:</label>
                        <input type="url" id="videoUrl" placeholder="https://youtube.com/watch?v=... or any supported site">
                    </div>
                    <div class="filter-group">
                        <label for="videoCategory" style="color: white;">Category:</label>
                        <input type="text" id="videoCategory" placeholder="e.g., entertainment, music">
                    </div>
                    <div class="filter-group">
                        <label for="videoTags" style="color: white;">Tags:</label>
                        <input type="text" id="videoTags" placeholder="comma, separated, tags">
                    </div>
                    <div class="filter-group">
                        <label style="color: transparent;">Actions:</label>
                        <button class="add-btn" onclick="addVideo()">Add Video</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="results-info" id="resultsInfo"></div>

        <div class="loading" id="loading" style="display: none;">
            🔄 Loading media...
        </div>

        <div class="media-grid image-grid" id="mediaGrid"></div>

        <div class="pagination" id="pagination" style="display: none;"></div>
    </div>

    <!-- Notification -->
    <div class="notification" id="notification"></div>

    <!-- Modal for full-size media -->
    <div id="mediaModal" class="modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <div class="modal-content">
            <img id="modalImage" src="" alt="" style="display: none;">
            <iframe id="modalVideo" src="" style="display: none;"></iframe>
            <div class="video-info-panel" id="videoInfoPanel" style="display: none;">
                <h3 id="videoTitle"></h3>
                <p id="videoDescription"></p>
                <div id="videoMeta"></div>
            </div>
        </div>
    </div>

    <script>
        let currentPage = 1;
        let currentTab = 'images';
        let isLoading = false;

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            // Search on Enter key
            document.getElementById('searchInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    performSearch(1);
                }
            });

            // Search on filter change
            document.querySelectorAll('select').forEach(element => {
                element.addEventListener('change', () => performSearch(1));
            });

            // Initial load
            performSearch(1);
        });

        function switchTab(tab) {
            currentTab = tab;
            currentPage = 1;
            
            // Update tab buttons
            document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Show/hide appropriate filters
            document.getElementById('imageFilters').style.display = tab === 'images' ? 'grid' : 'none';
            document.getElementById('videoFilters').style.display = tab === 'videos' ? 'grid' : 'none';
            
            // Update grid class
            const mediaGrid = document.getElementById('mediaGrid');
            mediaGrid.className = `media-grid ${tab}-grid`;
            
            // Clear current results and search
            mediaGrid.innerHTML = '';
            document.getElementById('pagination').style.display = 'none';
            document.getElementById('resultsInfo').style.display = 'none';
            
            performSearch(1);
        }

        function showAddVideoForm() {
            const section = document.getElementById('addVideoSection');
            section.classList.toggle('active');
        }

        async function addVideo() {
            const url = document.getElementById('videoUrl').value.trim();
            const category = document.getElementById('videoCategory').value.trim();
            const tags = document.getElementById('videoTags').value.trim();
            
            if (!url) {
                showNotification('Please enter a video URL', 'error');
                return;
            }
            
            try {
                const response = await fetch('/add_video', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        url: url,
                        category: category || 'uncategorized',
                        tags: tags
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showNotification(`Video "${data.title}" added successfully!`);
                    document.getElementById('videoUrl').value = '';
                    document.getElementById('videoCategory').value = '';
                    document.getElementById('videoTags').value = '';
                    document.getElementById('addVideoSection').classList.remove('active');
                    
                    // Refresh search if on videos tab
                    if (currentTab === 'videos') {
                        performSearch(1);
                    }
                } else {
                    showNotification(data.error, 'error');
                }
            } catch (error) {
                showNotification('Failed to add video. Please try again.', 'error');
                console.error('Error:', error);
            }
        }

        async function performSearch(page = 1) {
            if (isLoading) return;
            
            isLoading = true;
            currentPage = page;
            
            const loading = document.getElementById('loading');
            const mediaGrid = document.getElementById('mediaGrid');
            const pagination = document.getElementById('pagination');
            const resultsInfo = document.getElementById('resultsInfo');
            
            loading.style.display = 'block';
            if (page === 1) {
                mediaGrid.innerHTML = '';
                pagination.style.display = 'none';
                resultsInfo.style.display = 'none';
            }

            const query = document.getElementById('searchInput').value;
            
            let params, endpoint;
            if (currentTab === 'images') {
                params = new URLSearchParams({
                    q: query,
                    category: document.getElementById('imageCategoryFilter').value,
                    orientation: document.getElementById('orientationFilter').value,
                    page: page.toString()
                });
                endpoint = '/search_images';
            } else {
                params = new URLSearchParams({
                    q: query,
                    site: document.getElementById('siteFilter').value,
                    category: document.getElementById('videoCategoryFilter').value,
                    page: page.toString()
                });
                endpoint = '/search_videos';
            }

            try {
                const response = await fetch(`${endpoint}?${params}`);
                const data = await response.json();

                loading.style.display = 'none';
                
                if (currentTab === 'images') {
                    displayImageResults(data, page === 1);
                } else {
                    displayVideoResults(data, page === 1);
                }
                displayPagination(data);
                displayResultsInfo(data, currentTab);
                
            } catch (error) {
                console.error('Search error:', error);
                loading.style.display = 'none';
                mediaGrid.innerHTML = '<p style="color: white; text-align: center;">Error loading media. Please try again.</p>';
            }
            
            isLoading = false;
        }

        function displayImageResults(data, replace = false) {
            const mediaGrid = document.getElementById('mediaGrid');
            
            if (replace) {
                mediaGrid.innerHTML = '';
            }

            data.images.forEach(image => {
                const card = document.createElement('div');
                card.className = 'media-card';
                card.onclick = () => openImageModal(image.url, image.filename);
                
                const fileSizeKB = Math.round(image.filesize / 1024);
                
                card.innerHTML = `
                    <div class="image-wrapper">
                        <img src="${image.url}" alt="${image.filename}" loading="lazy" 
                             onerror="this.style.display='none'; this.parentNode.innerHTML='<div style=\\'display:flex;align-items:center;justify-content:center;height:100%;color:#999;\\'>Image not found</div>'">
                    </div>
                    <div class="media-info">
                        <div class="media-title">${image.filename}</div>
                        <div class="media-meta">
                            <span>${image.width}×${image.height}</span>
                            <span>${fileSizeKB} KB</span>
                            <span>${image.orientation}</span>
                            <span class="site-badge">${image.category}</span>
                        </div>
                    </div>
                `;
                
                mediaGrid.appendChild(card);
            });

            if (data.images.length === 0 && replace) {
                mediaGrid.innerHTML = '<p style="color: white; text-align: center; grid-column: 1/-1;">No images found matching your criteria.</p>';
            }
        }

        function displayVideoResults(data, replace = false) {
            const mediaGrid = document.getElementById('mediaGrid');
            
            if (replace) {
                mediaGrid.innerHTML = '';
            }

            data.videos.forEach(video => {
                const card = document.createElement('div');
                card.className = 'media-card';
                
                card.innerHTML = `
                    <div class="video-wrapper" onclick="openVideoModal('${video.url}', ${JSON.stringify(video).replace(/"/g, '&quot;')})">
                        <img src="${video.thumbnail || '/static/video-placeholder.jpg'}" alt="${video.title}" loading="lazy"
                             onerror="this.src='/static/video-placeholder.jpg'">
                        <div class="play-overlay">▶</div>
                        ${video.duration ? `<div class="duration-badge">${video.duration}</div>` : ''}
                    </div>
                    <div class="media-info">
                        <div class="media-title">${video.title}</div>
                        <div class="media-meta">
                            <span class="site-badge">${video.site}</span>
                            ${video.view_count ? `<span>${formatNumber(video.view_count)} views</span>` : ''}
                            <button class="save-btn ${video.saved ? 'saved' : ''}" 
                                    onclick="toggleSaveVideo(${video.id}, this)" 
                                    title="${video.saved ? 'Remove from saved' : 'Save video'}">
                                ${video.saved ? '❤️' : '🤍'}
                            </button>
                        </div>
                    </div>
                `;
                
                mediaGrid.appendChild(card);
            });

            if (data.videos.length === 0 && replace) {
                mediaGrid.innerHTML = '<p style="color: white; text-align: center; grid-column: 1/-1;">No videos found matching your criteria.</p>';
            }
        }

        function displayPagination(data) {
            const pagination = document.getElementById('pagination');
            
            if (data.total_pages <= 1) {
                pagination.style.display = 'none';
                return;
            }

            pagination.style.display = 'flex';
            pagination.innerHTML = '';

            // Previous button
            const prevBtn = document.createElement('button');
            prevBtn.textContent = '← Previous';
            prevBtn.disabled = data.page === 1;
            prevBtn.onclick = () => performSearch(data.page - 1);
            pagination.appendChild(prevBtn);

            // Page numbers
            const startPage = Math.max(1, data.page - 2);
            const endPage = Math.min(data.total_pages, data.page + 2);

            if (startPage > 1) {
                const firstBtn = document.createElement('button');
                firstBtn.textContent = '1';
                firstBtn.onclick = () => performSearch(1);
                pagination.appendChild(firstBtn);
                
                if (startPage > 2) {
                    const ellipsis = document.createElement('span');
                    ellipsis.textContent = '...';
                    ellipsis.style.padding = '8px';
                    ellipsis.style.color = 'white';
                    pagination.appendChild(ellipsis);
                }
            }

            for (let i = startPage; i <= endPage; i++) {
                const pageBtn = document.createElement('button');
                pageBtn.textContent = i;
                pageBtn.className = i === data.page ? 'current-page' : '';
                pageBtn.onclick = () => performSearch(i);
                pagination.appendChild(pageBtn);
            }

            if (endPage < data.total_pages) {
                if (endPage < data.total_pages - 1) {
                    const ellipsis = document.createElement('span');
                    ellipsis.textContent = '...';
                    ellipsis.style.padding = '8px';
                    ellipsis.style.color = 'white';
                    pagination.appendChild(ellipsis);
                }
                
                const lastBtn = document.createElement('button');
                lastBtn.textContent = data.total_pages;
                lastBtn.onclick = () => performSearch(data.total_pages);
                pagination.appendChild(lastBtn);
            }

            // Next button
            const nextBtn = document.createElement('button');
            nextBtn.textContent = 'Next →';
            nextBtn.disabled = data.page === data.total_pages;
            nextBtn.onclick = () => performSearch(data.page + 1);
            pagination.appendChild(nextBtn);
        }

        function displayResultsInfo(data, type) {
            const resultsInfo = document.getElementById('resultsInfo');
            const start = (data.page - 1) * data.per_page + 1;
            const end = Math.min(data.page * data.per_page, data.total);
            const itemType = type === 'images' ? 'images' : 'videos';
            
            resultsInfo.innerHTML = `
                Showing ${start}-${end} of ${data.total} ${itemType} 
                (Page ${data.page} of ${data.total_pages})
            `;
            resultsInfo.style.display = 'block';
        }

        function openImageModal(imageSrc, filename) {
            const modal = document.getElementById('mediaModal');
            const modalImg = document.getElementById('modalImage');
            const modalVideo = document.getElementById('modalVideo');
            const videoPanel = document.getElementById('videoInfoPanel');
            
            modal.style.display = 'block';
            modalImg.src = imageSrc;
            modalImg.alt = filename;
            modalImg.style.display = 'block';
            modalVideo.style.display = 'none';
            videoPanel.style.display = 'none';
            
            setupModalEvents();
        }

        function openVideoModal(videoUrl, videoData) {
            const modal = document.getElementById('mediaModal');
            const modalImg = document.getElementById('modalImage');
            const modalVideo = document.getElementById('modalVideo');
            const videoPanel = document.getElementById('videoInfoPanel');
            
            modal.style.display = 'block';
            modalImg.style.display = 'none';
            modalVideo.style.display = 'block';
            videoPanel.style.display = 'block';
            
            // Set up video embed
            const embedUrl = getEmbedUrl(videoUrl);
            modalVideo.src = embedUrl;
            
            // Update video info panel
            document.getElementById('videoTitle').textContent = videoData.title;
            document.getElementById('videoDescription').textContent = videoData.description;
            document.getElementById('videoMeta').innerHTML = `
                <span class="site-badge">${videoData.site}</span>
                ${videoData.duration ? `<span>${videoData.duration}</span>` : ''}
                ${videoData.view_count ? `<span>${formatNumber(videoData.view_count)} views</span>` : ''}
            `;
            
            setupModalEvents();
        }

        function getEmbedUrl(url) {
            // Convert various video URLs to embed format
            const urlObj = new URL(url);
            const hostname = urlObj.hostname.toLowerCase();
            
            if (hostname.includes('youtube.com') || hostname.includes('youtu.be')) {
                const videoId = hostname.includes('youtu.be') 
                    ? urlObj.pathname.slice(1) 
                    : new URLSearchParams(urlObj.search).get('v');
                return `https://www.youtube.com/embed/${videoId}`;
            }
            
            // For other sites, try to return the original URL
            // Note: Many adult sites don't support embedding due to security policies
            // You might need to open in a new tab instead
            return url;
        }

        function setupModalEvents() {
            const modal = document.getElementById('mediaModal');
            
            // Close modal on background click
            modal.onclick = function(event) {
                if (event.target === modal) {
                    closeModal();
                }
            };
            
            // Close modal on Escape key
            document.addEventListener('keydown', function(event) {
                if (event.key === 'Escape') {
                    closeModal();
                }
            });
        }

        function closeModal() {
            const modal = document.getElementById('mediaModal');
            const modalVideo = document.getElementById('modalVideo');
            
            modal.style.display = 'none';
            modalVideo.src = ''; // Stop video playback
            document.getElementById('modalImage').src = '';
        }

        async function toggleSaveVideo(videoId, button) {
            try {
                const response = await fetch('/toggle_save_video', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ video_id: videoId })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    button.classList.toggle('saved', data.saved);
                    button.innerHTML = data.saved ? '❤️' : '🤍';
                    button.title = data.saved ? 'Remove from saved' : 'Save video';
                    
                    showNotification(data.saved ? 'Video saved!' : 'Video removed from saved');
                } else {
                    showNotification('Failed to update video', 'error');
                }
            } catch (error) {
                showNotification('Failed to update video', 'error');
                console.error('Error:', error);
            }
        }

        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${type}`;
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }

        function formatNumber(num) {
            if (num >= 1000000) {
                return (num / 1000000).toFixed(1) + 'M';
            } else if (num >= 1000) {
                return (num / 1000).toFixed(1) + 'K';
            }
            return num.toString();
        }
    </script>
</body>
</html>
