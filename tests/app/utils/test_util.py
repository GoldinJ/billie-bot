from app.utils import (get_body,
                       get_media_id,
                       get_media_url,
                       get_message_status,
                       get_message_body,
                       get_message_type,
                       get_sender)

service_sent = {
    "object": "whatsapp_business_account",
    "entry": [
    {
        "id": "820441783887297",
        "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551441452",
              "phone_number_id": "810246222167565"
            },
            "statuses": [
              {
                "id": "wamid.HBgMOTcyNTQ2NDIyMjQxFQIAERgSQzA4NkMyQzgzQTMyQ0UyQkQ3AA==",
                "status": "sent",
                "timestamp": "1757949796",
                "recipient_id": "972546422241",
                "conversation": {
                  "id": "3883a3db141761abb56fc559df8c970a",
                  "expiration_timestamp": "1757949796",
                  "origin": {
                    "type": "service"
                  }
                },
                "pricing": {
                  "billable": False,
                  "pricing_model": "PMP",
                  "category": "service",
                  "type": "free_customer_service"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}

service_delivered = {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "820441783887297",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551441452",
              "phone_number_id": "810246222167565"
            },
            "statuses": [
              {
                "id": "wamid.HBgMOTcyNTQ2NDIyMjQxFQIAERgSQzA4NkMyQzgzQTMyQ0UyQkQ3AA==",
                "status": "delivered",
                "timestamp": "1757949796",
                "recipient_id": "972546422241",
                "conversation": {
                  "id": "3883a3db141761abb56fc559df8c970a",
                  "origin": {
                    "type": "service"
                  }
                },
                "pricing": {
                  "billable": False,
                  "pricing_model": "PMP",
                  "category": "service",
                  "type": "free_customer_service"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}

message_text = {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "820441783887297",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551441452",
              "phone_number_id": "810246222167565"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Jenia Goldin"
                },
                "wa_id": "972546422241"
              }
            ],
            "messages": [
              {
                "from": "972546422241",
                "id": "wamid.HBgMOTcyNTQ2NDIyMjQxFQIAEhggQUM1NDJEOEI0Qzg4NUMwRTZDRkZBQjNCMEY5MjBEOUEA",
                "timestamp": "1758129513",
                "text": {
                  "body": "Body"
                },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}

message_document = {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "820441783887297",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551441452",
              "phone_number_id": "810246222167565"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Jenia Goldin"
                },
                "wa_id": "972546422241"
              }
            ],
            "messages": [
              {
                "from": "972546422241",
                "id": "wamid.HBgMOTcyNTQ2NDIyMjQxFQIAEhggQUM5REYyNEI4RjkyRDg5QzE3OTI2NEJGMzgxNkY5MUEA",
                "timestamp": "1757949776",
                "type": "document",
                "document": {
                  "filename": "Invoice_21039073.pdf",
                  "mime_type": "application/pdf",
                  "sha256": "tCpvAY7e5gUC4SV7a/+KqnftZmSQOtiFXZdGm3S18Kc=",
                  "id": "651779301301439"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}

message_image = {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "820441783887297",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551441452",
              "phone_number_id": "810246222167565"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Jenia Goldin"
                },
                "wa_id": "972546422241"
              }
            ],
            "messages": [
              {
                "from": "972546422241",
                "id": "wamid.HBgMOTcyNTQ2NDIyMjQxFQIAEhggQUMyMUJERkVCMjg3QUJFNDgxNTEwRDY0MjdEMDBCNUMA",
                "timestamp": "1758129563",
                "type": "image",
                "image": {
                  "mime_type": "image/jpeg",
                  "sha256": "gXdLgj9gmSm9dkIW1XMJ/Q6Ymp2/ZT/9jreJEjfzmbI=",
                  "id": "766623462830009"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}

def test_get_body():
    assert get_body(message_text) == 'Body'
    
def test_get_body_document():
  assert get_body(message_document) is None
  
def test_get_body_empty():
  assert get_body({}) is None
  
def test_get_body_service_sent():
  assert get_body(service_sent) is None
  
def test_get_body_service_delivered():
  assert get_body(service_delivered) is None
  
  
def test_get_messege_status():
  assert get_message_status(service_sent) == 'sent'
  assert get_message_status(service_delivered) == 'delivered'
  assert get_message_status(message_document) is None
  assert get_message_status(message_image) is None
  assert get_message_status(message_text) is None
  assert get_message_status({}) is None
  
def test_get_media_id():
  assert get_media_id(message_image) == "766623462830009"
  assert get_media_id(message_document) == "651779301301439"
  assert get_media_id(message_text) is None
  assert get_media_id(service_delivered) is None
  assert get_media_id(service_sent) is None
  assert get_media_id({}) is None
  
def test_get_media_type():
  assert get_message_type(message_text) == "text"
  assert get_message_type(message_image) == "image"
  assert get_message_type(message_document) == "document"
  assert get_message_type(service_delivered) is None
  assert get_message_type(service_sent) is None
  

  
  
  


