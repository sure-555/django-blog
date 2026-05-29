import os
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

application = get_wsgi_application()

# --- TEMPORARY MIGRATION KICKER ---
# This runs the data load from inside the active app context
try:
    print("Core Migration: Attempting to inject cloud data fixtures...")
    call_command('loaddata', 'datadump.json')
    print("Core Migration: Success! Data fully populated.")
except Exception as e:
    print(print(f"Core Migration Note: {e}"))