using System.Net;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;

namespace IsraPoliticsTagging.Api;

public class GetUnlabeledItem(ILoggerFactory loggerFactory)
{
    private readonly ILogger _logger = loggerFactory.CreateLogger<GetUnlabeledItem>();

    [Function("GetUnlabeledItem")]
    public async Task<HttpResponseData> Run(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = null)]
        HttpRequestData req,
        [TableInput("DataForTagging", "DataForTagging",
                    Take = 1,
                    Filter = "Labeled eq false",
                    Connection = "AzureWebJobsStorage")]
        IEnumerable<DataForTagging> items
        )
    {
        _logger.LogInformation("Processing a request to get an unlabeled item.");

        var response = req.CreateResponse();
        response.Headers.Add("Access-Control-Allow-Origin", "*");


        var firstUnlabeledItem = items.FirstOrDefault();
        if (firstUnlabeledItem is null)
        {
            _logger.LogInformation("Unlabeled item didn't found.");
            response.StatusCode = HttpStatusCode.NoContent;
            return response;
        }
        response.StatusCode = HttpStatusCode.OK;
        await response.WriteAsJsonAsync(firstUnlabeledItem);
        _logger.LogInformation("Unlabeled item found. RowId: {RowId}", firstUnlabeledItem.RowId);
        return response;
    }
}