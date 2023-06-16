# Altered Carbon API

This project is a Django REST API that provides endpoints for viewing and editing user, group, error log, update check, and firmware data. It includes viewsets for each of these models, which handle standard CRUD (create, read, update, delete) operations through various HTTP methods. The serializers define how the model instances are converted to JSON format for use in the API.

This project could be used as a backend for a variety of web or mobile applications that need to store and retrieve data related to users, groups, and firmware. By providing an API, developers can easily communicate with the backend without needing to worry about database management or low-level networking code. Additionally, this project uses Django's built-in authentication and permission classes to ensure that only authorized users can access the API, which improves security. Overall, this project provides a robust backend for managing and storing data in a secure and standardized way.

- [Altered Carbon API](#altered-carbon-api)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Environment Variables (Optional)](#environment-variables-optional)
  - [License](#license)
  
## Prerequisites

Before you begin, make sure you have the following installed:

- Python (3.10.0)
- pip (package installer for Python)
- PostgreSQL (optional, if using PostgreSQL as the database)

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/project-name.git
```


2. Change into the project directory:

```
cd project-name
```

3. Create a virtual environment:

```
python -m venv env
```

4. Activate the virtual environment:

- For Windows:

  ```
  .\env\Scripts\activate
  ```

- For macOS/Linux:

  ```
  source env/bin/activate
  ```

5. Install the project dependencies:

```
pip install -r requirements.txt
```

6. Run database migrations:

```
python manage.py migrate
```

## Configuration

Before running the project, you need to configure the necessary settings.

1. Create a new file named `.env` in the project root directory.

2. Open the `.env` file and set the following environment variables:

```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
```

Make sure to replace your-secret-key and your-database-url with your actual values. Refer to the Environment Variables section for more information.

Save and close the .env file.

## Usage
To start the development server, run the following command:

```
python manage.py runserver
```

The project will be accessible at `http://localhost:8000`.


### Environment Variables (Optional)
The following environment variables are used in the project:

```
SECRET_KEY: A secret key used for cryptographic signing. It should be a long and randomly generated string.
DEBUG: Set to True to enable debugging mode. In production, set it to False.
DATABASE_URL: The URL or connection string for your database. For example, for PostgreSQL: postgres://username:password@localhost/database.
```
You may need to add additional environment variables depending on the project's requirements.


## License
MIT License

