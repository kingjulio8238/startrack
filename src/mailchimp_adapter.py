import os
import logging
from dotenv import load_dotenv
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class MailchimpAdapter:
    def __init__(self):
        self.api_key = os.environ.get("MAILCHIMP_API_KEY")
        self.list_id = os.environ.get("MAILCHIMP_AUDIENCE_ID")
        if not self.api_key or not self.list_id:
            raise ValueError("MAILCHIMP_API_KEY and MAILCHIMP_AUDIENCE_ID must be set in environment variables")

        self.client = MailChimp(mc_api=self.api_key, mc_user='apikey')

    def process_emails(self, emails, group_name):
        group_id = self.ensure_group(group_name)
        if not group_id:
            raise Exception(f"Failed to ensure '{group_name}' group")

        for email in emails:
            self.add_contact(email, group_id, group_name)

    def ensure_group(self, group_name):
        try:
            logger.info(f"Checking for '{group_name}' group")
            groups = self.client.lists.segments.all(self.list_id, get_all=True)

            group = next((group for group in groups['segments'] if group['name'] == group_name), None)

            if not group:
                logger.info(f"Creating '{group_name}' group")
                group = self.client.lists.segments.create(self.list_id, {
                    'name': group_name,
                    'static_segment': []
                })

            group_id = group['id']
            logger.info(f"Successfully ensured '{group_name}' group exists with ID: {group_id}")
            return group_id
        except MailChimpError as e:
            logger.error(f"MailChimp API error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    def add_contact(self, email, group_id, group_name):
        try:
            logger.info(f"Adding contact: {email}")
            member = self.client.lists.members.create_or_update(self.list_id, email, {
                'email_address': email,
                'status_if_new': 'subscribed'
            })

            self.client.lists.segments.members.create(self.list_id, group_id, {
                'email_address': email,
                'status': member['status']
            })

            logger.info(f"Successfully added {email} to the list and '{group_name}' group.")
            return True
        except MailChimpError as e:
            logger.error(f"MailChimp API error adding {email}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error adding {email}: {str(e)}")
            return False
