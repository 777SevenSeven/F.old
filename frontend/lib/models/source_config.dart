/// Model for search source configuration
class SourceConfig {
  final bool active;
  final String url;

  SourceConfig({
    required this.active,
    required this.url,
  });

  factory SourceConfig.fromJson(Map<String, dynamic> json) {
    return SourceConfig(
      active: json['ativo'] ?? false,
      url: json['url'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'ativo': active,
      'url': url,
    };
  }

  SourceConfig copyWith({
    bool? active,
    String? url,
  }) {
    return SourceConfig(
      active: active ?? this.active,
      url: url ?? this.url,
    );
  }
}
