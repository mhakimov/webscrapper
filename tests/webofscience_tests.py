import unittest
from webofscience.webofscience import Webofscience
import constants as const

class Webofscience_test(unittest.TestCase):

    def test_all_scrapped_emails_are_unique(self):
        with Webofscience() as bot:
            authors = bot.read_old_csv(const.ROOT_DIR + '/' + const.GENERATED_RECORDS_FILE)
            unique_authors = []
            for a in authors:
                exists = False
                for ua in unique_authors:
                    if a.email.lower() == ua.email.lower():
                        exists = True
                        break
                if not exists:
                    unique_authors.append(a)
            self.assertEqual(len(authors), len(unique_authors))


