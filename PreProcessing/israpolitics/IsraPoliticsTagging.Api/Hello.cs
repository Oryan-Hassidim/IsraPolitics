using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;
using System.Net;

namespace IsraPoliticsTagging.Api
{
    public class Hello(ILogger<Hello> logger)
    {
        private readonly ILogger<Hello> _logger = logger;

        [Function("Hello")]
        public async Task<HttpResponseData> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post")]
            HttpRequestData req)
        {
            _logger.LogInformation("C# HTTP trigger function processed a request.");
            var response = req.CreateResponse(HttpStatusCode.OK);
            string? name = req.Query["name"] ?? await req.ReadAsStringAsync();
            if (!string.IsNullOrEmpty(name))
                await response.WriteAsJsonAsync($"Hello, {name}");
            else
                await response.WriteAsJsonAsync("Hello");
            return response;
        }
    }
}
