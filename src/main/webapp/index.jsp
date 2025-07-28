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
        .video-container {
            margin: 20px auto;
            border: 5px solid #555;
            border-radius: 10px;
            width: 640px;
            height: 480px;
            overflow: hidden;
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
            background-color: #000;
        }
        img { display: block; width: 100%; height: 100%; }
        .controls { margin: 20px; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
        button {
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            border-radius: 8px;
            border: none;
            color: white;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        #captureBtn { background-color: #4CAF50; } /* Green */
        #sunglassesBtn { background-color: #008CBA; } /* Blue */
        #puppyBtn { background-color: #f44336; } /* Red */
        #clearBtn { background-color: #555; } /* Grey */
        #status { margin-top: 15px; font-weight: bold; min-height: 22px; font-size: 1.1em; }
        .success { color: #2a9d8f; }
        .error { color: #e76f51; }
    </style>
</head>
<body>
    <h1>Live Camera Feed with Filters 🐶</h1>
    <p>Select a filter to apply it to the live video stream.</p>
    
    <div class="video-container">
        <img src="http://127.0.0.1:5000/video_feed" width="640" height="480" alt="Live video feed">
    </div>

    <div class="controls">
        <button id="sunglassesBtn">😎 Sunglasses</button>
        <button id="puppyBtn">🐶 Puppy Ears</button>
        <button id="clearBtn">🚫 Clear Filter</button>
        <button id="captureBtn">📸 Capture Photo</button>
    </div>
    <p id="status"></p>

    <script>
        const statusEl = document.getElementById('status');
        const FLASK_SERVER_URL = 'http://127.0.0.1:5000';

        // --- Function to set the active filter ---
        function setFilter(filterName) {
            statusEl.textContent = `Setting filter to ${filterName}...`;
            statusEl.className = '';

            // --- Use string addition (+) to avoid JSP conflicts ---
            fetch(FLASK_SERVER_URL + '/set_filter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filter: filterName })
            })
            .then(response => response.json())
            .then(data => {
                statusEl.textContent = data.success ? data.message : 'Error: ' + data.message;
                statusEl.className = data.success ? 'success' : 'error';
            })
            .catch(error => {
                console.error('Filter Error:', error);
                statusEl.textContent = 'Failed to connect to the server to set filter.';
                statusEl.className = 'error';
            });
        }

        // --- Event Listeners for Filter Buttons ---
        document.getElementById('sunglassesBtn').addEventListener('click', () => setFilter('sunglasses'));
        document.getElementById('puppyBtn').addEventListener('click', () => setFilter('puppy'));
        document.getElementById('clearBtn').addEventListener('click', () => setFilter('none'));

        // --- Event Listener for Capture Button ---
        document.getElementById('captureBtn').addEventListener('click', function() {
            statusEl.textContent = 'Capturing...';
            statusEl.className = '';

            // --- Use string addition (+) to avoid JSP conflicts ---
            fetch(FLASK_SERVER_URL + '/capture', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                statusEl.textContent = data.success ? data.message : 'Error: ' + data.message;
                statusEl.className = data.success ? 'success' : 'error';
            })
            .catch(error => {
                console.error('Capture Error:', error);
                statusEl.textContent = 'Failed to connect to the server for capture.';
                statusEl.className = 'error';
            });
        });
    </script>

</body>
</html>
