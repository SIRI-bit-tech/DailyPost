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

## Deployment to Railway

### Prerequisites

- Railway account
- PostgreSQL database set up on Railway
- Cloudinary account

### Deployment Steps

1. Run the pre-deployment check script:
   ```
   python clean_and_check.py
   ```

2. Create a new project on Railway

3. Add the PostgreSQL plugin

4. Set up the following environment variables in Railway:
   - `SECRET_KEY` - Secure random string for Django
   - `DEBUG` - Set to False
   - `ALLOWED_HOSTS` - Your app's domain (e.g., yourdomain.com,www.yourdomain.com)
   - `DATABASE_URL` - This should be automatically set by Railway PostgreSQL plugin
   - `CLOUDINARY_CLOUD_NAME` - From your Cloudinary account
   - `CLOUDINARY_API_KEY` - From your Cloudinary account
   - `CLOUDINARY_API_SECRET` - From your Cloudinary account
   - Email configuration variables
   - Other settings from your .env file

5. Connect your GitHub repository to Railway

6. Deploy your app!

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
