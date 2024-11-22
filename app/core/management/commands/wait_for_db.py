"""
Django command to wait for DB
"""
import time
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as psycopg2OpError
from django.db.utils import OperationalError


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Entry point command"""
        self.stdout.write('waiting for database')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])

                db_up = True
            except (psycopg2OpError, OperationalError):
                self.stdout.write('database unvailable. wait for a second ')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('database available'))