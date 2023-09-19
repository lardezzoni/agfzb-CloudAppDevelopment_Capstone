/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: "tSdkTinqoWWwBoyDMYVhRQFfwykt0vsrsYe-WIuaZbDr" })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl("https://c36af5af-8fb7-43d5-8c43-4da3026125d8-bluemix.cloudantnosqldb.appdomain.cloud");
      try {
        let dbList = await cloudant.postAllDocs({ db: "dealerships", includeDocs: true, limit: 10 })    ;
        return {
                statusCode: 200,
                headers: { 'Content-Type': 'application/json' },
                body: dbList.result
         };
      } catch (error) {
          return { error: error.description };
      }
}