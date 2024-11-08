import requests
from dotenv import load_dotenv
import os
import time
import xml.etree.ElementTree as ET

# Load environment variables for the eBay API access token
load_dotenv()
access_token = os.getenv('access_token')


# Define the XML request for GetFeedback
def create_get_feedback_xml(user_id, item_id):
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <GetFeedbackRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <RequesterCredentials>
            <eBayAuthToken>{access_token}</eBayAuthToken>
        </RequesterCredentials>
        <UserID>{user_id}</UserID>
        <ItemID>{item_id}</ItemID>
        <FeedbackType>FeedbackReceivedAsSeller</FeedbackType>
        <DetailLevel>ReturnAll</DetailLevel>
        <Pagination>
            <EntriesPerPage>25</EntriesPerPage>
            <PageNumber>1</PageNumber>
        </Pagination>
    </GetFeedbackRequest>"""
    return xml


def get_feedback(user_id, item_id):
    url = "https://api.ebay.com/ws/api.dll"
    headers = {
        "Content-Type": "text/xml",
        "X-EBAY-API-CALL-NAME": "GetFeedback",
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967"
    }

    xml_body = create_get_feedback_xml(user_id, item_id)
    response = requests.post(url, headers=headers, data=xml_body)

    if response.status_code == 200:
        # print("Response received successfully \n\n")
        return response.text
    else:
        print("Request failed:", response.status_code, response.text)
        return None


def parse_feedback_response(xml_data):
    root = ET.fromstring(xml_data)
    namespace = "{urn:ebay:apis:eBLBaseComponents}"
    
    # Feedback Details
    feedback_details = []
    for feedback in root.findall(f'.//{namespace}FeedbackDetail'):
        feedback_info = {
            'ItemID': feedback.find(f'{namespace}ItemID').text,
            'CommentingUser': feedback.find(f'{namespace}CommentingUser').text,
            'CommentingUserScore': feedback.find(f'{namespace}CommentingUserScore').text,
            'CommentText': feedback.find(f'{namespace}CommentText').text,
            'CommentTime': feedback.find(f'{namespace}CommentTime').text,
            'CommentType': feedback.find(f'{namespace}CommentType').text
        }
        feedback_details.append(feedback_info)    
    
    
    # Print Feedback Details
    print("\nFeedback Details:")
    for feedback in feedback_details:
        print(f"User: {feedback['CommentingUser']} | Score: {feedback['CommentingUserScore']} | Star: {feedback['FeedbackRatingStar']}")
        print(f"Comment: {feedback['CommentText']}")
        print(f"Date: {feedback['CommentTime']} | Type: {feedback['CommentType']}")
        print(f"Item ID: {feedback['ItemID']} | Title: {feedback['ItemTitle']}")
        print("-" * 40)
    

# Example usage with the XML response data
# user_id = "t1gear"
# item_id = "115655996499"
user_id = "mr_dyson_sales"
item_id = "115322469956"

feedback_xml = get_feedback(user_id, item_id)
parse_feedback_response(feedback_xml)


