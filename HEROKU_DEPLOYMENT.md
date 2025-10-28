# Heroku Deployment Guide for Billie Bot

This guide will help you deploy your Billie Bot to Heroku with proper Google Cloud authentication.

## Prerequisites

1. A Heroku account
2. Heroku CLI installed
3. Google Cloud service account JSON file
4. All your WhatsApp and Splitwise credentials

## Step-by-Step Deployment

### 1. Prepare Your Application

```bash
# Clone or navigate to your project
cd billie-bot

# Create a Heroku app
heroku create your-bot-name

# Add Python buildpack (if not automatically detected)
heroku buildpacks:set heroku/python
```

### 2. Set Up Google Cloud Authentication

```bash
# Use the setup script to get your service account JSON
python scripts/setup_heroku_auth.py path/to/your-service-account.json

# Copy the JSON output and set it as a config var
heroku config:set GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":"your-project",...}'
```

### 3. Configure All Environment Variables

```bash
# Google Cloud settings
heroku config:set PROJECT_ID=your_gcp_project_id
heroku config:set LOCATION=us
heroku config:set PROCESSOR_ID=your_document_ai_processor_id

# WhatsApp settings
heroku config:set META_API_VERSION=v21.0
heroku config:set META_VERIFICATION_TOKEN=your_verification_token
heroku config:set ACCESS_TOKEN=your_whatsapp_access_token
heroku config:set PHONE_NUMBER_ID=your_phone_number_id
heroku config:set RECIPIENT_WAID=recipient_whatsapp_id

# Splitwise settings
heroku config:set SPLITWISE_CONSUMER_KEY=your_splitwise_consumer_key
heroku config:set SPLITWISE_CONSUMER_SECRET=your_splitwise_consumer_secret
heroku config:set SPLITWISE_API_KEY=your_splitwise_api_key
heroku config:set SPLITWISE_GROUP_ID=your_default_group_id

# Application settings
heroku config:set MEDIA_DIR=./media
heroku config:set LOGGING_CONFIG=conf/logging.json
```

### 4. Deploy Your Application

```bash
# Add and commit your changes
git add .
git commit -m "Add Heroku authentication support"

# Deploy to Heroku
git push heroku main
```

### 5. Verify Your Deployment

```bash
# Check if your app is running
heroku ps

# View logs
heroku logs --tail

# Test authentication (optional)
heroku run python scripts/test_auth.py
```

### 6. Configure Your WhatsApp Webhook

Update your WhatsApp webhook URL to point to your Heroku app:
```
https://your-bot-name.herokuapp.com/whatsapp
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```bash
   # Check if your service account JSON is properly set
   heroku config:get GOOGLE_SERVICE_ACCOUNT_JSON
   
   # Run authentication test
   heroku run python scripts/test_auth.py
   ```

2. **Missing Environment Variables**
   ```bash
   # List all config vars
   heroku config
   
   # Check specific variable
   heroku config:get PROJECT_ID
   ```

3. **Application Won't Start**
   ```bash
   # Check logs
   heroku logs --tail
   
   # Check dyno status
   heroku ps
   
   # Restart app
   heroku restart
   ```

4. **Document AI Quota Issues**
   - Check your Google Cloud quotas
   - Ensure your service account has proper permissions
   - Verify the processor ID is correct

### Useful Commands

```bash
# View all environment variables
heroku config

# Open your app in browser
heroku open

# Run a one-off command
heroku run python -c "import os; print(os.getenv('PROJECT_ID'))"

# Scale dynos
heroku ps:scale web=1

# View app information
heroku info
```

## Security Notes

1. **Never commit sensitive data** to your Git repository
2. **Use Heroku config vars** for all sensitive information
3. **Regularly rotate your API keys** and service account credentials
4. **Monitor your Google Cloud quotas** and usage
5. **Set up proper IAM permissions** for your service account (minimum required permissions only)

## Maintenance

### Updating Your App

```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push heroku main
```

### Updating Environment Variables

```bash
# Update a single variable
heroku config:set PROJECT_ID=new_project_id

# Update multiple variables
heroku config:set VAR1=value1 VAR2=value2
```

### Monitoring

- Set up Heroku log drains if needed
- Monitor your Google Cloud usage and quotas
- Check Splitwise API rate limits
- Monitor WhatsApp webhook delivery

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Heroku logs: `heroku logs --tail`
3. Test authentication: `heroku run python scripts/test_auth.py`
4. Verify all config vars are set: `heroku config`