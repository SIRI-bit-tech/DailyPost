# Daily Record News Website

A modern Django-based news website with Cloudinary integration for media handling.

## Features

- Responsive, mobile-friendly design
- Full content management system
- Cloudinary integration for media storage
- SEO optimization
- Newsletter subscription
- Contact forms
- Comment system

## Local Development

1. Clone the repository
2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Deployment to Render

### Prerequisites

- [Render](https://render.com) account
- PostgreSQL database set up on Render
- Cloudinary account

### Deployment Steps

1. Run the pre-deployment check script:
   ```
   python clean_and_check.py
   ```

2. Sign up for a Render account if you don't have one already

3. Create a new Web Service on Render
   - Connect your GitHub repository
   - Select the branch to deploy
   - Use "Python" as the Environment
   - Set the Build Command: `./build.sh`
   - Set the Start Command: `gunicorn dailyrecord.wsgi:application`

4. Set up the following environment variables in Render dashboard:
   - `SECRET_KEY` - Secure random string for Django
   - `DEBUG` - Set to False
   - `ALLOWED_HOSTS` - Your app's domain (e.g., yourdomain.onrender.com)
   - `CLOUDINARY_CLOUD_NAME` - From your Cloudinary account
   - `CLOUDINARY_API_KEY` - From your Cloudinary account
   - `CLOUDINARY_API_SECRET` - From your Cloudinary account
   - Email configuration variables
   - Other settings from your .env file

5. Create a PostgreSQL database in Render
   - In your Render dashboard, go to "New +" and select "PostgreSQL"
   - Give it a name and create it
   - Render will automatically provide the `DATABASE_URL` to your web service

6. Create a Redis instance in Render (if needed)
   - In your Render dashboard, go to "New +" and select "Redis"
   - Give it a name and create it
   - Render will automatically provide the `REDIS_URL` to your web service

7. Deploy your app!

### Post-Deployment

1. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

2. Run migrations if needed:
   ```
   python manage.py migrate
   ```

## Important Files

- `dailyrecord/settings.py` - Main Django settings
- `news/models.py` - Database models
- `news/views.py` - View controllers
- `templates/` - HTML templates

## Website Preview
https://www.thedailyrecordpost.com
![ScreenShot Tool -20250408094348](https://github.com/user-attachments/assets/34d85a6f-8859-4735-8750-f5fa98f249a0)
![ScreenShot Tool -20250408094647](https://github.com/user-attachments/assets/c59d509e-7d5c-47a1-b585-d664a93f9bb6)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
