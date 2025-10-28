#!/usr/bin/env python3
"""
Script to help set up Google Cloud authentication for Heroku deployment.
This script converts a service account JSON file to a base64-encoded string
that can be stored as a Heroku environment variable.
"""

import json
import sys

def setup_heroku_auth(service_account_path: str):
    """
    Read a service account JSON file and convert it to a format suitable for Heroku.
    
    Args:
        service_account_path: Path to the service account JSON file
    """
    try:
        # Read the service account JSON file
        with open(service_account_path, 'r') as f:
            service_account_data = json.load(f)
        
        # Convert to JSON string
        json_string = json.dumps(service_account_data)
        
        print("=" * 60)
        print("HEROKU DEPLOYMENT SETUP")
        print("=" * 60)
        print()
        print("1. Copy the JSON content below:")
        print("-" * 40)
        print(json_string)
        print("-" * 40)
        print()
        print("2. Set this as a Heroku environment variable:")
        print("   heroku config:set GOOGLE_SERVICE_ACCOUNT_JSON='<paste_json_here>'")
        print()
        print("   OR in Heroku Dashboard:")
        print("   Settings → Config Vars → Add:")
        print("   Key: GOOGLE_SERVICE_ACCOUNT_JSON")
        print("   Value: <paste_json_here>")
        print()
        print("3. Make sure these other environment variables are also set:")
        print("   - PROJECT_ID")
        print("   - LOCATION")
        print("   - PROCESSOR_ID")
        print("   - META_API_VERSION")
        print("   - META_VERIFICATION_TOKEN")
        print("   - ACCESS_TOKEN")
        print("   - PHONE_NUMBER_ID")
        print("   - RECIPIENT_WAID")
        print("   - SPLITWISE_CONSUMER_KEY")
        print("   - SPLITWISE_CONSUMER_SECRET")
        print("   - SPLITWISE_API_KEY")
        print("   - SPLITWISE_GROUP_ID")
        print()
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"Error: Service account file not found at {service_account_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in service account file {service_account_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_heroku_auth.py <path_to_service_account.json>")
        print("Example: python setup_heroku_auth.py /path/to/your-service-account.json")
        sys.exit(1)
    
    service_account_path = sys.argv[1]
    setup_heroku_auth(service_account_path)