import 'source_config.dart';

/// User preference model
class UserPreference {
  final String chatId;
  final String product;
  final String targetCity;
  final int minPrice;
  final int maxPrice;
  final List<String> negativeKeywords;
  final SourceConfig facebook;
  final SourceConfig mercadoLivre;
  final SourceConfig olx;

  UserPreference({
    required this.chatId,
    required this.product,
    required this.targetCity,
    this.minPrice = 0,
    this.maxPrice = 999999,
    this.negativeKeywords = const [],
    SourceConfig? facebook,
    SourceConfig? mercadoLivre,
    SourceConfig? olx,
  })  : facebook = facebook ?? SourceConfig(active: false, url: ''),
        mercadoLivre = mercadoLivre ?? SourceConfig(active: false, url: ''),
        olx = olx ?? SourceConfig(active: false, url: '');

  factory UserPreference.fromJson(Map<String, dynamic> json) {
    final sources = json['fontes'] ?? {};

    return UserPreference(
      chatId: json['chat_id']?.toString() ?? '',
      product: json['produto'] ?? '',
      targetCity: json['cidade_alvo'] ?? '',
      minPrice: json['preco_min'] ?? 0,
      maxPrice: json['preco_max'] ?? 999999,
      negativeKeywords: List<String>.from(json['palavras_negativas'] ?? []),
      facebook: sources['facebook'] != null ? SourceConfig.fromJson(sources['facebook']) : null,
      mercadoLivre: sources['mercadolivre'] != null ? SourceConfig.fromJson(sources['mercadolivre']) : null,
      olx: sources['olx'] != null ? SourceConfig.fromJson(sources['olx']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'chat_id': chatId,
      'produto': product,
      'cidade_alvo': targetCity,
      'preco_min': minPrice,
      'preco_max': maxPrice,
      'palavras_negativas': negativeKeywords,
      'facebook_ativo': facebook.active,
      'facebook_url': facebook.url,
      'mercadolivre_ativo': mercadoLivre.active,
      'mercadolivre_url': mercadoLivre.url,
      'olx_ativo': olx.active,
      'olx_url': olx.url,
    };
  }

  UserPreference copyWith({
    String? chatId,
    String? product,
    String? targetCity,
    int? minPrice,
    int? maxPrice,
    List<String>? negativeKeywords,
    SourceConfig? facebook,
    SourceConfig? mercadoLivre,
    SourceConfig? olx,
  }) {
    return UserPreference(
      chatId: chatId ?? this.chatId,
      product: product ?? this.product,
      targetCity: targetCity ?? this.targetCity,
      minPrice: minPrice ?? this.minPrice,
      maxPrice: maxPrice ?? this.maxPrice,
      negativeKeywords: negativeKeywords ?? this.negativeKeywords,
      facebook: facebook ?? this.facebook,
      mercadoLivre: mercadoLivre ?? this.mercadoLivre,
      olx: olx ?? this.olx,
    );
  }
}
