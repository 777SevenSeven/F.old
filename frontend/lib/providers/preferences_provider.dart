import 'package:flutter/foundation.dart';
import '../models/user_preference.dart';
import '../repositories/preferences_repository.dart';

/// Provider for managing user preferences
class PreferencesProvider with ChangeNotifier {
  final PreferencesRepository _repository;

  List<UserPreference> _preferences = [];
  bool _isLoading = false;
  String? _error;

  PreferencesProvider({required PreferencesRepository repository}) : _repository = repository;

  List<UserPreference> get preferences => _preferences;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Load all preferences from API
  Future<void> loadPreferences() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _preferences = await _repository.fetchPreferences();
      _error = null;
    } catch (e) {
      _error = e.toString();
      _preferences = [];
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Add a new preference
  Future<bool> addPreference(UserPreference preference) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final newPref = await _repository.createPreference(preference);
      _preferences.add(newPref);
      _error = null;
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Update an existing preference
  Future<bool> updatePreference(int index, UserPreference preference) async {
    if (index < 0 || index >= _preferences.length) {
      _error = 'Invalid index';
      notifyListeners();
      return false;
    }

    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final updated = await _repository.updatePreference(index, preference);
      _preferences[index] = updated;
      _error = null;
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Delete a preference
  Future<bool> deletePreference(int index) async {
    if (index < 0 || index >= _preferences.length) {
      _error = 'Invalid index';
      notifyListeners();
      return false;
    }

    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await _repository.deletePreference(index);
      _preferences.removeAt(index);
      _error = null;
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Clear error message
  void clearError() {
    _error = null;
    notifyListeners();
  }
}
