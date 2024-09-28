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

# Break text into structured list of lines
def structure_extracted_text(extracted_text):
    lines = extracted_text.split("\n")
    return [line.strip() for line in lines if line.strip()]  # Remove empty lines


# Google Pay specific logic
def gpay_logic(lines):
    transaction_details = {}
    transaction_details["Merchant"] = "Google Pay"

    # Extract amount (amount starts with '2', rest is the amount)
    for line in lines:
        if line.startswith('2'):
            transaction_details["Amount"] = f"₹{line[1:]}"
            break
    else:
        transaction_details["Amount"] = "Not found"

    # Extract date and time
    for line in lines:
        match = re.search(r'(\d{1,2}\s\w+\s\d{4},\s\d{1,2}:\d{2}\s?(AM|PM|am|pm))', line)
        if match:
            transaction_details["Date and Time"] = match.group(0)
            break
    else:
        transaction_details["Date and Time"] = "Not found"

    # Extract UPI transaction ID (look for "UPI transaction ID" and take the next line)
    transaction_details["UPI Transaction ID"] = "Not found"
    for i, line in enumerate(lines):
        if "UPI transaction ID" in line:
            # The UPI Transaction ID is on the next line
            if i + 1 < len(lines) and lines[i + 1].strip().isdigit():
                transaction_details["UPI Transaction ID"] = lines[i + 1].strip()
            break

    # Extract transaction status
    transaction_details["Transaction Status"] = "Not found"
    for line in lines:
        if "Completed" in line:
            transaction_details["Transaction Status"] = "Success"
            break
        elif "Failed" in line:
            transaction_details["Transaction Status"] = "Failed"
            break
        elif "Pending" in line:
            transaction_details["Transaction Status"] = "Pending"
            break

    return transaction_details


# Paytm specific logic
def paytm_logic(lines):
    transaction_details = {}
    transaction_details["Merchant"] = "Paytm"

    # Extract Amount (look for ' @')
    transaction_details["Amount"] = "Not found"
    for line in lines:
        if ' @' in line:
            # Split the line and get the first element before '@'
            amount_line = line.split()
            for word in amount_line:
                if '@' in word:
                    transaction_details["Amount"] = f"₹{amount_line[0]}"  # First element is the amount
                    break
            break

    # Extract Date and Time (look for "Paid at")
    transaction_details["Date and Time"] = "Not found"
    for line in lines:
        if "Paid at" in line:
            date_time = line.replace("Paid at", "").strip()
            transaction_details["Date and Time"] = date_time
            break

    # Extract UPI Transaction ID (look for "UPI Ref No:")
    transaction_details["UPI Transaction ID"] = "Not found"
    for line in lines:
        if "UPI Ref No:" in line:
            upi_id = line.split()
            for word in upi_id:
                if word.isdigit():
                    transaction_details["UPI Transaction ID"] = word
                    break
            break

    # Extract Transaction Status
    transaction_details["Transaction Status"] = "Not found"
    for line in lines:
        if "Successfully" in line:
            transaction_details["Transaction Status"] = "Success"
            break
        elif "Pending" in line:
            transaction_details["Transaction Status"] = "Pending"
            break
        elif "Failed" in line:
            transaction_details["Transaction Status"] = "Failed"
            break

    # Extract Merchant Name (look for "UPI ID:" and "@paytm")
    transaction_details["Merchant"] = "Not found"
    for line in lines:
        if "UPI ID:" in line and "@paytm" in line:
            transaction_details["Merchant"] = "Paytm"
            break

    return transaction_details


# PhonePe specific logic
def phonepe_logic(lines):
    transaction_details = {}
    transaction_details["Merchant"] = "PhonePe"

    # Extract amount (look for %)
    transaction_details["Amount"] = "Not found"
    for line in lines:
        if "%" in line:
            amount_line = line.split()
            for word in amount_line:
                if "%" in word:
                    transaction_details["Amount"] = word.replace("%", "₹")
                    break
            break

    # Extract date and time
    transaction_details["Date and Time"] = "Not found"
    for line in lines:
        match = re.search(r'(\d{1,2}:\d{2}\s?(AM|PM|am|pm) on \d{1,2}\s\w+\s\d{4})', line)
        if match:
            transaction_details["Date and Time"] = match.group(0)
            break

    # Extract UPI transaction ID
    transaction_details["UPI Transaction ID"] = "Not found"
    for line in lines:
        match = re.search(r'T[A-Za-z0-9]{12,}', line)
        if match:
            transaction_details["UPI Transaction ID"] = match.group(0)
            break

    # Extract transaction status
    transaction_details["Transaction Status"] = "Not found"
    for line in lines:
        if "Successful" in line:
            transaction_details["Transaction Status"] = "Success"
            break
        elif "Failed" in line:
            transaction_details["Transaction Status"] = "Failed"
            break
        elif "Pending" in line:
            transaction_details["Transaction Status"] = "Pending"
            break

    return transaction_details


# Function to detect merchant from structured lines
def detect_merchant(lines):
    for line in lines:
        # Check for Paytm by searching for '@paytm' in UPI ID
        if "@paytm" in line:
            return "Paytm"
        # Check for Google Pay keywords
        elif "Google" in line or "GPay" in line:
            return "Google Pay"
        # Check for PhonePe keywords
        elif "PhonePe" in line:
            return "PhonePe"
    return "Unknown"


# Main function to parse transaction details
def parse_transaction_details(lines):
    merchant = detect_merchant(lines)
    if merchant == "Google Pay":
        return gpay_logic(lines)
    elif merchant == "Paytm":
        return paytm_logic(lines)
    elif merchant == "PhonePe":
        return phonepe_logic(lines)
    else:
        return {
            "Merchant": "Unknown",
            "UPI Transaction ID": "Not found",
            "Amount": "Not found",
            "Date and Time": "Not found",
            "Transaction Status": "Not found"
        }

# Streamlit app
st.set_page_config(page_title="Smart UPI Transaction Extractor", layout="wide", page_icon="💳")

# Add a header with an icon
st.markdown("<h1 style='text-align: center; font-size: 3em; color: #4CAF50;'>Smart UPI Transaction Extractor 💳</h1>", unsafe_allow_html=True)

# Add a brief description
st.markdown("<p style='text-align: center; font-size: 1.5em;'>Upload your UPI transaction screenshot, and our smart system will extract and display key transaction details in no time!</p>", unsafe_allow_html=True)

# Use a full-width layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_image = st.file_uploader("Upload Transaction Screenshot", type=["jpg", "jpeg", "png"])

# If an image is uploaded, process it
if uploaded_image:
    st.markdown("<hr>", unsafe_allow_html=True)  # Add a stylish horizontal line
    st.markdown("<h3 style='text-align: center; font-size: 2em;'>Processing your Transaction... 📄</h3>", unsafe_allow_html=True)

    # Add a spinner while processing
    with st.spinner('Please wait... processing your transaction'):
        # Preprocess the image and extract text
        st.info("Preprocessing the image for better OCR results...")
        image = Image.open(uploaded_image)
        preprocessed_image = preprocess_image(image)
        
        st.info("Extracting text from the image...")
        extracted_text = extract_text_from_image(preprocessed_image)
        
        # Structure the extracted text into lines
        lines = structure_extracted_text(extracted_text)
        
        # Parse transaction details based on detected merchant
        transaction_details = parse_transaction_details(lines)

    st.markdown("<h3 style='text-align: center; font-size: 2em;'>Transaction Details Extracted</h3>", unsafe_allow_html=True)
    
    # Display transaction details in a stylish box
    st.json(transaction_details)
    
    st.markdown("<hr>", unsafe_allow_html=True)  # Add another horizontal line

    # Add a download button for the JSON file
    st.markdown("<h3 style='text-align: center; font-size: 1.8em;'>Download Your Data</h3>", unsafe_allow_html=True)
    json_data = json.dumps(transaction_details, indent=4)
    st.download_button(label="Download JSON", data=json_data, file_name="transaction_details.json", mime="application/json")

    # Add a success message
    st.success("Your transaction details have been successfully extracted and are ready for download! 🎉")
else:
    st.markdown("<p style='text-align: center; font-size: 1.5em; color: grey;'>Awaiting your transaction screenshot...</p>", unsafe_allow_html=True)

# Add a footer with a message
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<footer style='text-align: center; font-size: 1.2em;'>© 2024 Smart UPI Transaction Extractor</footer>", unsafe_allow_html=True)