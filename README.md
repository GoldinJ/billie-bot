# Billie Bot 🤖

A WhatsApp-integrated invoice processing bot that automatically extracts data from invoice images/documents and creates shared expenses in Splitwise.

## Overview

Billie Bot is a Flask-based webhook service that processes invoices sent via WhatsApp. It uses Google Cloud Document AI to extract structured data from invoice images or PDFs, classifies the invoice type, and automatically creates shared expenses in Splitwise for household or group expense management.

## Features

- **WhatsApp Integration**: Receive invoice images/documents directly through WhatsApp
- **Intelligent Invoice Processing**: Uses Google Cloud Document AI for accurate text extraction
- **Invoice Classification**: Automatically categorizes invoices (Water, Electricity, Gas, Internet, Property Tax)
- **Splitwise Integration**: Creates shared expenses automatically with proper categorization
- **Receipt Management**: Stores and attaches original receipts to Splitwise expenses
- **Real-time Processing**: Provides immediate feedback through WhatsApp messages
- **Comprehensive Logging**: Detailed logging for monitoring and debugging

## Architecture

```
WhatsApp → Meta Webhook → Billie Bot → Google Document AI → Splitwise
                ↓
           Media Storage (Local)
```

### Core Components

- **Flask Webhook**: Handles WhatsApp webhook requests and responses
- **Invoice Processor**: Extracts and processes invoice data using Google Cloud Document AI
- **Invoice Classifier**: Categorizes invoices based on content analysis
- **Splitwise Service**: Creates and manages shared expenses
- **Media Handler**: Downloads and stores invoice images/documents

## Supported Invoice Types

| Type | Category ID | Supported Languages |
|------|-------------|-------------------|
| Water & Sewage | 7 | Hebrew (מים, ביוב) |
| Electricity | 5 | Hebrew (חברת החשמל, חשמל) |
| Gas | 6 | Hebrew (גז, הספקת גז) |
| Internet | 8 | Hebrew (אינטרנט, TV) |
| Property Tax | 45 | Hebrew (ארנונה) |

## Prerequisites

- Python 3.13+
- Google Cloud Project with Document AI API enabled
- WhatsApp Business API access
- Splitwise account and API credentials
- ngrok (for local development)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GoldinJ/billie-bot.git
   cd billie-bot
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```env
   # Meta/WhatsApp Configuration
   META_API_VERSION=v21.0
   META_VERIFICATION_TOKEN=your_verification_token
   ACCESS_TOKEN=your_whatsapp_access_token
   PHONE_NUMBER_ID=your_phone_number_id
   RECIPIENT_WAID=recipient_whatsapp_id
   
   # Google Cloud Configuration
   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
   PROJECT_ID=your_gcp_project_id
   LOCATION=us
   PROCESSOR_ID=your_document_ai_processor_id
   
   # Splitwise Configuration
   SPLITWISE_CONSUMER_KEY=your_splitwise_consumer_key
   SPLITWISE_CONSUMER_SECRET=your_splitwise_consumer_secret
   SPLITWISE_API_KEY=your_splitwise_api_key
   SPLITWISE_GROUP_ID=your_default_group_id
   
   # Application Configuration
   MEDIA_DIR=./media
   ```

4. **Set up Google Cloud credentials**:
   - Create a service account in your Google Cloud Project
   - Enable the Document AI API
   - Download the service account JSON key
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable

5. **Configure WhatsApp Webhook**:
   - Set up a WhatsApp Business account
   - Configure webhook URL to point to your application endpoint
   - Use ngrok for local development: `ngrok http 5000`

## Usage

### Running the Application

1. **Start the Flask application**:
   ```bash
   python app.py
   ```

2. **For development with ngrok**:
   ```bash
   # In a separate terminal
   ngrok http 5000 --domain your-ngrok-domain.ngrok-free.app
   ```

3. **Send an invoice via WhatsApp**:
   - Send an image or PDF of an invoice to your configured WhatsApp number
   - The bot will process the invoice and create a Splitwise expense
   - You'll receive a confirmation message with expense details

### Example Workflow

1. User sends an electricity bill image via WhatsApp
2. Bot downloads and processes the image using Google Document AI
3. Invoice data is extracted and classified as "Electricity"
4. A new expense is created in Splitwise with:
   - Proper category (Electricity - Category ID: 5)
   - Extracted cost amount
   - Auto-generated description (e.g., "Electricity - 12/2025")
   - Original receipt attached
   - Split equally among group members
5. User receives confirmation message with expense details

## API Endpoints

- `GET /whatsapp` - Webhook verification endpoint
- `POST /whatsapp` - Main webhook handler for incoming messages

## Testing

Run the test suite:
```bash
pytest tests/
```

Test coverage includes:
- Invoice classification logic
- Document processing functionality
- Splitwise integration
- Utility functions

## Project Structure

```
billie-bot/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration management
│   ├── routes.py                # Webhook endpoints
│   ├── security.py              # Message verification
│   ├── utils.py                 # WhatsApp utilities
│   └── services/
│       ├── invoice_processor/
│       │   ├── __init__.py      # Invoice types enum
│       │   ├── classifier.py    # Invoice classification
│       │   ├── invoice.py       # Invoice data model
│       │   └── processor.py     # Main processing logic
│       ├── splitwise/
│       │   └── spitwise_utils.py # Splitwise integration
│       └── google/
│           └── google_utils.py   # Google Document AI
├── tests/                       # Test suite
├── conf/                        # Configuration files
├── logs/                        # Application logs
├── media/                       # Stored invoice files
├── app.py                       # Application entry point
├── pyproject.toml              # Project dependencies
└── README.md                   # This file
```

## Configuration

### Google Cloud Document AI Setup

1. Create a Document AI processor in the Google Cloud Console
2. Choose the "Form Parser" processor type for best results with invoices
3. Note the Processor ID for your environment configuration

### Splitwise Setup

1. Create a Splitwise account and group for shared expenses
2. Generate API credentials from the Splitwise developer portal
3. Note your group ID from the Splitwise URL

### WhatsApp Business API Setup

1. Set up a Meta developer account
2. Create a WhatsApp Business app
3. Configure webhook endpoints and verification tokens
4. Obtain necessary API tokens and phone number ID

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

1. **Invoice not recognized**: Ensure the invoice contains Hebrew text matching the classification keywords
2. **Google Document AI errors**: Verify service account credentials and API quotas
3. **Splitwise creation fails**: Check API credentials and group permissions
4. **WhatsApp webhook not responding**: Verify ngrok tunnel and webhook URL configuration

### Logging

Check the application logs in `logs/app.log` for detailed error information and processing status.

## Acknowledgments

- Google Cloud Document AI for intelligent document processing
- Splitwise for expense management API
- Meta WhatsApp Business API for messaging integration