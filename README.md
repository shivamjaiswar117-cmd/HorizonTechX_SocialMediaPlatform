# Loop: Django social media platform

Features: user profiles (bio, avatar URL), posts and comments, like/unlike (no page reload),
follow/unfollow, a feed of followed users, people directory, registration/login/logout, admin panel.

## Run

    python -m venv venv
    venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations network
    python manage.py migrate
    python manage.py seed          # demo users alice, bob, carol (password: demo12345)
    python manage.py runserver

Open http://127.0.0.1:8000/

## Database tables
User (Django built-in), Profile, Post (with likes), Comment, Follow (followers)
