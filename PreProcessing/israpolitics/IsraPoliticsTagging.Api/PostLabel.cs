using Azure;
using Azure.Data.Tables;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;
using System.Net;

namespace IsraPoliticsTagging.Api;

public class PostLabel(ILoggerFactory loggerFactory)
{
    private readonly ILogger _logger = loggerFactory.CreateLogger<PostLabel>();

    [Function("PostLabel")]
    public async Task<HttpResponseData> Run(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)]
        HttpRequestData req)
    {
        _logger.LogInformation("Processing a request to post a label.");

        var response = req.CreateResponse();
        response.Headers.Add("Access-Control-Allow-Origin", "*");

        DataForTagging? data = await req.ReadFromJsonAsync<DataForTagging>();
        if (data is null)
        {
            _logger.LogInformation("Invalid request body.");
            response.StatusCode = HttpStatusCode.BadRequest;
            return response;
        }

        TableClient tableClient = new("UseDevelopmentStorage=true", "DataForTagging");
        await tableClient.UpdateEntityAsync(data, ETag.All, TableUpdateMode.Replace);

        _logger.LogInformation("Item updated. RowId: {RowId}", data.RowId);
        response.StatusCode = HttpStatusCode.OK;
        return response;
    }
}