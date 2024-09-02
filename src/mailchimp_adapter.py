import os
import logging
from dotenv import load_dotenv
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class MailchimpAdapter:
    """
    Adapter for interacting with Mailchimp API v3.

    Note: The API uses 'list_id' that refers to what the GUI calls 'audience_id'.
    Static segments created through this API appear as Tags in the Mailchimp GUI.
    """

    def __init__(self):
        self.mailchimp_user_id = os.environ.get("MAILCHIMP_USER_ID")
        print(self.mailchimp_user_id)
        self.mailchimp_api_key = os.environ.get("MAILCHIMP_API_KEY")
        print(self.mailchimp_api_key)
        self.list_id = os.environ.get("MAILCHIMP_LIST_ID")  # This corresponds to the AUDIENCE_ID in the Mailchimp GUI
        if not self.mailchimp_user_id or not self.mailchimp_api_key or not self.list_id:
            raise ValueError(
                "MAILCHIMP_USER_ID and MAILCHIMP_API_KEY and MAILCHIMP_LIST_ID must be set in environment variables")

        self.client = MailChimp(mc_api=self.mailchimp_api_key, mc_user=self.mailchimp_user_id)

    def process_emails(self, emails, tag_name):
        """Process a list of emails and add them to a specified tag."""
        tag_id = self.ensure_tag(tag_name)
        if not tag_id:
            raise Exception(f"Failed to ensure '{tag_name}' tag")

        for email in emails:
            self.add_contact(email, tag_id, tag_name)

    def ensure_tag(self, tag_name):
        """Ensure a tag exists, creating it if necessary."""
        try:
            logger.info(f"Checking for '{tag_name}' tag")
            segments = self.client.lists.segments.all(self.list_id, get_all=True)

            segment = next((seg for seg in segments['segments'] if seg['name'] == tag_name), None)

            if not segment:
                logger.info(f"Creating '{tag_name}' tag")
                segment = self.client.lists.segments.create(self.list_id, {
                    'name': tag_name,
                    'static_segment': []
                })

            tag_id = segment['id']
            logger.info(f"Successfully ensured '{tag_name}' tag exists with ID: {tag_id}")
            return tag_id
        except MailChimpError as e:
            logger.error(f"MailChimp API error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    def add_contact_to_list(self, email):
        """Add a contact to the Mailchimp list."""
        try:
            logger.info(f"Adding contact: {email} to list id {self.list_id}")
            member = self.client.lists.members.create_or_update(self.list_id, email, {
                'email_address': email,
                'status_if_new': 'subscribed'
            })
            logger.info(f"Successfully added {email} to the list.")
            return member
        except MailChimpError as e:
            logger.error(f"MailChimp API error adding {email} to list: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error adding {email} to list: {str(e)}")
            return None

    def add_contact_to_tag(self, email, tag_id, tag_name):
        """Add a contact to a specific tag."""
        try:
            logger.info(f"Adding contact: {email} to the tag {tag_id}")
            self.client.lists.segments.members.create(self.list_id, tag_id, {
                'email_address': email,
                'status': 'subscribed'
            })
            logger.info(f"Successfully added {email} to the '{tag_name}' tag.")
            return True
        except MailChimpError as e:
            logger.error(f"MailChimp API error adding {email} to tag: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error adding {email} to tag: {str(e)}")
            return False

    def add_contact(self, email, tag_id, tag_name):
        """Add a contact to both the list and a specific tag."""
        member = self.add_contact_to_list(email)
        if member:
            return self.add_contact_to_tag(email, tag_id, tag_name)
        return False