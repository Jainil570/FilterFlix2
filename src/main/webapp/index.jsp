<%-- index.jsp --%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8" isELIgnored="true" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Live Camera from JSP</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; text-align: center; background-color: #f4f4f9; margin: 0; padding: 20px; }
        h1 { color: #333; }
        .video-container { margin: 20px auto; border: 5px solid #555; border-radius: 10px; width: 640px; height: 480px; overflow: hidden; box-shadow: 0 6px 12px rgba(0,0,0,0.2); background-color: #000; }
        img { display: block; width: 100%; height: 100%; }
        .controls { margin: 20px; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
        button, .download-btn { padding: 12px 24px; font-size: 16px; font-weight: 600; cursor: pointer; border-radius: 8px; border: none; color: white; transition: all 0.2s ease-in-out; box-shadow: 0 2px 4px rgba(0,0,0,0.15); text-decoration: none; display: inline-block; }
        button:hover, .download-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        #captureBtn { background-color: #4CAF50; }
        #sunglassesBtn { background-color: #008CBA; }
        #puppyBtn { background-color: #f44336; }
        #lipstickBtn { background-color: #E91E63; }
        #crownBtn { background-color: #FFC107; }
        #clearBtn { background-color: #555; }
        #downloadAllBtn { background-color: #9C27B0; } /* Purple */
        .download-btn { background-color: #009688; font-size: 14px; padding: 8px 16px; } /* Teal */
        #status { margin-top: 15px; font-weight: bold; min-height: 22px; font-size: 1.1em; }
        .success { color: #2a9d8f; }
        .error { color: #e76f51; }
        #gallery-container { margin-top: 30px; }
        #gallery { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 10px; }
        .gallery-item { border: 2px solid #ddd; border-radius: 8px; padding: 10px; background-color: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .gallery-item p { margin: 0 0 10px 0; font-weight: 500; }
    </style>
</head>
<body>
    <h1>Live Camera Feed with Filters 👑</h1>
    <p>Select a filter to apply it to the live video stream.</p>
    
    <div class="video-container" id="videoContainer" style="display: none;">
    	<img id="videoFeed" src="" width="640" height="480" alt="Live video feed">
	</div>


    <div class="controls">
    	<button id="startCameraBtn" style="background-color: #6a1b9a;">🎥 Start Camera</button>
    	<button id="stopCameraBtn" style="background-color: #b71c1c; display: none;">🛑 Stop Camera</button>
        <button id="sunglassesBtn">😎 Sunglasses</button>
        <button id="puppyBtn">🐶 Puppy Ears</button>
        <button id="lipstickBtn">💄 Lipstick</button>
        <button id="crownBtn">👑 Crown</button>
        <button id="clearBtn">🚫 Clear Filter</button>
        <button id="captureBtn">📸 Capture Photo</button>
    </div>
    <p id="status"></p>

    <div id="gallery-container">
        <h2>Your Captures</h2>
        <div id="gallery">
            <p>No images captured yet. Use the "Capture Photo" button!</p>
        </div>
        <div class="controls" style="margin-top: 20px;">
             <a id="downloadAllBtn" class="download-btn" style="display: none;">📦 Download All as ZIP</a>
        </div>
    </div>

    <script>
        const statusEl = document.getElementById('status');
        const galleryEl = document.getElementById('gallery');
        const downloadAllBtn = document.getElementById('downloadAllBtn');
        const FLASK_SERVER_URL = 'http://localhost:5000';

        // --- FIX: Create a unique ID on the client-side ---
        const userId = crypto.randomUUID();
        // Start Camera Button Logic
        const startBtn = document.getElementById('startCameraBtn');
        const stopBtn = document.getElementById('stopCameraBtn');
        const videoContainer = document.getElementById('videoContainer');
        const videoFeed = document.getElementById('videoFeed');

        startBtn.addEventListener('click', function () {
            videoFeed.src = FLASK_SERVER_URL + '/video_feed';
            videoContainer.style.display = 'block';
            startBtn.style.display = 'none';
            stopBtn.style.display = 'inline-block';
        });

        stopBtn.addEventListener('click', function () {
            videoFeed.src = '';  // Stop the stream by removing the source
            videoContainer.style.display = 'none';
            stopBtn.style.display = 'none';
            startBtn.style.display = 'inline-block';
        });

        function updateGallery() {
            // Send the userId as a query parameter
            fetch(FLASK_SERVER_URL + '/get_captures?user_id=' + userId)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.files.length > 0) {
                        galleryEl.innerHTML = '';
                        data.files.forEach(filename => {
                            const item = document.createElement('div');
                            item.className = 'gallery-item';
                            const downloadUrl = FLASK_SERVER_URL + '/download/' + filename + '?user_id=' + userId;
                            item.innerHTML = '<p>' + filename + '</p>' +
                                             '<a href="' + downloadUrl + '" class="download-btn">Download</a>';
                            galleryEl.appendChild(item);
                        });
                        downloadAllBtn.href = FLASK_SERVER_URL + '/download_all?user_id=' + userId;
                        downloadAllBtn.style.display = 'inline-block';
                    } else {
                        galleryEl.innerHTML = '<p>No images captured yet. Use the "Capture Photo" button!</p>';
                        downloadAllBtn.style.display = 'none';
                    }
                });
        }

        function setFilter(filterName) {
            statusEl.textContent = `Setting filter to ${filterName}...`;
            statusEl.className = '';
            fetch(FLASK_SERVER_URL + '/set_filter', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ filter: filterName }) })
                .then(res => res.json()).then(data => {
                    statusEl.textContent = data.success ? data.message : 'Error: ' + data.message;
                    statusEl.className = data.success ? 'success' : 'error';
                }).catch(err => { statusEl.textContent = 'Failed to set filter.'; statusEl.className = 'error'; });
        }

        document.getElementById('captureBtn').addEventListener('click', function() {
            statusEl.textContent = 'Capturing...';
            statusEl.className = '';
            // Send the userId in the body of the POST request
            fetch(FLASK_SERVER_URL + '/capture', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ user_id: userId }) })
                .then(res => res.json()).then(data => {
                    statusEl.textContent = data.success ? data.message : 'Error: ' + data.message;
                    statusEl.className = data.success ? 'success' : 'error';
                    if(data.success) {
                        // Use a small delay to ensure the file is written before updating the gallery
                        setTimeout(updateGallery, 100);
                    }
                }).catch(err => { statusEl.textContent = 'Failed to capture.'; statusEl.className = 'error'; });
        });

        document.getElementById('sunglassesBtn').addEventListener('click', () => setFilter('sunglasses'));
        document.getElementById('puppyBtn').addEventListener('click', () => setFilter('puppy'));
        document.getElementById('lipstickBtn').addEventListener('click', () => setFilter('lipstick'));
        document.getElementById('crownBtn').addEventListener('click', () => setFilter('crown'));
        document.getElementById('clearBtn').addEventListener('click', () => setFilter('none'));

        window.addEventListener('load', updateGallery);
    </script>

</body>
</html>
