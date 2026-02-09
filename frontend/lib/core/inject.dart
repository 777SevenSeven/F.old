import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';

import '../config/api_config.dart';
import '../providers/preferences_provider.dart';
import '../providers/search_provider.dart';
import '../repositories/preferences_repository.dart';
import '../repositories/search_repository.dart';
import '../services/api_service.dart';

final GetIt inject = GetIt.instance;

Future<void> setupInjection() async {
  if (!inject.isRegistered<Dio>()) {
    inject.registerLazySingleton<Dio>(() {
      final options = BaseOptions(
        baseUrl: ApiConfig.baseUrl,
        connectTimeout: ApiConfig.timeout,
        sendTimeout: ApiConfig.timeout,
        receiveTimeout: ApiConfig.timeout,
        contentType: Headers.jsonContentType,
      );
      final dio = Dio(options);
      return dio;
    });
  }

  if (!inject.isRegistered<ApiService>()) {
    inject.registerLazySingleton<ApiService>(
      () => ApiService(dio: inject<Dio>()),
    );
  }

  if (!inject.isRegistered<PreferencesRepository>()) {
    inject.registerLazySingleton<PreferencesRepository>(
      () => PreferencesRepository(inject<ApiService>()),
    );
  }

  if (!inject.isRegistered<SearchRepository>()) {
    inject.registerLazySingleton<SearchRepository>(
      () => SearchRepository(inject<ApiService>()),
    );
  }

  if (!inject.isRegistered<PreferencesProvider>()) {
    inject.registerFactory<PreferencesProvider>(
      () => PreferencesProvider(repository: inject<PreferencesRepository>()),
    );
  }

  if (!inject.isRegistered<SearchProvider>()) {
    inject.registerFactory<SearchProvider>(
      () => SearchProvider(repository: inject<SearchRepository>()),
    );
  }
}
