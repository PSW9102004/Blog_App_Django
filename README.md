# Django Blog App

A simple, full-featured blogging application built with Django.

## Features
<p align="center">
  <img src="Screenshot 2025-11-30 155405.png" alt="Screenshot" />
</p>
*   **User Authentication:**
    *   User Registration
    *   Login / Logout
    *   Profile Management (Update username, email, and profile picture)
*   **Blog Posts:**
    *   Create, Read, Update, and Delete (CRUD) posts
    *   View all posts on the home page
    *   View individual post details
    *   Pagination for posts
*   **Comments:**
    *   Add comments to posts
*   **Permissions:**
    *   Only authors can edit or delete their own posts
    *   Login required for creating posts and comments
*   **UI/UX:**
    *   Clean and responsive design using custom CSS and Bootstrap (via Crispy Forms)

## Technologies Used

*   **Backend:** Django (Python)
*   **Database:** SQLite (default)
*   **Frontend:** HTML, CSS, Django Templates
*   **Forms:** Django Crispy Forms (Bootstrap 4/5)
*   **Image Processing:** Pillow

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/PSW9102004/Blog_App_Django.git
    cd Blog_App_Django
    ```

2.  **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django django-crispy-forms crispy-bootstrap4 Pillow
    ```

4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a default profile image (if needed):**
    If you encounter errors about missing `default.jpg`, run the included script:
    ```bash
    python create_default_image.py
    ```

6.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

8.  **Access the app:**
    Open your browser and go to `http://127.0.0.1:8000/`

## Usage

*   **Register** a new account.
*   **Login** to access full features.
*   **Update your profile** by clicking on your username or "Profile" in the navigation bar.
*   **Create a new post** using the "New Post" link.
*   **Interact** by reading posts and leaving comments.
