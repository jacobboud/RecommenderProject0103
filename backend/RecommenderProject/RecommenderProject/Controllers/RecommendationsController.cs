using Microsoft.AspNetCore.Mvc;
using RecommenderProject.Models;
using System.Diagnostics;

namespace RecommenderProject.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class RecommendationsController : ControllerBase
    {
        [HttpPost]
        public IActionResult GetRecommendations([FromBody] RecommendationRequest request)
        {
            var id = request.Id;
            var type = request.Type.ToLower();

            var collaborativeRecs = new List<long>();
            var contentRecs = new List<long>();

            // --- COLLABORATIVE ---
            string collaborativeScript = type switch
            {
                "item" => "PythonModels/get_collaborative_recs.py",
                "user" => "PythonModels/get_collaborative_recs_user.py",
                _ => null
            };

            if (collaborativeScript != null)
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"{collaborativeScript} {id} 5",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using (var process = Process.Start(psi))
                using (var reader = process.StandardOutput)
                {
                    string? line;
                    while ((line = reader.ReadLine()) != null)
                    {
                        if (long.TryParse(line, out long recId))
                        {
                            collaborativeRecs.Add(recId);
                        }
                    }

                    process.WaitForExit();
                }
            }

            // --- CONTENT-BASED (now supports both item and user) ---
            if (type == "item" || type == "user")
            {
                var psiContent = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"PythonModels/get_content_recs.py {id} 5 {type}", // type = "item" or "user"
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using (var process = Process.Start(psiContent))
                using (var reader = process.StandardOutput)
                {
                    string? line;
                    while ((line = reader.ReadLine()) != null)
                    {
                        if (long.TryParse(line, out long recId))
                        {
                            contentRecs.Add(recId);
                        }
                    }

                    process.WaitForExit();
                }
            }

            // --- FINAL RESPONSE ---
            var result = new RecommendationResponse
            {
                Collaborative = collaborativeRecs,
                Content = contentRecs,
                WideAndDeep = new List<long>() // Placeholder for Azure ML recs
            };

            return Ok(result);
        }
    }
}
