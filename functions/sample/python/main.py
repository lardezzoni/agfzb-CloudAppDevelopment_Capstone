#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

from ibmcloudant.cloudant_v1 import CloudantV1
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
        response = service.post_all_docs(
            db='reviews',
            include_docs=True,
            limit=10
        ).get_result()

        print(response)

    except ApiException as ae:
      if ae.code == 412:
        print(f'Cannot create "{example_db_name}" database, ' +
              'it already exists.')

    return {
        "status":200,
        "body":response,
        "content_type":'application/json',
    };
