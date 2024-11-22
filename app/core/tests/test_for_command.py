
from unittest.mock import patch
from psycopg2 import OperationalError as psycopg2Error   #  it throws error when the postgres db is not ready
from django.test import SimpleTestCase   # use since we do not need to integrate the db or migrations,we are only testing behaviour
from django.db.utils import OperationalError   # error thrown depending on the start
from django.core.management import call_command   # help us call the commands that we are testing


@patch('core.management.commands.wait_for_db.Command.check')  # this give rise to patched_check
class CommandTest(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):

        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')  # we do not want to add delay in the unit test so that it wont be slow, so we mock it
    def test_wait_for_db_delay(self, patched_sleep, patched_check): 
        """test waiting for database when getting operational error """
        patched_check.side_effect = [psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6) 
        patched_check.assert_called_with(databases=['default'])

