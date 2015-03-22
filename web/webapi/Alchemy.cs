using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace webapi
{
    public class Alchemy
    {
        const string ImageKeywordsEndpoint = "http://access.alchemyapi.com/calls/image/ImageGetRankedImageKeywords";

        void main()
        {
            
        }
    }
}

// http://access.alchemyapi.com/calls/image/ImageGetRankedImageKeywords?apikey=1d20978a11f5a83679f65178b09538cbeee0dc99&url=https%3A%2F%2Fbikeraxx.blob.core.windows.net%2Fimages%2FG0010568.JPG&imagePostMode=not-raw&outputMode=json&forceShowAll=1
// http://access.alchemyapi.com/calls/image/ImageGetRankedImageKeywords?apikey=1d20978a11f5a83679f65178b09538cbeee0dc99&url=https%3A%2F%2Fbikeraxx.blob.core.windows.net%2Fimages%2FG0010568.JPG&outputMode=json&forceShowAll=1