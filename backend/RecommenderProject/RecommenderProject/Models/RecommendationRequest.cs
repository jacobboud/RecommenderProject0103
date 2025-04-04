namespace RecommenderProject.Models
{
    public class RecommendationRequest
    {
        public string Id { get; set; }
        public string Type { get; set; } // "user" or "item"
    }

}
