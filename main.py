import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Create a directory to save media if it doesn't exist
MEDIA_DIR = "media"
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# Your Twilio Account SID and Auth Token from the .env file
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# NOTE: The Twilio helper library automatically uses these environment variables
# if they are set, so we don't need to explicitly pass them to the client.

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """
    This function handles all incoming messages from Twilio.
    It checks for incoming media and downloads it.
    """
    # Create a Twilio MessagingResponse object to build the reply
    resp = MessagingResponse()
    
    # Get the number of media items in the incoming message
    num_media = int(request.values.get("NumMedia", 0))

    if num_media > 0:
        # Loop through all media items in the message
        for i in range(num_media):
            # Twilio provides the media URL and content type in the request form data
            media_url = request.values.get(f"MediaUrl{i}")
            content_type = request.values.get(f"MediaContentType{i}")
            
            # Use requests to download the media file
            try:
                response = requests.get(media_url, auth=(ACCOUNT_SID, AUTH_TOKEN))
                
                # Check for successful download
                if response.status_code == 200:
                    # Determine the file extension based on content type
                    # A simple mapping for common image types
                    ext = ".jpg"
                    if content_type == "image/png":
                        ext = ".png"
                    elif content_type == "image/jpeg":
                        ext = ".jpeg"
                    
                    # Create a unique filename for the downloaded image
                    # We can use the MessageSid and MediaSid from the request for a robust name
                    message_sid = request.values.get("MessageSid")
                    media_sid = request.values.get(f"MediaSid{i}")
                    filename = f"{message_sid}_{media_sid}{ext}"
                    filepath = os.path.join(MEDIA_DIR, filename)

                    # Save the image to the media directory
                    with open(filepath, "wb") as f:
                        f.write(response.content)

                    print(f"Downloaded image: {filepath}")
                    resp.message("Thanks for sending the receipt! I have successfully downloaded it.")
                else:
                    resp.message(f"Oops! I couldn't download the image. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading image: {e}")
                resp.message("There was an error trying to download the image. Please try again.")

    else:
        # If the message has no media, send a prompt to the user
        resp.message("I can only process images. Please send a picture of your receipt.")

    # Return the TwiML response to Twilio
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
