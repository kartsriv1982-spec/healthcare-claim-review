import os


class Settings:

    # ======================================
    # FastAPI
    # ======================================

    API_HOST = os.getenv(
        "API_HOST",
        "0.0.0.0"
    )

    API_PORT = int(
        os.getenv(
            "API_PORT",
            "8000"
        )
    )

    # ======================================
    # Database
    # ======================================

    DB_HOST = os.getenv(
        "DB_HOST",
        "localhost"
    )

    DB_PORT = int(
        os.getenv(
            "DB_PORT",
            "5432"
        )
    )

    DB_NAME = os.getenv(
        "DB_NAME",
        "healthcare_claims"
    )

    DB_USER = os.getenv(
        "DB_USER",
        "admin"
    )

    DB_PASSWORD = os.getenv(
        "DB_PASSWORD",
        "admin123"
    )

    # ======================================
    # AWS
    # ======================================

    AWS_REGION = os.getenv(
        "AWS_REGION",
        "us-east-1"
    )

    S3_BUCKET = os.getenv(
        "S3_BUCKET"
    )

    # ======================================
    # OpenAI
    # ======================================

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )

    # ======================================
    # RAG
    # ======================================

    COVERAGE_DOC_PATH = os.getenv(
        "COVERAGE_DOC_PATH"
    )

    COVERAGE_RAG_PATH = os.getenv(
        "COVERAGE_RAG_PATH"
    )


settings = Settings()