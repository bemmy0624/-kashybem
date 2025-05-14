class Config:
    # Database configuration
    DB_HOST = "localhost"  # Change if you're using a remote database
    DB_USER = "root"  # Your MySQL username
    DB_PASSWORD = "password"  # Your MySQL password
    DB_NAME = "kate"  # Change this to the correct database name

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking for performance
