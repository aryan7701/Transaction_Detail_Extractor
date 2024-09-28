# import streamlit as st
# import pytesseract
# import cv2
# import numpy as np
# import re
# from PIL import Image
# import json

# # Setup for Tesseract OCR
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Function to preprocess the image
# def preprocess_image(image):
#     open_cv_image = np.array(image)
#     gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
#     _, threshold_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#     return threshold_img

# # Function to extract all text from the image
# def extract_text_from_image(image):
#     text = pytesseract.image_to_string(image)
#     return text

# # Function to parse amount and replace % with ₹ if found
# # def process_amount(extracted_text):
# #     lines = extracted_text.split("\n")
# #     for line in lines:
# #         if "%" in line:
# #             amount_line = line.split()
# #             for word in amount_line:
# #                 if "%" in word:
# #                     amount = word.replace("%", "₹")
# #                     return amount
# #     return "Not found"

# # def process_amount(extracted_text):
# #     # Use regular expression to find the amount format
# #     match = re.search(r'₹\s?(\d+(?:\.\d{1,2})?)', extracted_text)
# #     if match:
# #         return match.group(0)  # Return the found amount
# #     else:
# #         # Check for the amount in a different format (if necessary)
# #         match = re.search(r'(\d+(?:\.\d{1,2})?)', extracted_text)
# #         if match:
# #             return "₹" + match.group(0)  # Prepend ₹ to the found amount
# #     return "Not found"

# # Function to parse amount from extracted text
# def process_amount(extracted_text):
#     # Look for the amount format, allowing for optional currency symbols and proper formatting
#     match = re.search(r'₹?\s*(\d{1,3}(?:\.\d{1,2})?)', extracted_text)
#     if match:
#         return "₹" + match.group(1)  # Prepend ₹ to the found amount
#     return "Not found"



# # Function to extract date and time based on known merchant formats
# def extract_date_time(extracted_text, merchant):
#     if merchant == "PhonePe":
#         match = re.search(r'(\d{1,2}:\d{2}\s?(AM|PM|am|pm) on \d{1,2}\s\w+\s\d{4})', extracted_text)
#     elif merchant == "Paytm":
#         match = re.search(r'(\d{1,2}:\d{2}\s?(AM|PM|am|pm),\s\d{1,2}\s\w+\s\d{4})', extracted_text)
#     elif merchant == "Google Pay":
#         match = re.search(r'(\d{1,2}\s\w+\s\d{4},\s\d{1,2}:\d{2}\s?(AM|PM|am|pm))', extracted_text)
#     else:
#         match = None
    
#     if match:
#         return match.group(0)
#     else:
#         return "Not found"

# # Function to search for specific transaction details from extracted text
# def parse_transaction_details(extracted_text):
#     transaction_details = {}

#     # Detect merchant by looking for specific keywords
#     if "Google" in extracted_text or "GPay" in extracted_text:
#         transaction_details["Merchant"] = "Google Pay"
#     elif "Paytm" in extracted_text:
#         transaction_details["Merchant"] = "Paytm"
#     elif "PhonePe" in extracted_text:
#         transaction_details["Merchant"] = "PhonePe"
#     else:
#         transaction_details["Merchant"] = "Unknown"

#     # Search for UPI Transaction ID
#     upi_match = re.search(r'[A-Za-z0-9]{12,}', extracted_text)
#     if upi_match:
#         transaction_details["UPI Transaction ID"] = upi_match.group(0)
#     else:
#         transaction_details["UPI Transaction ID"] = "Not found"

#     # Search for the amount and replace % with ₹ if necessary
#     transaction_details["Amount"] = process_amount(extracted_text)

#     # Search for date and time based on merchant
#     transaction_details["Date and Time"] = extract_date_time(extracted_text, transaction_details["Merchant"])

#     # Search for transaction status
#     if any(status in extracted_text for status in ["Success", "Completed", "Successful"]):
#         transaction_details["Transaction Status"] = "Success"
#     elif "Failed" in extracted_text:
#         transaction_details["Transaction Status"] = "Failed"
#     elif "Pending" in extracted_text:
#         transaction_details["Transaction Status"] = "Pending"
#     else:
#         transaction_details["Transaction Status"] = "Not found"

#     return transaction_details

# # Streamlit app to upload and process image
# st.title("Transaction Details Extraction")

# uploaded_image = st.file_uploader("Upload Transaction Screenshot", type=["jpg", "jpeg", "png"])

# if uploaded_image:
#     # Preprocess the image and extract text
#     st.write("Preprocessing the image for better OCR results...")
#     image = Image.open(uploaded_image)
#     preprocessed_image = preprocess_image(image)
    
#     st.write("Extracting text from the image...")
#     extracted_text = extract_text_from_image(preprocessed_image)
    
#     # Parse transaction details without showing extracted data
#     transaction_details = parse_transaction_details(extracted_text)
    
#     st.write("Transaction Details Extracted:")
#     st.json(transaction_details)

#     # Button to download JSON
#     json_data = json.dumps(transaction_details, indent=4)
#     st.download_button(label="Download JSON", data=json_data, file_name="transaction_details.json", mime="application/json")

# import streamlit as st
# import pytesseract
# import cv2
# import numpy as np
# import re
# from PIL import Image
# import json

# # Setup for Tesseract OCR
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Function to preprocess the image
# def preprocess_image(image):
#     open_cv_image = np.array(image)
#     gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
#     _, threshold_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#     return threshold_img

# # Function to extract all text from the image
# def extract_text_from_image(image):
#     text = pytesseract.image_to_string(image)
#     return text

# # Function to parse amount and replace % with ₹ if found
# def process_amount(extracted_text):
#     # Search for amounts with percentage and replace with ₹
#     lines = extracted_text.split("\n")
#     for line in lines:
#         if "%" in line:
#             amount_line = line.split()
#             for word in amount_line:
#                 if "%" in word:
#                     amount = word.replace("%", "₹")
#                     return amount

#     # If no percentage found, search for amounts with ₹
#     match = re.search(r'₹\d+(?:\.\d{1,2})?', extracted_text)
#     if match:
#         return match.group(0)  # Return the found amount

#     return "Not found"  # If no amount is found

# # Function to extract date and time based on known merchant formats
# def extract_date_time(extracted_text, merchant):
#     if merchant == "PhonePe":
#         match = re.search(r'(\d{1,2}:\d{2}\s?(AM|PM|am|pm) on \d{1,2}\s\w+\s\d{4})', extracted_text)
#     elif merchant == "Paytm":
#         match = re.search(r'(\d{1,2}:\d{2}\s?(AM|PM|am|pm),\s\d{1,2}\s\w+\s\d{4})', extracted_text)
#     elif merchant == "Google Pay":
#         match = re.search(r'(\d{1,2}\s\w+\s\d{4},\s\d{1,2}:\d{2}\s?(AM|PM|am|pm))', extracted_text)
#     else:
#         match = None
    
#     if match:
#         return match.group(0)
#     else:
#         return "Not found"

# # Function to search for specific transaction details from extracted text
# def parse_transaction_details(extracted_text):
#     transaction_details = {}

#     # Detect merchant by looking for specific keywords
#     if "Google" in extracted_text or "GPay" in extracted_text:
#         transaction_details["Merchant"] = "Google Pay"
#     elif "Paytm" in extracted_text:
#         transaction_details["Merchant"] = "Paytm"
#     elif "PhonePe" in extracted_text:
#         transaction_details["Merchant"] = "PhonePe"
#     else:
#         transaction_details["Merchant"] = "Unknown"

#     # Search for UPI Transaction ID
#     upi_match = re.search(r'[A-Za-z0-9]{12,}', extracted_text)
#     if upi_match:
#         transaction_details["UPI Transaction ID"] = upi_match.group(0)
#     else:
#         transaction_details["UPI Transaction ID"] = "Not found"

#     # Search for the amount and replace % with ₹ if necessary
#     transaction_details["Amount"] = process_amount(extracted_text)

#     # Search for date and time based on merchant
#     transaction_details["Date and Time"] = extract_date_time(extracted_text, transaction_details["Merchant"])

#     # Search for transaction status
#     if any(status in extracted_text for status in ["Success", "Completed", "Successful"]):
#         transaction_details["Transaction Status"] = "Success"
#     elif "Failed" in extracted_text:
#         transaction_details["Transaction Status"] = "Failed"
#     elif "Pending" in extracted_text:
#         transaction_details["Transaction Status"] = "Pending"
#     else:
#         transaction_details["Transaction Status"] = "Not found"

#     return transaction_details

# # Streamlit app to upload and process image
# st.title("Transaction Details Extraction")

# uploaded_image = st.file_uploader("Upload Transaction Screenshot", type=["jpg", "jpeg", "png"])

# if uploaded_image:
#     # Preprocess the image and extract text
#     st.write("Preprocessing the image for better OCR results...")
#     image = Image.open(uploaded_image)
#     preprocessed_image = preprocess_image(image)
    
#     st.write("Extracting text from the image...")
#     extracted_text = extract_text_from_image(preprocessed_image)
    
#     # Display raw extracted text
#     st.subheader("Raw Extracted Text")
#     st.text(extracted_text)

#     # Parse transaction details without showing extracted data
#     transaction_details = parse_transaction_details(extracted_text)
    
#     st.write("Transaction Details Extracted:")
#     st.json(transaction_details)

#     # Button to download JSON
#     json_data = json.dumps(transaction_details, indent=4)
#     st.download_button(label="Download JSON", data=json_data, file_name="transaction_details.json", mime="application/json")

import streamlit as st
import pytesseract
import cv2
import numpy as np
import re
from PIL import Image
import json

# Setup for Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to preprocess the image
def preprocess_image(image):
    open_cv_image = np.array(image)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    _, threshold_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return threshold_img

# Function to extract all text from the image
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to parse amount and replace % with ₹ if found
def process_amount(extracted_text):
    # Search for amounts with percentage and replace with ₹
    lines = extracted_text.split("\n")
    for line in lines:
        if "%" in line:
            amount_line = line.split()
            for word in amount_line:
                if "%" in word:
                    amount = word.replace("%", "₹")
                    return amount

    # If no percentage found, search for amounts with ₹
    match = re.search(r'₹\d+(?:\.\d{1,2})?', extracted_text)
    if match:
        return match.group(0)  # Return the found amount

    return "Not found"  # If no amount is found

# Function to extract date and time based on known merchant formats
def extract_date_time(extracted_text, merchant):
    if merchant == "PhonePe":
        match = re.search(r'(\d{1,2}:\d{2}\s?(AM|PM|am|pm) on \d{1,2}\s\w+\s\d{4})', extracted_text)
    elif merchant == "Paytm":
        match = re.search(r'(\d{1,2}:\d{2}\s?(AM|PM|am|pm),\s\d{1,2}\s\w+\s\d{4})', extracted_text)
    elif merchant == "Google Pay":
        match = re.search(r'(\d{1,2}\s\w+\s\d{4},\s\d{1,2}:\d{2}\s?(AM|PM|am|pm))', extracted_text)
    else:
        match = None
    
    if match:
        return match.group(0)
    else:
        return "Not found"

# Function to search for specific transaction details from extracted text
def parse_transaction_details(extracted_text):
    transaction_details = {}

    # Detect merchant by looking for specific keywords
    if "Google" in extracted_text or "GPay" in extracted_text:
        transaction_details["Merchant"] = "Google Pay"
    elif "Paytm" in extracted_text:
        transaction_details["Merchant"] = "Paytm"
    elif "PhonePe" in extracted_text:
        transaction_details["Merchant"] = "PhonePe"
    else:
        transaction_details["Merchant"] = "Unknown"

    # Search for UPI Transaction ID
    upi_match = re.search(r'[A-Za-z0-9]{12,}', extracted_text)
    if upi_match:
        transaction_details["UPI Transaction ID"] = upi_match.group(0)
    else:
        transaction_details["UPI Transaction ID"] = "Not found"

    # Search for the amount and replace % with ₹ if necessary
    transaction_details["Amount"] = process_amount(extracted_text)

    # Search for date and time based on merchant
    transaction_details["Date and Time"] = extract_date_time(extracted_text, transaction_details["Merchant"])

    # Search for transaction status
    if any(status in extracted_text for status in ["Success", "Completed", "Successful"]):
        transaction_details["Transaction Status"] = "Success"
    elif "Failed" in extracted_text:
        transaction_details["Transaction Status"] = "Failed"
    elif "Pending" in extracted_text:
        transaction_details["Transaction Status"] = "Pending"
    else:
        transaction_details["Transaction Status"] = "Not found"

    return transaction_details

# Streamlit app to upload and process image
st.title("Transaction Details Extraction")

uploaded_image = st.file_uploader("Upload Transaction Screenshot", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # Preprocess the image and extract text
    st.write("Preprocessing the image for better OCR results...")
    image = Image.open(uploaded_image)
    preprocessed_image = preprocess_image(image)
    
    st.write("Extracting text from the image...")
    extracted_text = extract_text_from_image(preprocessed_image)
    
    # Display raw extracted text
    st.subheader("Raw Extracted Text")
    st.text(extracted_text)

    # Parse transaction details without showing extracted data
    transaction_details = parse_transaction_details(extracted_text)
    
    # Include raw extracted text in transaction details
    transaction_details["Raw Extracted Text"] = extracted_text
    
    st.write("Transaction Details Extracted:")
    st.json(transaction_details)

    # Button to download JSON including raw text
    json_data = json.dumps(transaction_details, indent=4)
    st.download_button(label="Download JSON", data=json_data, file_name="transaction_details.json", mime="application/json")
