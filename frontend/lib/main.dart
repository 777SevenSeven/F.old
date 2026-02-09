import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/inject.dart';
import 'core/theme/app_theme.dart';
import 'screens/home_screen/home_screen.dart';
import 'repositories/preferences_repository.dart';
import 'repositories/search_repository.dart';
import 'providers/preferences_provider.dart';
import 'providers/search_provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await setupInjection();

  runApp(
    MultiProvider(
      providers: [
        Provider<PreferencesRepository>.value(
          value: inject<PreferencesRepository>(),
        ),
        Provider<SearchRepository>.value(
          value: inject<SearchRepository>(),
        ),
        ChangeNotifierProvider<PreferencesProvider>(
          create: (_) => PreferencesProvider(
            repository: inject<PreferencesRepository>(),
          ),
        ),
        ChangeNotifierProvider<SearchProvider>(
          create: (_) => SearchProvider(
            repository: inject<SearchRepository>(),
          ),
        ),
      ],
      child: const GarimpoBotApp(),
    ),
  );
}

class GarimpoBotApp extends StatelessWidget {
  const GarimpoBotApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'F.OLD - Intelligence Engine',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      home: const HomeScreen(),
    );
  }
}
