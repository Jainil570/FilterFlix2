# 🎥 FilterFlix: Real-Time AR Video Filter Engine

FilterFlix is a high-performance web app that applies augmented reality (AR) filters (e.g., sunglasses, puppy ears, lipstick) in **real-time** to a webcam feed using a modern **microservices architecture**. It features a **Flask + OpenCV + MediaPipe** backend and a **Java (JSP)** front-end with Dockerized deployment.

---

## 🚀 Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>
  <img src="https://img.shields.io/badge/MediaPipe-007F7F?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white"/>
</p>

---

## 🌐 Live Demo

🔗 [Click here to try FilterFlix online](#) <!-- Replace with actual Render link -->

---

## 🖼️ Interface Preview

<p align="center">
  <img src="https://github.com/user-attachments/assets/33f9a240-2c54-4ed0-be04-0b608203a536" width="640" alt="FilterFlix Logo"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b36d62c5-31f2-4b35-ab3c-378717198590" width="100%" alt="Screenshot 1"/>
  <br/><em>Interactive front-end interface deployed via Render</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/030eb196-d0a7-4887-b935-3e12d023dbe2" width="100%" alt="Screenshot 2"/>
  <br/><em>Real-time AR filters with face tracking</em>
</p>

---

## 🧠 Core Features

- 🎯 **Real-Time Video Filters** — Webcam feed processed with minimal latency.
- 🧩 **Modular Microservices** — Decoupled front-end and back-end architecture.
- 🎨 **Dynamic AR Filter Overlays** — Includes sunglasses, puppy ears, lipstick, and crown filters.
- 🧠 **468-point Face Tracking** — Powered by MediaPipe’s 3D face mesh.
- 💡 **Head Pose Estimation** — Dynamic resizing and orientation of filters.
- 📸 **Capture + Download** — Users can capture filtered frames and download them individually or as ZIP.
- ☁️ **Cloud Native** — Dockerized, CI/CD-ready, deployed on Render.

---

## 🖼️ Available Filters

| Sunglasses 😎 | Puppy Ears 🐶 | Crown 👑 | Lipstick 💄 |
|:-------------:|:-------------:|:--------:|:-----------:|
| *(Live AR Overlay)* | *(Live AR Overlay)* | *(Live AR Overlay)* | *(Live AR Overlay)* |

---

## ⚙️ Architecture Overview

```plaintext
+----------------------------+
|  User's Browser (JSP UI)  |
+----------------------------+
              |
       HTTP / Video Feed
              |
+----------------------------+
|  Java Front-End (Tomcat)  |
|  + HTML + JS (JSP)        |
+----------------------------+
              |
   API Calls / Stream Proxy
              |
+----------------------------+
| Python Flask Back-End     |
| + OpenCV + MediaPipe      |
+----------------------------+
