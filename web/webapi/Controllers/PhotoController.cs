using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Threading.Tasks;
using System.Web.Configuration;

namespace webapi.Controllers
{
    public class PhotoController : ApiController
    {
        // PUT: api/Photo/5
        public async Task Put(string id)
        {
            //TODO: do something

/*
 * Create a New Row
Creates a new Row in an existing Job. This is the request format and endpoint to use for unit-by-unit posting.
curl -d "unit[data][{column1}]={some_data_1}" -d "unit[data][{column2}]={some_data_2}" https://api.crowdflower.com/v1/jobs/{job_id}/units.json?key={api_key}
Responses: JSON object of the Row created, including its ID, data, and related Job ID. JSON application message indicating status of the operation (e.g., "Unit was successfully created")
 */

            var client = new HttpClient();
            var dict = new Dictionary<string, string>()  { { "unit[data][image]", id } };
            var content = new FormUrlEncodedContent(dict);
            var uri = new Uri(String.Format("https://api.crowdflower.com/v1/jobs/{0}/units.json?key={1}",  
                WebConfigurationManager.AppSettings["crowdflower.jobid"],
                WebConfigurationManager.AppSettings["crowdflower.apiKey"]));
            var response = await client.PostAsync(uri, content);
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.InternalServerError) { Content = response.Content });
        }
    }
}
