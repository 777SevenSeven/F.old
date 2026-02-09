import '../models/search_item.dart';
import '../services/api_service.dart';

/// Repository layer for search operations.
class SearchRepository {
  SearchRepository(this._apiService);

  final ApiService _apiService;

  Future<List<SearchItem>> searchItems(int preferenceIndex) {
    return _apiService.searchItems(preferenceIndex);
  }
}
