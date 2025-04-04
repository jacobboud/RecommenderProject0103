namespace RecommenderProject.Models
{
    public class RecommendationResponse
    {
        public List<long> Collaborative { get; set; }
        public List<long> Content { get; set; }
        public List<long> WideAndDeep { get; set; }
    }

}
