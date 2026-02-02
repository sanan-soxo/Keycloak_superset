# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import os
import sys

from celery.schedules import crontab
from flask_caching.backends.filesystemcache import FileSystemCache
from flask_appbuilder.security.manager import AUTH_OAUTH

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Database configuration
# ---------------------------------------------------------
DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

# ---------------------------------------------------------
# Redis & Cache
# ---------------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG

# ---------------------------------------------------------
# Celery
# ---------------------------------------------------------
class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.thumbnails",
        "superset.tasks.cache",
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        }
    }

CELERY_CONFIG = CeleryConfig

# ---------------------------------------------------------
# Superset core settings
# ---------------------------------------------------------
FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
}

AUTH_ROLE_ADMIN = "Admin"
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
SQLLAB_CTAS_NO_LIMIT = True

WEBDRIVER_BASEURL = "http://superset:8088/"
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL
                                                                      
# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------
LOG_LEVEL = getattr(
    logging,
    os.getenv("SUPERSET_LOG_LEVEL", "INFO").upper(),
    logging.INFO,
)

# ---------------------------------------------------------
# AUTHENTICATION — KEYCLOAK (OIDC)
# ---------------------------------------------------------
AUTH_TYPE = AUTH_OAUTH
AUTH_DISABLE_LOCAL_LOGIN = True

AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"
AUTH_USER_REGISTRATION_ROLE = "Public"


AUTH_ROLES_SYNC_AT_LOGIN = True



AUTH_OAUTH_USER_INFO_URL = (
    "http://127.0.0.1:8080/realms/superset/protocol/openid-connect/userinfo"
)

AUTH_ROLES_MAPPING = {
    "default-roles-superset": ["Gamma"],
    "KeycloakAdmin": ["Admin"],
    "KeycloakAlpha": ["Alpha"],
    "KeycloakGamma": ["Gamma"],
    "superset-public": ["Public"],

}
def oauth_user_info(provider, response=None):
    if provider == "keycloak":
        return {
            "username": response.get("preferred_username"),
            "email": response.get("email"),
            "first_name": response.get("given_name"),
            "last_name": response.get("family_name"),
            "role_keys": response.get("roles", []),
        }

AUTH_USER_INFO_FUNC = oauth_user_info


OAUTH_PROVIDERS = [
    {
        "name": "keycloak",
        "label": "Login with Keycloak",
        "icon": "fa-key",
        "token_key": "access_token",
        "remote_app": {
            "client_id": "superset-client",
            "client_secret": "17ZigzjkWyy6oWpVfGgY5rIzsfijBh8Q",
            "client_kwargs": {"scope": "openid email profile"},
            "access_token_url": "http://127.0.0.1:8080/realms/superset/protocol/openid-connect/token",
            "authorize_url": "http://127.0.0.1:8080/realms/superset/protocol/openid-connect/auth",
            "api_base_url": "http://127.0.0.1:8080/realms/superset/protocol/openid-connect/",
            "userinfo_endpoint": "userinfo",
        },
    }
]


# ---------------------------------------------------------
# Cypress (optional)
# ---------------------------------------------------------
if os.getenv("CYPRESS_CONFIG") == "true":
    base_dir = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(base_dir, "../../tests/integration_tests/"))
    from superset_test_config import *  # noqa
    sys.path.pop(0)

# ---------------------------------------------------------
# Optional docker override
# ---------------------------------------------------------
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded Docker override config from {superset_config_docker.__file__}"
    )
except ImportError:
    logger.info("No superset_config_docker.py override found")
