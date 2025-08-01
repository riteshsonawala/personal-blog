# Personal Blog Project

This is a complete Flask blog application ready for deployment on AWS.

## Project Structure
```
personal-blog/
├── app.py                     # Main Flask application
├── pyproject.toml            # Poetry configuration
├── README.md                 # Project documentation
├── requirements.txt          # pip requirements (generated from Poetry)
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore file
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose for local development
├── gunicorn.conf.py         # Gunicorn configuration
├── aws/
│   ├── buildspec.yml        # AWS CodeBuild configuration
│   ├── appspec.yml          # AWS CodeDeploy configuration
│   └── eb-config/           # Elastic Beanstalk configuration
│       └── .ebextensions/
│           └── python.config
└── templates/
    ├── base.html            # Base template
    ├── index.html           # Home page
    ├── about.html           # About page
    ├── post_detail.html     # Individual post view
    ├── write_post.html      # Create new post
    └── edit_post.html       # Edit existing post
```

## Features
- ✅ Create, read, update, delete blog posts
- ✅ Markdown support with syntax highlighting
- ✅ Responsive modern design
- ✅ SQLite database (easily switchable to PostgreSQL for production)
- ✅ Form validation and CSRF protection
- ✅ Ready for AWS deployment
- ✅ Docker support
- ✅ Production-ready with Gunicorn

## Quick Start

### 1. Install Dependencies
```bash
# Using Poetry (recommended)
poetry install
poetry shell

# Or using pip
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run Locally
```bash
# Development mode
flask run

# Or with Gunicorn (production-like)
gunicorn app:app
```

### 4. Deploy to AWS
See the deployment guides in the aws/ folder for different deployment options.

## Customization
1. Update the About page in `templates/about.html` with your information
2. Modify the blog title and branding in `templates/base.html`
3. Adjust styling in the base template CSS section
4. Configure environment variables for production

## Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `PORT`: Port to run the application (default: 5000)

The application is ready to deploy on AWS using Elastic Beanstalk, ECS, or EC2!