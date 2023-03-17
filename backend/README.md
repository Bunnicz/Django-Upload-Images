# Django Image Hosting

## How to run the project

1. clone the repo
2. create .env file based on .env.example
3. Run docker compose

```bash
docker-compose up --build
```

4. connect to the docker image CLI
5. Make migrations, migrate and create super user:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. Restart docker image if needed
7. Go to "http://127.0.0.1:8000/admin/" and create tiers and users with tier attached.
7. Go to "http://127.0.0.1:8000/api/images" and login. NOTE: Users need to be authenticated (loged in) and have a tier to be able to use API
8. When no longer needed unmount docker image:

```bash
docker-compose down
```

9. NOTE: In requirements.txt libraries for tests and formating were commented out. If you want you can bring them back.

## API endpoints

1. You can check detailed swagger documentation at localhost:5000/apidocs

2. GET "http://127.0.0.1:8000/api-auth/login/" - returns csrf token
3. POST "http://127.0.0.1:8000/api-auth/login/" - login user

```json
{
    {
        "X-CSRFToken": <csrftoken>
},
    {
        "username": <str>,
        "password": <str>
    }
}
```

4. GET "http://127.0.0.1:8000/api-auth/logout/" - logout user

5. GET "http://127.0.0.1:8000/api/images" - returns current user images if images exist depending on user tier:

```json
{
    {
        "id": <uuid>,
        "img_px200": <image_url>,
        "img_px400": <optional:image_url>,
        "img_native": <optional:image_url>,
        "temp_url": <optional:image_url>,
        "delete_url_time_left_second": <optional:int>
    }
}
```

6. POST "http://127.0.0.1:8000/api/images" - upload image. Users with generated_url tier can add time in seconds after which temp_url will expire (default between 300 and 30_000 seconds):

```json
{
    {
        "X-CSRFToken": <csrftoken>
},
    {
        "image": <image>,
        "delete_url_time": <optional:int>
    }
}
```

## Image Validation

1. During uploading file, image is validated by django build-in "FileExtensionValidator" to validate that the file extension is supported by Pillow. "validate_image_file_extension"

2. Custom validators in "validators.py" file:

- validate_image() - checks if:
-- image is present
-- image file size is less than 3 MB (settings.py)
-- image extension is .jpg or .png. NOTE: Just checks the filename extension not the acctual extension. It's required by django documentation not to rely on this type of validation. "Files can be renamed to have any extension no matter what data they contain." <https://docs.djangoproject.com/en/4.1/ref/validators/#fileextensionvalidator>
