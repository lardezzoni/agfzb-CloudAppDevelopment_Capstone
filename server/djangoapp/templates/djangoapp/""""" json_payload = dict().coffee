                """""  json_payload = dict()
                      json_payload["id"] = 999
                      json_payload["name"]= "Berk"
                      json_payload["dealership"] = dealer_id
                      json_payload["review"] = "default"
                      json_payload["purchase"] = True
                      json_payload["purchase_date"]="00/00/0000"
                      json_payload["car_make"]="Audi"
                      json_payload["car_model"]="A10"
                      json_payload["car_year"]="2000"
                      review = {             
                            "id": 998,
                            "name": "Default, came from website url",
                            "dealership": dealer_id,
                            "review": "review",
                            "purchase": "true",
                            "purchase_date" : "07/11/2020",
                            "car_make": "Audi",
                            "car_model": "A7",
                            "car_year": 2010
                        }
                      jsonreview = json.dumps(review)
                      response = post_request(url, jsonreview)
                      print(response)
                      return HttpResponse(response)"""""