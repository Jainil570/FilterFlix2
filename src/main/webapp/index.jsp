<%-- index.jsp --%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8" isELIgnored="true" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapFilter - Real-time Face Filters</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #ff6b35;
            --secondary-color: #004e89;
            --accent-color: #ffd23f;
            --bg-light: #f8f9fa;
            --bg-dark: #1a1a1a;
            --text-light: #333;
            --text-dark: #ffffff;
            --card-bg-light: #ffffff;
            --card-bg-dark: #2d2d2d;
            --border-light: #e0e0e0;
            --border-dark: #404040;
            --shadow-light: 0 8px 32px rgba(0, 0, 0, 0.1);
            --shadow-dark: 0 8px 32px rgba(0, 0, 0, 0.5);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            min-height: 100vh;
            transition: all 0.3s ease;
            overflow-x: hidden;
        }

        body.dark-mode {
            background: linear-gradient(135deg, #2d1b69, #11998e);
        }

        /* Dark mode styles */
        .dark-mode {
            --bg-light: var(--bg-dark);
            --text-light: var(--text-dark);
            --card-bg-light: var(--card-bg-dark);
            --border-light: var(--border-dark);
            --shadow-light: var(--shadow-dark);
        }

        /* Theme Toggle */
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 50px;
            padding: 12px 16px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 18px;
        }

        .theme-toggle:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }

        /* Initial Screen */
        .initial-screen {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            text-align: center;
            padding: 20px;
        }

        .logo {
            font-size: 4rem;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #ff6b35, #ffd23f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: pulse 2s infinite;
        }

        .app-title {
            font-size: 3rem;
            font-weight: 800;
            color: white;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .app-subtitle {
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 40px;
            max-width: 500px;
            line-height: 1.6;
        }

        .start-camera-btn {
            background: linear-gradient(45deg, var(--accent-color), var(--primary-color));
            border: none;
            padding: 20px 40px;
            border-radius: 50px;
            font-size: 1.3rem;
            font-weight: 600;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .start-camera-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(255, 107, 53, 0.6);
        }

        /* Main Interface */
        .main-interface {
            display: none;
            opacity: 0;
            transform: translateY(50px);
            transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            padding: 20px;
            min-height: 100vh;
        }

        .main-interface.show {
            display: block;
            opacity: 1;
            transform: translateY(0);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        /* Video Container */
        .video-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 30px;
        }

        .video-container {
            position: relative;
            background: var(--card-bg-light);
            border-radius: 20px;
            padding: 20px;
            box-shadow: var(--shadow-light);
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-light);
        }

        .video-frame {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            background: #000;
            position: relative;
        }

        #videoFeed {
            width: 100%;
            height: auto;
            max-width: 640px;
            display: block;
        }

        /* Controls */
        .controls-section {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
        }

        .control-group {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }

        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            border: 2px solid transparent;
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: white;
            position: relative;
            overflow: hidden;
        }

        .btn:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }

        .btn:hover:before {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }

        .btn-primary { background: linear-gradient(45deg, #ff6b35, #f7931e); }
        .btn-secondary { background: linear-gradient(45deg, #004e89, #1f4e79); }
        .btn-success { background: linear-gradient(45deg, #28a745, #20c997); }
        .btn-danger { background: linear-gradient(45deg, #dc3545, #e91e63); }
        .btn-warning { background: linear-gradient(45deg, #ffc107, #ff9800); }
        .btn-info { background: linear-gradient(45deg, #17a2b8, #6f42c1); }
        .btn-dark { background: linear-gradient(45deg, #343a40, #495057); }

        /* Gallery */
        .gallery-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-top: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .gallery-title {
            color: white;
            font-size: 2rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .gallery-item {
            background: var(--card-bg-light);
            border-radius: 15px;
            padding: 15px;
            box-shadow: var(--shadow-light);
            transition: all 0.3s ease;
            border: 1px solid var(--border-light);
            text-align: center;
        }

        .gallery-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        }

        .gallery-item img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 10px;
        }

        .gallery-item p {
            color: var(--text-light);
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 0.9rem;
        }

        .empty-gallery {
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            font-size: 1.1rem;
            padding: 40px 20px;
        }

        /* Status Messages */
        .status {
            position: fixed;
            top: 80px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            transform: translateX(400px);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .status.show {
            transform: translateX(0);
        }

        .status.success {
            background: linear-gradient(45deg, #28a745, #20c997);
        }

        .status.error {
            background: linear-gradient(45deg, #dc3545, #e91e63);
        }

        .status.info {
            background: linear-gradient(45deg, #17a2b8, #6f42c1);
        }

        /* Animations */
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .animate-slide-up {
            animation: slideInUp 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .app-title {
                font-size: 2rem;
            }
            
            .app-subtitle {
                font-size: 1rem;
            }
            
            .start-camera-btn {
                padding: 15px 30px;
                font-size: 1.1rem;
            }
            
            .header h1 {
                font-size: 1.8rem;
            }
            
            .controls-section {
                gap: 10px;
            }
            
            .btn {
                padding: 10px 16px;
                font-size: 0.9rem;
            }
            
            .gallery-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 15px;
            }
            
            .video-container {
                padding: 15px;
            }
        }

        @media (max-width: 480px) {
            .controls-section {
                flex-direction: column;
                align-items: center;
            }
            
            .control-group {
                justify-content: center;
            }
            
            .gallery-grid {
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            }
        }

        /* Loading spinner */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- Theme Toggle -->
    <button class="theme-toggle" id="themeToggle">
        <i class="fas fa-moon"></i>
    </button>

    <!-- Initial Screen -->
    <div class="initial-screen" id="initialScreen">
        <div class="logo">🎭</div>
        <h1 class="app-title">SnapFilter</h1>
        <p class="app-subtitle">Transform your world with amazing real-time face filters. Express yourself with style!</p>
        <button class="start-camera-btn" id="startCameraBtn">
            <i class="fas fa-camera"></i> Start Camera
        </button>
    </div>

    <!-- Main Interface -->
    <div class="main-interface" id="mainInterface">
        <div class="container">
            <div class="header">
                <h1>✨ Live Filter Studio</h1>
            </div>

            <!-- Video Section -->
            <div class="video-section">
                <div class="video-container">
                    <div class="video-frame">
                        <img id="videoFeed" src="" alt="Live video feed" style="display: none;">
                    </div>
                </div>

                <!-- Main Controls -->
                <div class="controls-section">
                    <div class="control-group">
                        <button class="btn btn-danger" id="stopCameraBtn">
                            <i class="fas fa-stop"></i> Stop Camera
                        </button>
                        <button class="btn btn-success" id="captureBtn">
                            <i class="fas fa-camera"></i> Capture Photo
                        </button>
                    </div>
                </div>

                <!-- Filter Controls -->
                <div class="controls-section">
                    <div class="control-group">
                        <button class="btn btn-info" id="sunglassesBtn">
                            <i class="fas fa-glasses"></i> Sunglasses
                        </button>
                        <button class="btn btn-warning" id="puppyBtn">
                            <i class="fas fa-dog"></i> Puppy Ears
                        </button>
                        <button class="btn btn-primary" id="lipstickBtn">
                            <i class="fas fa-kiss"></i> Lipstick
                        </button>
                        <button class="btn btn-secondary" id="crownBtn">
                            <i class="fas fa-crown"></i> Crown
                        </button>
                        <button class="btn btn-dark" id="clearBtn">
                            <i class="fas fa-times"></i> Clear Filter
                        </button>
                    </div>
                </div>
            </div>

            <!-- Gallery Section -->
            <div class="gallery-section">
                <h2 class="gallery-title">📸 Your Captures</h2>
                <div class="gallery-grid" id="gallery">
                    <div class="empty-gallery">
                        <i class="fas fa-images" style="font-size: 3rem; margin-bottom: 15px; opacity: 0.5;"></i>
                        <p>No images captured yet. Start capturing some amazing moments!</p>
                    </div>
                </div>
                <div class="controls-section">
                    <a class="btn btn-info" id="downloadAllBtn" style="display: none;">
                        <i class="fas fa-download"></i> Download All as ZIP
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Status Messages -->
    <div class="status" id="status"></div>

    <script>
        // Global variables
        const FLASK_SERVER_URL = 'http://localhost:5000';
        const userId = crypto.randomUUID();
        
        // DOM elements
        const initialScreen = document.getElementById('initialScreen');
        const mainInterface = document.getElementById('mainInterface');
        const startBtn = document.getElementById('startCameraBtn');
        const stopBtn = document.getElementById('stopCameraBtn');
        const videoFeed = document.getElementById('videoFeed');
        const statusEl = document.getElementById('status');
        const galleryEl = document.getElementById('gallery');
        const downloadAllBtn = document.getElementById('downloadAllBtn');
        const themeToggle = document.getElementById('themeToggle');

        // Theme Toggle
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
            localStorage.setItem('darkMode', isDark);
        });

        // Load saved theme
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }

        // Start Camera
        startBtn.addEventListener('click', function() {
            startBtn.innerHTML = '<span class="loading"></span> Starting...';
            startBtn.disabled = true;

            // Simulate loading delay for better UX
            setTimeout(() => {
                videoFeed.src = FLASK_SERVER_URL + '/video_feed';
                videoFeed.style.display = 'block';
                
                initialScreen.style.opacity = '0';
                initialScreen.style.transform = 'scale(0.8)';
                
                setTimeout(() => {
                    initialScreen.style.display = 'none';
                    mainInterface.classList.add('show');
                    showStatus('Camera started successfully!', 'success');
                }, 300);
            }, 1000);
        });

        // Stop Camera
        stopBtn.addEventListener('click', function() {
            videoFeed.src = '';
            videoFeed.style.display = 'none';
            
            mainInterface.classList.remove('show');
            setTimeout(() => {
                initialScreen.style.display = 'flex';
                initialScreen.style.opacity = '1';
                initialScreen.style.transform = 'scale(1)';
                startBtn.innerHTML = '<i class="fas fa-camera"></i> Start Camera';
                startBtn.disabled = false;
            }, 300);
            
            showStatus('Camera stopped', 'info');
        });

        // Status Management
        function showStatus(message, type = 'info') {
            statusEl.textContent = message;
            statusEl.className = `status ${type} show`;
            
            setTimeout(() => {
                statusEl.classList.remove('show');
            }, 3000);
        }

        // Filter Functions
        function setFilter(filterName) {
            const filterButtons = document.querySelectorAll('[id$="Btn"]');
            filterButtons.forEach(btn => {
                if (btn.id.includes(filterName) || (filterName === 'none' && btn.id === 'clearBtn')) {
                    btn.style.transform = 'scale(0.95)';
                    setTimeout(() => btn.style.transform = '', 200);
                }
            });

            showStatus(`Setting ${filterName === 'none' ? 'no' : filterName} filter...`, 'info');
            
            fetch(FLASK_SERVER_URL + '/set_filter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filter: filterName })
            })
            .then(res => res.json())
            .then(data => {
                showStatus(data.success ? data.message : 'Error: ' + data.message, data.success ? 'success' : 'error');
            })
            .catch(() => {
                showStatus('Failed to set filter', 'error');
            });
        }

        // Capture Photo
        document.getElementById('captureBtn').addEventListener('click', function() {
            const btn = this;
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span class="loading"></span> Capturing...';
            btn.disabled = true;

            fetch(FLASK_SERVER_URL + '/capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId })
            })
            .then(res => res.json())
            .then(data => {
                showStatus(data.success ? data.message : 'Error: ' + data.message, data.success ? 'success' : 'error');
                if (data.success) {
                    setTimeout(updateGallery, 100);
                }
            })
            .catch(() => {
                showStatus('Failed to capture photo', 'error');
            })
            .finally(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            });
        });

        // Update Gallery
        function updateGallery() {
            fetch(FLASK_SERVER_URL + '/get_captures?user_id=' + userId)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.files.length > 0) {
                        galleryEl.innerHTML = '';
                        data.files.forEach((filename, index) => {
                            const item = document.createElement('div');
                            item.className = 'gallery-item animate-slide-up';
                            item.style.animationDelay = `${index * 0.1}s`;
                            
                            const imageUrl = FLASK_SERVER_URL + '/download/' + filename + '?user_id=' + userId;
                            const downloadUrl = imageUrl;
                            
                            item.innerHTML = `
                                <img src="${imageUrl}" alt="${filename}" loading="lazy">
                                <p>${filename}</p>
                                <a href="${downloadUrl}" class="btn btn-primary" style="font-size: 0.8rem; padding: 8px 12px;">
                                    <i class="fas fa-download"></i> Download
                                </a>
                            `;
                            galleryEl.appendChild(item);
                        });
                        
                        downloadAllBtn.href = FLASK_SERVER_URL + '/download_all?user_id=' + userId;
                        downloadAllBtn.style.display = 'inline-flex';
                    } else {
                        galleryEl.innerHTML = `
                            <div class="empty-gallery">
                                <i class="fas fa-images" style="font-size: 3rem; margin-bottom: 15px; opacity: 0.5;"></i>
                                <p>No images captured yet. Start capturing some amazing moments!</p>
                            </div>
                        `;
                        downloadAllBtn.style.display = 'none';
                    }
                });
        }

        // Filter Event Listeners
        document.getElementById('sunglassesBtn').addEventListener('click', () => setFilter('sunglasses'));
        document.getElementById('puppyBtn').addEventListener('click', () => setFilter('puppy'));
        document.getElementById('lipstickBtn').addEventListener('click', () => setFilter('lipstick'));
        document.getElementById('crownBtn').addEventListener('click', () => setFilter('crown'));
        document.getElementById('clearBtn').addEventListener('click', () => setFilter('none'));

        // Initialize gallery on load
        window.addEventListener('load', updateGallery);

        // Add some interactive animations
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.02)';
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    </script>
</body>
</html>