import requests
from dotenv import load_dotenv
import os

load_dotenv()
access_token = os.getenv('access_token')

# Replace these with your actual eBay API credentials

item_ids = ['v1|405306690432|0']
# v1|126199144924|427211371126
# v1|276596530300|2560025902430
# v1|126199144924|427211371126
# v1|186736780109|0
# v1|235795846248|0
# '315911089455'
# '315908636487'
# '167046923605'
# Define the endpoint for the getItem call
# url = f'https://api.ebay.com/buy/browse/v1/item/v1|{item_id}|0'

# Headers, including the authorization token
headers = {
    'Authorization': f'Bearer {access_token}',
    'X-EBAY-C-ENDUSERCTX': 'contextualLocation=country=IE'  # Specify Ireland as the country
}

for item_id in item_ids:
    url = f'https://api.ebay.com/buy/browse/v1/item/{item_id}'
    response = requests.get(url, headers=headers) 

    if response.status_code == 200:
        item_details = response.json()

        shipped_to_ie = False

        if 'shipToLocations' in item_details and 'regionIncluded' in item_details['shipToLocations']:
            for region in item_details['shipToLocations']['regionIncluded']:
                if region.get('regionName') in ('Ireland', 'Worldwide', 'Europe'):
                    shipped_to_ie = True
                    break
            for region in item_details['shipToLocations']['regionExcluded']:
                if region.get('regionName') == 'Ireland':
                    shipped_to_ie = False
                    break



        print(item_details)
        print('\n'*2)
        print(shipped_to_ie)

    else:
        print("Error:", response.status_code, response.text)
