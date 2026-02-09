/// API Configuration
class ApiConfig {
  //static const String baseUrl = 'https://garimpobot.onrender.com';
  static const String baseUrl = 'http://localhost:8000/';

  
  // Endpoints
  static const String health = '/health';
  static const String preferences = '/api/preferences';
  static const String search = '/api/search';
  static const String aiAnalyze = '/api/ai/analyze';
  static const String aiSuggestSearch = '/api/ai/suggest-search';
  
  // Timeout
  static const Duration timeout = Duration(seconds: 30);
}
