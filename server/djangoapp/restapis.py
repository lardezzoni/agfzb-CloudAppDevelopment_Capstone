import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', "tSdkTinqoWWwBoyDMYVhRQFfwykt0vsrsYe-WIuaZbDr"))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload):
    print("POST from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, data=json_payload, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', "tSdkTinqoWWwBoyDMYVhRQFfwykt0vsrsYe-WIuaZbDr"))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = {"sucess": "sucess"}
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["rows"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review["doc"]
            try:
                sentiment_analyzed = analyze_review_sentiments(review_doc["review"])

                
            
            # Create a CarDealer object with values in `doc` object
                review_obj = DealerReview(id=review_doc["id"], name=review_doc["name"], review=review_doc["review"],
                                   purchase=review_doc["purchase"], purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                   car_model=review_doc["car_model"],
                                   car_year=review_doc["car_year"], sentiment=sentiment_analyzed, dealership=review_doc["dealership"])
            except:
                return "Dealer don't exist"

            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):

   
        url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/a9270a83-5bb9-41eb-969c-587796bf847d/v1/analyze?version=2019-07-12"
        args = { "text": dealerreview, 
                "features": {
                    
                        "sentiment": True,
                        
                        
                    },
                "language": "en",
                "keywords": {
                    "sentiment": True,
                    "limit": 2
                },
                "return_analyzed_text":True,
                }
        try:
             response = requests.post(url, params=args, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', "rzj9c47bmhO-AdSVpZVvulPGNkqgGQJ0liY92Bsc0S0r"))
        except:
            print("error getting AI")
        data = response.json()
        #res_params = dict()
       # res_params["text"] = data["text"]
       # res_params["version"] = data["version"]
       # res_params["features"] = data["features"]
       # res_params["return_analyzed_text"] = data["return_analyzed_text"]
        finalresponse = data["sentiment"]["document"]["label"]
        return finalresponse

...


