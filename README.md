# Smart Feedback Collection & Analysis System

🚀 **Live Demo:** [https://smart-feedback-system-dmyi.onrender.com](https://smart-feedback-system-dmyi.onrender.com)

A comprehensive feedback management platform that uses **AI (NLP)** to analyze user sentiment in real-time. Features a verified user system, glassmorphism UI, and an interactive admin dashboard.

## 🌟 Features

*   **Real-time Sentiment Analysis**: Automatically categorizes feedback as Positive, Neutral, or Negative using TextBlob.
*   **User Verification**: dedicated profile verification flow for users to submit employment details (Name, Dept, Employee ID).
*   **Interactive Dashboard**:
    *   Live sentiment distribution charts (Chart.js).
    *   Admin User Management table to view and verify user status.
    *   Staggered entry animations and responsive design.
*   **Role-Based Access**:
    *   **Admin**: View all users, verify profiles, see global stats.
    *   **User**: Submit feedback, view own history, request verification.

## 🛠️ Tech Stack

*   **Backend**: Flask (Python), SQLAlchemy
*   **AI/ML**: TextBlob (Sentiment Analysis)
*   **Frontend**: HTML5, CSS3 (Custom Glassmorphism), JavaScript
*   **Database**: SQLite

## 📦 Setup & Run

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Karankumawa/smart-feedback-system.git
    cd smart-feedback-system
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    python app.py
    ```
