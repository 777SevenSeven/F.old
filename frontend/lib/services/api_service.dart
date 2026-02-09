import 'dart:convert';

import 'package:dio/dio.dart';

import '../config/api_config.dart';
import '../models/user_preference.dart';
import '../models/search_item.dart';

/// API Service for GarimpoBot
class ApiService {
  ApiService({Dio? dio})
      : _dio = dio ??
            Dio(
              BaseOptions(
                baseUrl: ApiConfig.baseUrl,
                connectTimeout: ApiConfig.timeout,
                sendTimeout: ApiConfig.timeout,
                receiveTimeout: ApiConfig.timeout,
                contentType: Headers.jsonContentType,
              ),
            );

  final Dio _dio;

  /// Check API health
  Future<Map<String, dynamic>> checkHealth() async {
    try {
      final response = await _dio.get(ApiConfig.health);

      if (response.statusCode == 200) {
        return _asMap(response.data);
      } else {
        throw Exception('Health check failed: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to check health: $e');
    }
  }

  /// Get all preferences
  Future<List<UserPreference>> getPreferences() async {
    try {
      final response = await _dio.get(
        ApiConfig.preferences,
        options: Options(headers: {'Content-Type': Headers.jsonContentType}),
      );

      if (response.statusCode == 200) {
        final data = _asMap(response.data);
        if (data['success'] == true) {
          final List<dynamic> prefsJson = data['data'];
          return prefsJson.map((json) => UserPreference.fromJson(json)).toList();
        } else {
          throw Exception(data['error'] ?? 'Unknown error');
        }
      } else {
        throw Exception('Failed to load preferences: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to get preferences: $e');
    }
  }

  /// Create a new preference
  Future<UserPreference> createPreference(UserPreference preference) async {
    try {
      final response = await _dio.post(
        ApiConfig.preferences,
        data: preference.toJson(),
        options: Options(headers: {'Content-Type': Headers.jsonContentType}),
      );

      if (response.statusCode == 201) {
        final data = _asMap(response.data);
        if (data['success'] == true) {
          return UserPreference.fromJson(data['data']);
        } else {
          throw Exception(data['error'] ?? 'Unknown error');
        }
      } else {
        final errorData = _asMap(response.data);
        throw Exception(errorData['error'] ?? 'Failed to create preference');
      }
    } catch (e) {
      throw Exception('Failed to create preference: $e');
    }
  }

  /// Update an existing preference
  Future<UserPreference> updatePreference(int index, UserPreference preference) async {
    try {
      final response = await _dio.put(
        '${ApiConfig.preferences}/$index',
        data: preference.toJson(),
        options: Options(headers: {'Content-Type': Headers.jsonContentType}),
      );

      if (response.statusCode == 200) {
        final data = _asMap(response.data);
        if (data['success'] == true) {
          return UserPreference.fromJson(data['data']);
        } else {
          throw Exception(data['error'] ?? 'Unknown error');
        }
      } else {
        final errorData = _asMap(response.data);
        throw Exception(errorData['error'] ?? 'Failed to update preference');
      }
    } catch (e) {
      throw Exception('Failed to update preference: $e');
    }
  }

  /// Delete a preference
  Future<void> deletePreference(int index) async {
    try {
      final response = await _dio.delete(
        '${ApiConfig.preferences}/$index',
      );

      if (response.statusCode == 200) {
        final data = _asMap(response.data);
        if (data['success'] != true) {
          throw Exception(data['error'] ?? 'Unknown error');
        }
      } else {
        final errorData = _asMap(response.data);
        throw Exception(errorData['error'] ?? 'Failed to delete preference');
      }
    } catch (e) {
      throw Exception('Failed to delete preference: $e');
    }
  }

  /// Search items based on preference
  Future<List<SearchItem>> searchItems(int preferenceIndex) async {
    try {
      final response = await _dio.post(
        ApiConfig.search,
        data: {'preference_index': preferenceIndex},
        options: Options(headers: {'Content-Type': Headers.jsonContentType}),
      );

      if (response.statusCode == 200) {
        final data = _asMap(response.data);
        if (data['success'] == true) {
          final List<dynamic> itemsJson = data['data']['items'];
          return itemsJson.map((json) => SearchItem.fromJson(json)).toList();
        } else {
          throw Exception(data['error'] ?? 'Unknown error');
        }
      } else {
        final errorData = _asMap(response.data);
        throw Exception(errorData['error'] ?? 'Failed to search items');
      }
    } catch (e) {
      throw Exception('Failed to search items: $e');
    }
  }

  /// Analyze product with AI
  Future<String> analyzeProduct(String product, double price) async {
    try {
      final response = await _dio.post(
        ApiConfig.aiAnalyze,
        data: {
          'produto': product,
          'preco': price,
        },
      );

      if (response.statusCode == 200) {
        final data = _asMap(response.data);
        if (data['success'] == true) {
          return data['data']['analysis'];
        } else {
          throw Exception(data['error'] ?? 'Unknown error');
        }
      } else {
        final errorData = _asMap(response.data);
        throw Exception(errorData['error'] ?? 'Failed to analyze product');
      }
    } catch (e) {
      throw Exception('Failed to analyze product: $e');
    }
  }

  /// Get AI search suggestions
  Future<String> getSuggestedSearchUrls(String product, String city) async {
    try {
      final response = await _dio.post(
        ApiConfig.aiSuggestSearch,
        data: {
          'produto': product,
          'cidade': city,
        },
      );

      if (response.statusCode == 200) {
        final data = _asMap(response.data);
        if (data['success'] == true) {
          return data['data']['suggestions'];
        } else {
          throw Exception(data['error'] ?? 'Unknown error');
        }
      } else {
        final errorData = _asMap(response.data);
        throw Exception(errorData['error'] ?? 'Failed to get suggestions');
      }
    } catch (e) {
      throw Exception('Failed to get suggestions: $e');
    }
  }

  Map<String, dynamic> _asMap(dynamic data) {
    if (data is Map<String, dynamic>) {
      return data;
    }
    if (data is String && data.isNotEmpty) {
      final decoded = json.decode(data);
      if (decoded is Map<String, dynamic>) {
        return decoded;
      }
    }
    throw Exception('Invalid response format');
  }
}
