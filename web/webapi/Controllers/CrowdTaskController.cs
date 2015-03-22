using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;

namespace webapi.Controllers
{
    public class CrowdflowerTask {
        public string signal;
        public string payload;
        public string signature;
    }

    public class CrowdTaskController : ApiController
    {
        // POST: api/CrowdTask
        public HttpResponseMessage Post(string id, [FromBody] CrowdflowerTask task)
        {
            //NOTE: id is ignored.
            return new HttpResponseMessage(HttpStatusCode.OK);
        }
    }
}
