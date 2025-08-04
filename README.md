# FilterFlix: Real-Time AR Video Filter Engine


<img width="640" height="515" alt="Screenshot 2025-07-25 133128" src="https://github.com/user-attachments/assets/33f9a240-2c54-4ed0-be04-0b608203a536" />

FilterFlix is a high-performance web application that demonstrates a sophisticated microservices architecture for applying real-time, augmented reality (AR) filters to video streams. The system leverages a powerful Python back-end for intensive computer vision tasks and a decoupled Java front-end for user interaction, showcasing a modern approach to building complex, interactive media applications.

Live Demo: [Link to your deployed front-end on Render]

Visual Showcase
<p align="center">
<em>Application Interface - Deployed on Render</em>
<br>
<img width="1349" height="610" alt="image" src="https://github.com/user-attachments/assets/b36d62c5-31f2-4b35-ab3c-378717198590" />
</p>
<br>
<img width="1353" height="609" alt="image" src="https://github.com/user-attachments/assets/030eb196-d0a7-4887-b935-3e12d023dbe2" />
The Technology in Action
The core of FilterFlix is its ability to accurately map facial landmarks and apply transformations in real time.

Face Detection & Mesh Generation

Filter Application

High-fidelity facial landmarks detected by MediaPipe.
![captured_photo_0003](https://github.com/user-attachments/assets/9740ebf8-57f5-46d5-8d9c-d70e340b0b35)
Geometric transformations applied to overlay AR assets.

![captured_photo_0004](https://github.com/user-attachments/assets/9ca51edc-4347-4fec-91a3-42686838375d)

<img width="640" height="515" alt="Screenshot 2025-07-25 133128" src="https://github.com/user-attachments/assets/9209a5f6-e67f-4b56-a391-202c5f3d47e0" />

Available Filters
A collection of dynamically applied AR filters, each with unique positioning and scaling logic.

Sunglasses

Puppy Ears

Crown

Lipstick

<img src="![capture_3_20250804_151656](https://github.com/user-attachments/assets/5dd12e1c-723c-4256-b8bd-9da6506d954b)"/>

<img src="![capture_3](https://github.com/user-attachments/assets/19a6f347-a8b9-4586-a18b-e634a60dd523)"/>

<img src="![capture_1_20250804_151605](https://github.com/user-attachments/assets/7c97ad98-b216-4aa7-b990-b70e207c654d)"/>

<img src="![capture_1](https://github.com/user-attachments/assets/50098059-d232-480d-a686-5c703f387f74)"/>

Core Features
Real-Time Video Processing: Ingests a video stream and applies complex filters frame-by-frame with minimal latency.

Decoupled Microservices Architecture: A robust Java (JSP) front-end is fully separated from the Python (Flask) back-end, allowing for independent scaling and development.

State-of-the-Art Face Tracking: Utilizes Google's MediaPipe Face Mesh to detect 468 3D facial landmarks for precise filter placement.

Dynamic AR Asset Overlay:

Calculates head rotation, tilt, and distance to dynamically resize and orient filter assets.

Employs alpha blending to seamlessly overlay transparent PNG assets onto the video stream.

Interactive Web Interface: Users can select filters, capture still images of the filtered stream, and download their creations individually or as a ZIP archive.

Cloud-Native Deployment: Fully containerized with Docker and deployed on the Render cloud platform, demonstrating modern CI/CD practices.

Technology Stack & Architecture
This project is a practical implementation of a distributed system.

Back-End (Python Computer Vision Service)
Framework: Flask (A lightweight WSGI framework for building the API).

Computer Vision:

OpenCV: For core image and video manipulation, including reading frames and color space conversions.

MediaPipe: For high-performance face mesh detection and landmark tracking.

Libraries: NumPy for efficient numerical operations on image data.

Production Server: Gunicorn for running the Flask application in a production environment.

Front-End (Java Web Service)
Language: Java

Web Technology: JavaServer Pages (JSP) for dynamically generating the user-facing HTML.

Server: Deployed on an Apache Tomcat server environment.

Deployment & Infrastructure
Containerization: Docker is used to create a portable, reproducible server environment for the Java front-end.

Cloud Platform: Render for hosting both the Python back-end and the containerized Java front-end, with auto-deploy on Git push.

Version Control: Git & GitHub.

Architectural Diagram
+--------------------------+      HTTP Request      +---------------------------+
|                          |   (Select Filter, etc.)  |                           |
|   User's Browser         +------------------------>|   Java Front-End (Render) |
| (Viewing JSP Page)       |                        | (Dockerized Tomcat)       |
|                          |<------------------------+                           |
+-----------+--------------+      HTML/JS/CSS       +---------------------------+
            |
            | Video Stream & API Calls
            | (CORS Enabled)
            v
+-----------+--------------+
|                          |
| Python Back-End (Render) |
| (Flask, OpenCV,         |
|  MediaPipe)              |
|                          |
+--------------------------+

Setup & Local Development
To run this project on a local machine, you need both a Python environment and a Java web server.

Prerequisites
Python 3.9+

Java JDK 11+

Apache Tomcat 9+

Git

Back-End (Python)
Navigate to the python_server directory.

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the server:

python app.py

The back-end will be running at http://localhost:5000.

Front-End (Java)
Deploy the snapchat2 web application directory to your Apache Tomcat server.

Start the Tomcat server.

Access the application in your browser, typically at http://localhost:8080/snapchat2/.
