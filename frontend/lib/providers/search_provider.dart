import 'package:flutter/foundation.dart';
import '../models/search_item.dart';
import '../repositories/search_repository.dart';

/// Provider for managing search results
class SearchProvider with ChangeNotifier {
  final SearchRepository _repository;

  List<SearchItem> _items = [];
  bool _isSearching = false;
  String? _error;

  SearchProvider({required SearchRepository repository}) : _repository = repository;

  List<SearchItem> get items => _items;
  bool get isSearching => _isSearching;
  String? get error => _error;

  /// Search for items based on preference index
  Future<void> search(int preferenceIndex) async {
    _isSearching = true;
    _error = null;
    notifyListeners();

    try {
      _items = await _repository.searchItems(preferenceIndex);
      _error = null;
    } catch (e) {
      _error = e.toString();
      _items = [];
    } finally {
      _isSearching = false;
      notifyListeners();
    }
  }

  /// Clear search results
  void clearResults() {
    _items = [];
    _error = null;
    notifyListeners();
  }

  /// Clear error message
  void clearError() {
    _error = null;
    notifyListeners();
  }
}
