# Kritiflow:Smart Feedback Collection & Analysis System

**Live Demo:** [https://smart-feedback-system-dmyi.onrender.com](https://smart-feedback-system-dmyi.onrender.com)

A comprehensive **Full Stack** feedback management platform that utilizes **AI (NLP)** to analyze user sentiment in real-time. Features a secure verified user system, a modern glassmorphism UI, and an interactive admin dashboard for data-driven insights. This project integrates a robust **Flask** backend with a dynamic **Frontend** and **MongoDB** database to deliver a seamless user experience.

## 🚀 Features

*   **Real-time Sentiment Analysis**: Automatically processes feedback text to categorize it as **Positive**, **Neutral**, or **Negative** using TextBlob.
*   **User Management & Verification**:
    *   **Registration & Login**: Secure authentication system.
    *   **Profile Verification**: Users can submit employment details (Name, Dept, Employee ID, Organization) for Admin verification.
    *   **Password Management**: Secure "Change Password" functionality for all users.
*   **Admin Dashboard**:
    *   **Overview**: View global sentiment distribution via interactive charts (Chart.js).
    *   **User Management**: View all registered users, verify user profiles, and update user details (Department, Organization, etc.).
*   **Role-Based Access Control (RBAC)**:
    *   **Admin**: Full access to user management and global analytics.
    *   **User**: Submit feedback, view personal feedback history, and manage verified profile.
*   **Modern UI/UX**:
    *   Responsive Glassmorphism design.
    *   Smooth entry animations and interactive elements.

## 🛠 Tech Stack

*   **Backend**: Flask (Python), SQLAlchemy / MongoEngine
*   **Database**: MongoDB (via `flask-mongoengine`)
*   **AI/ML**: TextBlob (Natural Language Processing)
*   **Frontend**: HTML5, CSS3 (Custom Glassmorphism), JavaScript
*   **Visualization**: Chart.js

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📂 Project Structure

```
TCS Project/
├── app.py              # Main Flask application entry point
├── models.py           # Database models (User, Feedback)
├── analysis.py         # Sentiment analysis logic
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment configuration (e.g., for Render/Heroku)
├── static/             # Static assets (CSS, JS, Images)
├── templates/          # HTML templates (Jinja2)
├── tests/              # Unit tests
└── scripts/            # Utility scripts (e.g., db checks)
```

## ⚙️ Configuration

1.  **Environment Variables**:
    Create a `.env` file in the root directory to manage sensitive configuration:

    ```env
    MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/dbname
    SECRET_KEY=your_secure_secret_key
    ```
    *(Note: Replace the placeholder values with your actual MongoDB connection string and a strong secret key)*

## 🏃 Setup & Run

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Karankumawa/smart-feedback-system.git
    cd smart-feedback-system
    ```

2.  **Create Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Ensure your `.env` file is set up as described in the **Configuration** section.

5.  **Run the Application**
    ```bash
    python app.py
    ```
    The application will be available at `http://localhost:5001`.

## 🧪 Testing

The project includes basic unit tests located in the `tests/` directory.

To run tests:
```bash
python -m pytest tests/
```
*Or simply run the test file directly:*
```bash
python tests/test_basic.py
```

## 🚀 Deployment

This application includes a `Procfile` for easy deployment on platforms like **Render** or **Heroku**.

1.  Push your code to a GitHub repository.
2.  Connect your repository to Render/Heroku.
3.  Add the environment variables (`MONGODB_URI`, `SECRET_KEY`) in the dashboard of your hosting provider.
4.  Deploy!

---
*Developed by Karan*
