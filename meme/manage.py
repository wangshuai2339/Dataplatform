#!/usr/bin/env python
import os
import sys

# cd meme && python manage.py runserver 192.168.31.79:8000
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meme.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
