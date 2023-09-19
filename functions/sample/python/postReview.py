from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
import requests
import sys

def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:


        authenticator = IAMAuthenticator('tSdkTinqoWWwBoyDMYVhRQFfwykt0vsrsYe-WIuaZbDr')
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url('https://c36af5af-8fb7-43d5-8c43-4da3026125d8-bluemix.cloudantnosqldb.appdomain.cloud')
        review_doc = Document(
             _id= "6ce15a14a432c1d6b1e6ad0a5b324508",
             _rev= "1-6d3a916e140863cdb147048888d26051",
             id= 88,
             name= "Berkly Shepley",
             dealership= 15,
             review= "Total grid-enabled service-desk",
             purchase= "true",
             purchase_date = "07/11/2020",
             car_make= "Audi",
             car_model= "A6",
             car_year= 2010)

        response = service.post_document(db='reviews', document=review_doc).get_result()

    except ApiException as ae:
      if ae.code == 412:
        print(f'Cannot create "{example_db_name}" database, ' +
              'it already exists.')

    return {
        "status":200,
        "body": "post completed",
        "content_type":'application/json',
    };