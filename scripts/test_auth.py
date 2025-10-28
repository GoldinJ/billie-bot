#!/usr/bin/env python3
"""
Test script to verify Google Cloud authentication is working correctly.
Run this locally and on Heroku to ensure your authentication setup is correct.
"""

import os
import json
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.google.google_utils import _get_credentials
from google.cloud import documentai

def test_authentication():
    """Test Google Cloud authentication."""
    print("Testing Google Cloud Authentication...")
    print("=" * 50)
    
    # Test credential loading
    credentials = _get_credentials()
    
    if credentials:
        print("✓ Credentials loaded successfully from GOOGLE_SERVICE_ACCOUNT_JSON")
        print(f"  Project ID: {credentials.project_id}")
        print(f"  Service Account Email: {credentials.service_account_email}")
    else:
        print("→ Using default credentials (GOOGLE_APPLICATION_CREDENTIALS)")
        
        # Check if GOOGLE_APPLICATION_CREDENTIALS is set
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if creds_path:
            print(f"  Credentials file: {creds_path}")
            if os.path.exists(creds_path):
                print("  ✓ Credentials file exists")
                try:
                    with open(creds_path, 'r') as f:
                        creds_data = json.load(f)
                    print(f"  Project ID: {creds_data.get('project_id', 'Not found')}")
                    print(f"  Service Account Email: {creds_data.get('client_email', 'Not found')}")
                except Exception as e:
                    print(f"  ✗ Error reading credentials file: {e}")
            else:
                print("  ✗ Credentials file does not exist")
        else:
            print("  ✗ GOOGLE_APPLICATION_CREDENTIALS not set")
    
    # Test client creation
    try:
        from google.api_core.client_options import ClientOptions
        
        project_id = os.getenv('GOOGLE_PROJECT_ID')
        location = os.getenv('GOOGLE_PROCESSOR_REGION', 'us')
        
        if not project_id:
            print("\n✗ GOOGLE_PROJECT_ID environment variable not set")
            return False
            
        print("\nTesting Document AI client creation...")
        print(f"  Project ID: {project_id}")
        print(f"  Location: {location}")
        
        client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        
        if credentials:
            client = documentai.DocumentProcessorServiceClient(
                client_options=client_options, 
                credentials=credentials
            )
        else:
            client = documentai.DocumentProcessorServiceClient(client_options=client_options)
        
        print("✓ Document AI client created successfully")
        
        # Test listing processors (if permissions allow)
        try:
            parent = f"projects/{project_id}/locations/{location}"
            response = client.list_processors(parent=parent)
            processors = list(response)
            print("✓ Successfully connected to Document AI API")
            print(f"  Found {len(processors)} processors")
            
            processor_id = os.getenv('GOOGLE_PROCESSOR_ID')
            if processor_id:
                processor_found = any(proc.name.endswith(processor_id) for proc in processors)
                if processor_found:
                    print(f"✓ Configured processor ID {processor_id} found")
                else:
                    print(f"⚠ Configured processor ID {processor_id} not found in list")
            else:
                print("⚠ GOOGLE_PROCESSOR_ID not configured")
                
        except Exception as e:
            print(f"⚠ Could not list processors (may be a permission issue): {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating Document AI client: {e}")
        return False

def check_environment_variables():
    """Check if all required environment variables are set."""
    print("\nChecking Environment Variables...")
    print("=" * 50)
    
    required_vars = [
        'GOOGLE_PROJECT_ID',
        'GOOGLE_PROCESSOR_REGION',
        'GOOGLE_PROCESSOR_ID',
        'META_API_VERSION',
        'META_VERIFICATION_TOKEN',
        'ACCESS_TOKEN',
        'PHONE_NUMBER_ID',
        'RECIPIENT_WAID',
        'SPLITWISE_CONSUMER_KEY',
        'SPLITWISE_CONSUMER_SECRET',
        'SPLITWISE_API_KEY',
        'SPLITWISE_GROUP_ID'
    ]
    
    optional_vars = [
        'GOOGLE_APPLICATION_CREDENTIALS',
        'GOOGLE_SERVICE_ACCOUNT_JSON',
        'GOOGLE_PROCESSOR_VERSION_ID',
        'MEDIA_DIR',
        'LOGGING_CONFIG',
        'PYTHONPATH',
        'META_APP_SECRET',
        'META_APP_ID'
    ]
    
    missing_required = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'TOKEN' in var or 'KEY' in var or 'SECRET' in var:
                display_value = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: Not set")
            missing_required.append(var)
    
    print("\nOptional variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            if var == 'GOOGLE_SERVICE_ACCOUNT_JSON':
                print(f"✓ {var}: Set (length: {len(value)} chars)")
            else:
                print(f"✓ {var}: {value}")
        else:
            print(f"→ {var}: Not set")
    
    if missing_required:
        print(f"\n⚠ Missing required environment variables: {', '.join(missing_required)}")
        return False
    else:
        print("\n✓ All required environment variables are set")
        return True

if __name__ == "__main__":
    print("Billie Bot - Authentication Test")
    print("=" * 50)
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✓ Loaded .env file")
    except ImportError:
        print("→ python-dotenv not available, using system environment")
    except Exception as e:
        print(f"→ Could not load .env file: {e}")
    
    env_ok = check_environment_variables()
    auth_ok = test_authentication()
    
    print("\n" + "=" * 50)
    if env_ok and auth_ok:
        print("✓ All tests passed! Your bot should work correctly.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please check the configuration above.")
        sys.exit(1)