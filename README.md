# URL Shortening Service

A Django REST Framework-based URL shortening service that allows users to create, manage, and track shortened URLs with authentication and statistics.

## Features

- 🔗 **URL Shortening**: Create short, memorable links from long URLs
- 👤 **User Authentication**: JWT-based authentication system with user registration and login
- 📊 **Link Statistics**: Track access statistics for shortened links
- 🔒 **Access Control**: Users can only manage their own links
- 🐳 **Docker Support**: Containerized application with Dockerfile
- 📝 **RESTful API**: Clean, documented API endpoints
- 🗄️ **PostgreSQL Database**: Robust data persistence

## Tech Stack

- **Backend**: Django 5.2.8, Django REST Framework 3.16.1
- **Authentication**: JWT (Simple JWT), Djoser
- **Database**: PostgreSQL (via psycopg2-binary)
- **Server**: Gunicorn
- **Containerization**: Docker

## Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Docker (optional, for containerized deployment)

## Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/dmitriy-zverev/link-shortener.git
   cd link-shortener
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   
   Create a PostgreSQL database and user for the project.

5. **Configure environment variables**
   
   Create a `.env` file in the `link_shortener` directory or set the following environment variables:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_NAME=link_shortener_db
   DATABASE_USER=your_db_user
   DATABASE_PASSWORD=your_db_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

6. **Run migrations**
   ```bash
   cd link_shortener
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000`

## Docker Deployment

This project includes a Dockerfile for the application service, but **does not include a database Dockerfile**. When creating a `docker-compose.yml` file, you'll need to include the PostgreSQL database service yourself.

### Example docker-compose.yml

Here's a sample `docker-compose.yml` you can create:

```yaml
services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=link_shortener_db
      - POSTGRES_USER=link_shortener_user
      - POSTGRES_PASSWORD=your_secure_password
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U link_shortener_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    command: sh -c "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 link_shortener.wsgi:application"
    volumes:
      - ./link_shortener:/app
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-secret-key-here
      - DEBUG=False
      - DATABASE_NAME=link_shortener_db
      - DATABASE_USER=link_shortener_user
      - DATABASE_PASSWORD=your_secure_password
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
```

### Running with Docker Compose

```bash
# Build and start services
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## API Documentation

### Authentication Endpoints

- `POST /users/` - Register a new user
- `POST /auth/token/login/` - Login (obtain JWT tokens)
- `POST /auth/token/logout/` - Logout

### Link Management Endpoints

- `GET /s/` - List all links (authenticated user's links)
- `POST /s/` - Create a new short link
- `GET /s/{short_code}/` - Redirect to the url page
- `PUT /s/{short_code}/` - Update a link
- `PATCH /s/{short_code}/` - Partially update a link
- `DELETE /s/{short_code}/` - Delete a link
- `GET /s/{short_code}/detail/` - Get link statistics

### Making Authenticated Requests

Include the JWT token in the Authorization header:

```bash
curl -H "Authorization: Token <your_access_token>" http://localhost:8000/s/
```

### Example: Creating a Short Link

```bash
curl -X POST http://localhost:8000/s/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/very-long-url"
  }'
```

## Project Structure

```
link-shortener/
├── Dockerfile              # Docker configuration for the application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── data/                  # Postman collection
├── link_shortener/        # Django project root
│   ├── manage.py
│   ├── link_shortener/    # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core/              # Main app (links, statistics)
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── utils.py
│   └── users/             # User management app
│       ├── models.py
│       ├── views.py
│       └── serializers.py
```

## Database Schema

### Link Model
- `url` - The original long URL
- `short_code` - The shortened code (unique)
- `author` - Foreign key to User
- `created_at` - Timestamp of creation
- `updated_at` - Timestamp of last update

### LinkStatistic Model
- `link` - Foreign key to Link
- `user` - Foreign key to User (who accessed the link)
- `created_at` - Timestamp of access

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `False` |
| `DATABASE_NAME` | PostgreSQL database name | `link_shortener_db` |
| `DATABASE_USER` | PostgreSQL user | Required |
| `DATABASE_PASSWORD` | PostgreSQL password | Required |
| `DATABASE_HOST` | PostgreSQL host | `localhost` |
| `DATABASE_PORT` | PostgreSQL port | `5432` |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Project inspired by [roadmap.sh URL Shortening Service](https://roadmap.sh/projects/url-shortening-service) project challenge
- Built with Django and Django REST Framework
- Uses JWT for secure authentication

## Support

If you have any questions or run into issues, please open an issue on GitHub.

---
