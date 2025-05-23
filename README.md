# 🍳 LetEmCook

LetEmCook is a social media web application where users can share their own recipes or generate creative recipes with the help of AI. With features powered by **Google's Gemini AI**, users can input a title and ingredients, and LetEmCook will automatically generate detailed descriptions, instructions, and tags.

## 🌟 Features

- 🧑‍🍳 Share your own unique recipes
- 🤖 Generate descriptions, instructions, and tags using **Gemini AI**
- 🔒 Register and log in securely with **Google or GitHub** using **django-allauth**
- 📝 Comment on recipes and interact with others
- 🏷️ Tag-based filtering (via `django-taggit`)
- 🖼️ User profiles and recipe pages
- 🔐 Email MFA (multi-factor authentication) support

## 🔧 Tech Stack

- **Backend:** Django 5.2
- **Frontend:** HTML/CSS (with Django templates)
- **Database:** PostgreSQL
- **Authentication:** Django Allauth (Google & GitHub providers)
- **AI Integration:** Google Gemini API
- **Deployment:** Render.com
- **Media Storage:** AWS S3 Bucket

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/iFabsss/LetEmCook.git
cd LetEmCook
```

### 2. Set Up Your Environment

Create a `.env` file in the root directory and add the following:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1 localhost letemcook.onrender.com

#If postgre is deployed
DATABASE_URL=your_postgres_database_url
#
#If local postgre DB
DB_NAME='let_em_cook_db'
DB_USER='let_em_cook_user'
DB_PASSWORD='1234'


GEMINI_KEY=your_gemini_api_key
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_secret
SITE_ID=1

#Make an S3 Bucket with IAM with FullS3Access
AWS_ACCESS_KEY_ID='your_iam_access_key' 
AWS_SECRET_ACCESS_KEY='your_iam_secret_key'
AWS_STORAGE_BUCKET_NAME='your_s3_bucket'

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

### 5. Access the App

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🛠 Deployment

LetEmCook is deployed on [Render.com](https://letemcook.onrender.com). Ensure the following environment variables are configured in your Render Dashboard.

## 📸 Screenshots

Coming soon...

## 📄 License

This project is open-source and free to use for educational or personal projects.
