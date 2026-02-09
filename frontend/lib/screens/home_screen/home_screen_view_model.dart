import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

import '../../dtos/conversation_dto.dart';
import '../../dtos/product_dto.dart';
import '../../models/user_preference.dart';
import '../../models/search_item.dart';
import '../../repositories/preferences_repository.dart';
import '../../repositories/search_repository.dart';

enum HomeScreenStatus { idle, loading, content, error }

class HomeScreenViewModel extends ChangeNotifier {
  HomeScreenViewModel({
    required PreferencesRepository preferencesRepository,
    required SearchRepository searchRepository,
  })  : _preferencesRepository = preferencesRepository,
        _searchRepository = searchRepository;

  final PreferencesRepository _preferencesRepository;
  final SearchRepository _searchRepository;

  HomeScreenStatus preferencesStatus = HomeScreenStatus.idle;
  HomeScreenStatus offersStatus = HomeScreenStatus.idle;
  String? preferencesError;
  String? offersError;

  List<UserPreference> _preferences = [];
  List<SearchItem> _offers = [];
  List<ProductDto> _mockProducts = [];
  final Map<String, List<ProductDto>> _mockCatalogByKey = {};
  int _selectedPreferenceIndex = 0;
  String _currentSearchTerm = '';
  bool _mockCatalogLoaded = false;

  List<UserPreference> get preferences => _preferences;
  List<ConversationDto> get conversations => _preferences
      .map((pref) => ConversationDto(
            id: pref.chatId,
            title: pref.product.isNotEmpty ? pref.product : 'Preference ${pref.chatId}',
            icon: _iconForPreference(pref.product),
          ))
      .toList();

  List<ProductDto> get bestPriceProducts {
    if (_mockProducts.isNotEmpty) {
      return _mockProducts.take(8).toList();
    }
    return _offers.take(6).map(_mapItemToProduct).toList();
  }

  List<ProductDto> get recentProducts {
    if (_mockProducts.isNotEmpty) {
      return _mockProducts.skip(8).take(8).toList();
    }
    return _offers.skip(6).take(6).map(_mapItemToProduct).toList();
  }

  int get totalProducts => _mockProducts.isNotEmpty ? _mockProducts.length : _offers.length;
  bool get hasPreferences => _preferences.isNotEmpty;
  int get selectedPreferenceIndex => _selectedPreferenceIndex;

  Future<void> loadInitialData() async {
    await Future.wait([
      loadPreferences(),
      _loadMockCatalog(),
    ]);
  }

  Future<void> loadPreferences() async {
    preferencesStatus = HomeScreenStatus.loading;
    notifyListeners();
    try {
      _preferences = await _preferencesRepository.fetchPreferences();
      preferencesStatus = HomeScreenStatus.content;
      preferencesError = null;
    } catch (e) {
      preferencesStatus = HomeScreenStatus.error;
      preferencesError = e.toString();
    }
    notifyListeners();
  }

  Future<void> fetchOffersForPreference(int index) async {
    if (index < 0 || index >= _preferences.length) return;
    _selectedPreferenceIndex = index;
    offersStatus = HomeScreenStatus.loading;
    _mockProducts = [];
    notifyListeners();
    try {
      _offers = await _searchRepository.searchItems(index);
      if (_offers.isEmpty) {
        await _loadMockCatalog();
        _mockProducts = _generateMocksForTerm(_preferences[index].product);
      } else {
        _mockProducts = [];
      }
      offersStatus = HomeScreenStatus.content;
      offersError = null;
    } catch (e) {
      await _loadMockCatalog();
      _offers = [];
      _mockProducts = _generateMocksForTerm(_preferences[index].product);
      offersStatus = HomeScreenStatus.content;
      offersError = null;
    }
    notifyListeners();
  }

  Future<void> searchByTerm(String term) async {
    if (term.trim().isEmpty) return;
    _currentSearchTerm = term.trim();
    offersStatus = HomeScreenStatus.loading;
    _offers = [];
    _mockProducts = [];
    notifyListeners();

    await _loadMockCatalog();
    await Future.delayed(const Duration(seconds: 1));
    _mockProducts = _generateMocksForTerm(_currentSearchTerm);
    if (_mockProducts.isNotEmpty) {
      offersStatus = HomeScreenStatus.content;
      offersError = null;
    } else {
      offersStatus = HomeScreenStatus.error;
      offersError = 'No mock available for this term';
    }
    notifyListeners();
  }

  Future<void> fetchOffersByChatId(String chatId) async {
    final index = _preferences.indexWhere((pref) => pref.chatId == chatId);
    if (index != -1) {
      await fetchOffersForPreference(index);
    }
  }

  Future<void> _loadMockCatalog() async {
    if (_mockCatalogLoaded) return;
    try {
      final jsonString = await rootBundle.loadString('assets/mocks/products.json');
      final Map<String, dynamic> data = jsonDecode(jsonString) as Map<String, dynamic>;
      _populateMockCatalog(data);
      _mockCatalogLoaded = true;
    } catch (e) {
      debugPrint('Failed to load mock catalog: $e');
      _populateMockCatalog(_fallbackMockCatalog);
      _mockCatalogLoaded = true;
    }
  }

  void _populateMockCatalog(Map<String, dynamic> data) {
    data.forEach((key, value) {
      final items = (value as List).map<ProductDto>((entry) => ProductDto.fromJson(Map<String, dynamic>.from(entry as Map))).toList();
      _mockCatalogByKey[key.toLowerCase()] = items;
    });
  }

  List<ProductDto> _generateMocksForTerm(String term) {
    if (_mockCatalogByKey.isEmpty) return [];
    final key = _catalogKeyForTerm(term.toLowerCase());
    final defaultCatalog = _mockCatalogByKey['default'] ?? [];
    final catalog = _mockCatalogByKey[key] ?? defaultCatalog;
    return List<ProductDto>.from(catalog);
  }

  String _catalogKeyForTerm(String term) {
    if (term.contains('iphone') || term.contains('celular') || term.contains('smartphone')) {
      return 'iphone';
    }
    if (term.contains('macbook') || term.contains('notebook') || term.contains('laptop')) {
      return 'macbook';
    }
    if (term.contains('gameboy') || term.contains('nintendo')) {
      return 'gameboy';
    }
    return 'default';
  }

  ProductDto _mapItemToProduct(SearchItem item) {
    final statusTexts = ['just listed', 'new', 'recently posted'];
    final isStatusTitle = statusTexts.any(
      (s) => item.title.toLowerCase().contains(s),
    );

    final title = isStatusTitle
        ? item.priceText.isNotEmpty
            ? item.priceText
            : 'Untitled product'
        : item.title.isNotEmpty
            ? item.title
            : 'Untitled product';

    final displayTitle = title.length > 18 ? '${title.substring(0, 15)}...' : title;

    final badge = item.extraInfo.isNotEmpty && item.extraInfo.length <= 15 ? item.extraInfo : null;

    return ProductDto(
      title: displayTitle,
      price: item.priceText.isNotEmpty ? item.priceText : 'Price not provided',
      imageUrl: item.imageUrl,
      marketplace: item.origin.isNotEmpty ? item.origin : 'Desconhecido',
      badge: badge,
      link: item.link,
    );
  }

  IconData _iconForPreference(String product) {
    final normalized = product.toLowerCase();
    if (normalized.contains('notebook') || normalized.contains('laptop')) {
      return Icons.laptop;
    }
    if (normalized.contains('playstation') || normalized.contains('console')) {
      return Icons.videogame_asset;
    }
    if (normalized.contains('iphone') || normalized.contains('celular')) {
      return Icons.smartphone;
    }
    if (normalized.contains('tv')) {
      return Icons.tv;
    }
    return Icons.chat_bubble_outline;
  }
}

const Map<String, dynamic> _fallbackMockCatalog = {
  'iphone': [
    {
      'title': 'iPhone 12 64GB Preto',
      'price': 'R\$ 1.899',
      'marketplace': 'FACEBOOK',
      'badge': 'Low price',
      'imageUrl': 'https://images.unsplash.com/photo-1603899123140-b7b6be6c4585?w=600',
      'link': 'https://facebook.com/marketplace/iphone12-64gb-preto',
    },
    {
      'title': 'iPhone 12 128GB Verde',
      'price': 'R\$ 2.080',
      'marketplace': 'MERCADOLIVRE',
      'badge': 'new',
      'imageUrl': 'https://images.unsplash.com/photo-1606066906352-0282f9b56bce?w=600',
      'link': 'https://www.mercadolivre.com.br/iphone12-128gb-verde',
    },
    {
      'title': 'iPhone 12 Pro 128GB',
      'price': 'R\$ 2.899',
      'marketplace': 'FACEBOOK',
      'badge': 'Deal',
      'imageUrl': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600',
      'link': 'https://facebook.com/marketplace/iphone12-pro',
    },
    {
      'title': 'iPhone 12 256GB Branco',
      'price': 'R\$ 2.650',
      'marketplace': 'OLX',
      'badge': 'Seminew',
      'imageUrl': 'https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=600',
      'link': 'https://www.olx.com.br/iphone12-256',
    },
    {
      'title': 'iPhone 12 Mini 64GB',
      'price': 'R\$ 1.550',
      'marketplace': 'OLX',
      'badge': 'Low price',
      'imageUrl': 'https://images.unsplash.com/photo-1529612700005-e35377bf1415?w=600',
      'link': 'https://www.olx.com.br/iphone12-mini',
    },
    {
      'title': 'iPhone 12 128GB Roxo',
      'price': 'R\$ 2.200',
      'marketplace': 'FACEBOOK',
      'badge': 'Top deal',
      'imageUrl': 'https://images.unsplash.com/photo-1512499617640-c2f999098c01?w=600',
      'link': 'https://facebook.com/marketplace/iphone12-roxo',
    },
    {
      'title': 'iPhone 12 64GB Azul',
      'price': 'R\$ 1.750',
      'marketplace': 'MERCADOLIVRE',
      'badge': 'Low price',
      'imageUrl': 'https://images.unsplash.com/photo-1475180098004-ca77a66827be?w=600',
      'link': 'https://www.mercadolivre.com.br/iphone12-azul',
    },
    {
      'title': 'iPhone 12 128GB Branco',
      'price': 'R\$ 2.150',
      'marketplace': 'FACEBOOK',
      'badge': 'Lacrado',
      'imageUrl': 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=600',
      'link': 'https://facebook.com/marketplace/iphone12-branco',
    },
  ],
  'macbook': [
    {
      'title': 'MacBook Air M1 256GB',
      'price': 'R\$ 4.200',
      'marketplace': 'OLX',
      'badge': 'Seminew',
      'imageUrl': 'https://images.unsplash.com/photo-1503602642458-232111445657?w=600',
      'link': 'https://www.olx.com.br/macbook-air-m1',
    },
    {
      'title': 'MacBook Pro 14"',
      'price': 'R\$ 9.800',
      'marketplace': 'FACEBOOK',
      'badge': 'Lacrado',
      'imageUrl': 'https://images.unsplash.com/photo-1517331156700-3c241d2b4d83?w=600',
      'link': 'https://facebook.com/marketplace/macbook-pro-14',
    },
    {
      'title': 'MacBook Air M2 512GB',
      'price': 'R\$ 6.300',
      'marketplace': 'MERCADOLIVRE',
      'badge': 'Premium',
      'imageUrl': 'https://images.unsplash.com/photo-1517445312885-5bc20087f9e2?w=600',
      'link': 'https://www.mercadolivre.com.br/macbook-air-m2',
    },
    {
      'title': 'MacBook Pro 13" i5',
      'price': 'R\$ 3.900',
      'marketplace': 'OLX',
      'badge': 'Low price',
      'imageUrl': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600',
      'link': 'https://www.olx.com.br/macbook-pro-13',
    },
    {
      'title': 'MacBook Air 2019',
      'price': 'R\$ 3.100',
      'marketplace': 'FACEBOOK',
      'badge': 'Bom estado',
      'imageUrl': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600',
      'link': 'https://facebook.com/marketplace/macbook-air-2019',
    },
    {
      'title': 'MacBook Pro 16" i9',
      'price': 'R\$ 8.700',
      'marketplace': 'MERCADOLIVRE',
      'badge': 'Top deal',
      'imageUrl': 'https://images.unsplash.com/photo-1511385348-a52b4a160dc2?w=600',
      'link': 'https://www.mercadolivre.com.br/macbook-pro-16',
    },
    {
      'title': 'MacBook Air M2 8GB',
      'price': 'R\$ 5.800',
      'marketplace': 'FACEBOOK',
      'badge': 'new',
      'imageUrl': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600',
      'link': 'https://facebook.com/marketplace/macbook-air-m2',
    },
    {
      'title': 'MacBook Pro 15" Retina',
      'price': 'R\$ 4.500',
      'marketplace': 'OLX',
      'badge': 'Seminew',
      'imageUrl': 'https://images.unsplash.com/photo-1483058712412-4245e9b90334?w=600',
      'link': 'https://www.olx.com.br/macbook-pro-15',
    },
  ],
  'gameboy': [
    {
      'title': 'Game Boy Color Roxo',
      'price': 'R\$ 550',
      'marketplace': 'FACEBOOK',
      'badge': 'Retro',
      'imageUrl': 'https://images.unsplash.com/photo-1613940109083-6e139e12e7d8?w=600',
      'link': 'https://facebook.com/marketplace/gameboy-color',
    },
    {
      'title': 'Game Boy Advance SP',
      'price': 'R\$ 720',
      'marketplace': 'OLX',
      'badge': 'Completo',
      'imageUrl': 'https://images.unsplash.com/photo-1526045478516-99145907023c?w=600',
      'link': 'https://www.olx.com.br/gameboy-advance-sp',
    },
    {
      'title': 'Game Boy Pocket',
      'price': 'R\$ 480',
      'marketplace': 'MERCADOLIVRE',
      'badge': 'Colecionador',
      'imageUrl': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600',
      'link': 'https://www.mercadolivre.com.br/gameboy-pocket',
    },
    {
      'title': 'Game Boy Advance Azul',
      'price': 'R\$ 630',
      'marketplace': 'FACEBOOK',
      'badge': 'Raro',
      'imageUrl': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600',
      'link': 'https://facebook.com/marketplace/gameboy-advance',
    },
    {
      'title': 'Game Boy Classic',
      'price': 'R\$ 690',
      'marketplace': 'MERCADOLIVRE',
      'badge': 'Great condition',
      'imageUrl': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=600',
      'link': 'https://www.mercadolivre.com.br/gameboy-classic',
    },
    {
      'title': 'Game Boy Micro',
      'price': 'R\$ 780',
      'marketplace': 'OLX',
      'badge': 'Raro',
      'imageUrl': 'https://images.unsplash.com/photo-1523475472560-d2df97ec485c?w=600',
      'link': 'https://www.olx.com.br/gameboy-micro',
    },
    {
      'title': 'Game Boy Color Verde',
      'price': 'R\$ 520',
      'marketplace': 'FACEBOOK',
      'badge': 'Retro',
      'imageUrl': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600',
      'link': 'https://facebook.com/marketplace/gameboy-color-verde',
    },
    {
      'title': 'Game Boy Advance Rosa',
      'price': 'R\$ 610',
      'marketplace': 'MERCADOLIVRE',
      'badge': 'Colecionador',
      'imageUrl': 'https://images.unsplash.com/photo-1526045612212-70caf35c14df?w=600',
      'link': 'https://www.mercadolivre.com.br/gameboy-advance-rosa',
    },
  ],
  'default': [
    {
      'title': 'Great used item',
      'price': 'R\$ 299',
      'marketplace': 'FACEBOOK',
      'badge': 'Low price',
      'imageUrl': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=600',
      'link': 'https://facebook.com/marketplace/used-product',
    },
    {
      'title': 'Featured deal',
      'price': 'R\$ 450',
      'marketplace': 'OLX',
      'badge': 'Deal',
      'imageUrl': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600',
      'link': 'https://www.olx.com.br/featured-deal',
    },
    {
      'title': 'Collectible item',
      'price': 'R\$ 199',
      'marketplace': 'MERCADOLIVRE',
      'badge': 'Colecionador',
      'imageUrl': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=600',
      'link': 'https://www.mercadolivre.com.br/item-colecionavel',
    },
    {
      'title': 'Featured product',
      'price': 'R\$ 550',
      'marketplace': 'FACEBOOK',
      'badge': 'Top deal',
      'imageUrl': 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=600',
      'link': 'https://facebook.com/marketplace/featured-product',
    },
    {
      'title': 'Achado especial',
      'price': 'R\$ 380',
      'marketplace': 'OLX',
      'badge': 'new',
      'imageUrl': 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600',
      'link': 'https://www.olx.com.br/achado-especial',
    },
    {
      'title': 'Flash deal',
      'price': 'R\$ 620',
      'marketplace': 'MERCADOLIVRE',
      'badge': 'Deal',
      'imageUrl': 'https://images.unsplash.com/photo-1481349518771-20055b2a7b24?w=600',
      'link': 'https://www.mercadolivre.com.br/flash-deal',
    },
    {
      'title': 'Verified product',
      'price': 'R\$ 150',
      'marketplace': 'FACEBOOK',
      'badge': 'Garantido',
      'imageUrl': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600',
      'link': 'https://facebook.com/marketplace/verified-product',
    },
    {
      'title': 'Confirmed deal',
      'price': 'R\$ 490',
      'marketplace': 'OLX',
      'badge': 'Seminew',
      'imageUrl': 'https://images.unsplash.com/photo-1504593811423-6dd665756598?w=600',
      'link': 'https://www.olx.com.br/confirmed-deal',
    },
  ],
};




