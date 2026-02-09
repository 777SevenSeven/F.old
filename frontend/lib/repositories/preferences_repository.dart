import '../models/user_preference.dart';
import '../services/api_service.dart';

/// Repository layer for user preference operations.
class PreferencesRepository {
  PreferencesRepository(this._apiService);

  final ApiService _apiService;

  Future<List<UserPreference>> fetchPreferences() {
    return _apiService.getPreferences();
  }

  Future<UserPreference> createPreference(UserPreference preference) {
    return _apiService.createPreference(preference);
  }

  Future<UserPreference> updatePreference(int index, UserPreference preference) {
    return _apiService.updatePreference(index, preference);
  }

  Future<void> deletePreference(int index) {
    return _apiService.deletePreference(index);
  }
}
