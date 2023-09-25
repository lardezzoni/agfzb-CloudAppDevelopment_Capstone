from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from requests.auth import HTTPBasicAuth
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_request, get_reviews_from_cf, analyze_review_sentiments, post_request
from .models import CarDealer, DealerReview
from django.forms.models import model_to_dict
from django.template import RequestContext
import logging
import json
import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def IndexView(request):
    context={}
    return render(request,'djangoapp/index.html', context)

def AddReviewView(request):
    context={}

    return render(request,'djangoapp/add_review.html', context)

def DealerDetailsView(request):
    if request.method == "GET":
        dealer_id=15
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/f24bc0b4-325b-4601-a262-9b9454e6bfb0/dealership-package/get-review"
        url_dealers = "https://us-south.functions.appdomain.cloud/api/v1/web/f24bc0b4-325b-4601-a262-9b9454e6bfb0/dealership-package/get-dealerships"

        # Get dealers from the URL
        reviews= get_reviews_from_cf(url)
        dealerships_list = get_dealers_from_cf(url_dealers)
        # Concat all dealer's short name
        context = dict()  
        context['dealership_list']=dealerships_list
        context["reviews"]= reviews
        iterate_dict = dict()
        iterate_dict["reviews"] = []

        test = dict()
        try:
            for review in reviews:
                print(review)
                if dealer_id == review.dealership:
                    
                    print(type(review))
                    #model_to_dict(review)
                    
                    iterate_dict["reviews"].append(review)
                   


            for dealer in dealerships_list:

                if dealer_id == dealer.id:

                    iterate_dict["id"] = dealer
                    print(dealer.full_name)
            
            for iterate in iterate_dict["reviews"]:
                print(iterate)
            
            #return HttpResponse(iterate_dict["id"])
            return render(request, 'djangoapp/dealer_details.html', {'context':iterate_dict})



        except:
            if reviews == "Dealer don't exist":
                return HttpResponse("Dealer don't exist")
            else:
                return render(request, 'djangoapp/dealer_details.html', context)

def RegistrationView(request):
    context={}

    return render(request,'djangoapp/registration.html', context)

def AboutUsView(request):
    context={
    }
    return render(request,'djangoapp/about.html', context)

def ContactView(request):
    context={}
    return render(request,'djangoapp/contact.html', context)

def LoginView(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)

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
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/f24bc0b4-325b-4601-a262-9b9454e6bfb0/dealership-package/get-dealerships"
        # Get dealers from the URL
        dealerships_list = get_dealers_from_cf(url)
        context = dict()
        url_rev= "https://us-south.functions.appdomain.cloud/api/v1/web/f24bc0b4-325b-4601-a262-9b9454e6bfb0/dealership-package/get-review"
        context['dealership_list']=dealerships_list
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships_list])
        # Return a list of dealer short name
        return render(request,'djangoapp/index.html', context)
    
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/f24bc0b4-325b-4601-a262-9b9454e6bfb0/dealership-package/get-review"
        url_dealers = "https://us-south.functions.appdomain.cloud/api/v1/web/f24bc0b4-325b-4601-a262-9b9454e6bfb0/dealership-package/get-dealerships"

        # Get dealers from the URL
        reviews= get_reviews_from_cf(url)
        dealerships_list = get_dealers_from_cf(url_dealers)
        # Concat all dealer's short name
        context = dict()  
        context['dealership_list']=dealerships_list
        context["reviews"]= reviews
        iterate_dict = dict()
        iterate_dict["reviews"] = []

        test = dict()
        try:
            for review in reviews:
                print(review)
                if dealer_id == review.dealership:
                    
                    print(type(review))
                    #model_to_dict(review)
                    
                    iterate_dict["reviews"].append(review)
                   


            for dealer in dealerships_list:

                if dealer_id == dealer.id:

                    iterate_dict["id"] = dealer
                    print(dealer.full_name)
            
            for iterate in iterate_dict["reviews"]:
                print(iterate)
            
            #return HttpResponse(iterate_dict["id"])
            return render(request, 'djangoapp/dealer_details.html', {'context':iterate_dict})



        except:
            if reviews == "Dealer don't exist":
                return HttpResponse("Dealer don't exist")
            else:
                return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = dict()
    context["cars"] = []
    context["dealership_name"] = {}
    iterate_context = []
    if request.method == "GET":

        if request.user.is_authenticated:
            url="https://us-south.functions.appdomain.cloud/api/v1/web/f24bc0b4-325b-4601-a262-9b9454e6bfb0/dealership-package/post-review"
            url_dealer_exist ="https://us-south.functions.appdomain.cloud/api/v1/web/f24bc0b4-325b-4601-a262-9b9454e6bfb0/dealership-package/get-review"
            reviews = get_reviews_from_cf(url_dealer_exist)
            url_dealers = "https://us-south.functions.appdomain.cloud/api/v1/web/f24bc0b4-325b-4601-a262-9b9454e6bfb0/dealership-package/get-dealerships"


            dealerships_list = get_dealers_from_cf(url_dealers)
            print("FIRST")
            if reviews == "Dealer don't exist" or reviews==None:
                for dealer in dealerships_list:
                     context["cars"].append(dealer.id)
                
                print(context["cars"])
                print("HERE5")
                return render(request, 'djangoapp/add_review.html', context)
            else:
             for review in reviews:
                if review.dealership == dealer_id:
                    context["cars"].append(review)
            for dealer in dealerships_list:
                if dealer.id == dealer_id:
                    context["dealership_name"]=dealer.full_name
                    print("HERE 6666")
                    break
            print(context["dealership_name"])
            render(request, 'djangoapp/add_review.html', context)



            try:
                print(context["cars"])
                print("HERE5")
                return render(request, 'djangoapp/add_review.html', context)
            except:
                print("HERE2")
                return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        print("HERE")
        values = extract_payload(request)

        return HttpResponse(values)

def extract_payload(request):
   submitted_payload = []
   for key in request.POST:
           value = request.POST[key]
           submitted_payload.append(value)
   return submitted_payload       
 
def get_test(request, **kwargs):
    if request.method == "GET":
        url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/a9270a83-5bb9-41eb-969c-587796bf847d/v1/analyze?version=2019-07-12"
        args = { "text": "i love myself, this is great news, where I signup", 
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
        response = requests.post(url, params=args, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', "rzj9c47bmhO-AdSVpZVvulPGNkqgGQJ0liY92Bsc0S0r"))
        data = response.json()
        res_params = dict()
       # res_params["text_unit"] = data["text_unit"]
       # res_params["version"] = data["version"]
        #res_params["features"] = data["features"]
       # res_params["return_analyzed_text"] = data["return_analyzed_text"]
        finalresponse = data["sentiment"]["document"]["label"]
        return HttpResponse(finalresponse)