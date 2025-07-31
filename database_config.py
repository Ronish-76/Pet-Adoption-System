"""
Database configuration for Pet Adoption Platform
Update Django settings to use this MySQL database
"""

# Add this to your Django settings.py DATABASES configuration
DATABASES_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pet_adoption_db',
        'USER': 'root',  # Change this to your MySQL username
        'PASSWORD': '',  # Change this to your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

# MySQL connection parameters for direct connections
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': '',  # Change this to your MySQL password
    'database': 'pet_adoption_db',
    'port': 3306
}