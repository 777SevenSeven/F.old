/// Search result item model
class SearchItem {
  final String origin;
  final String color;
  final String id;
  final String title;
  final String priceText;
  final String link;
  final String extraInfo;
  final String imageUrl;

  SearchItem({
    required this.origin,
    required this.color,
    required this.id,
    required this.title,
    required this.priceText,
    required this.link,
    this.extraInfo = '',
    this.imageUrl = '',
  });

  factory SearchItem.fromJson(Map<String, dynamic> json) {
    return SearchItem(
      origin: json['origem'] ?? '',
      color: json['cor'] ?? '🔵',
      id: json['id'] ?? '',
      title: json['titulo'] ?? '',
      priceText: json['preco_texto'] ?? '',
      link: json['link'] ?? '',
      extraInfo: json['info_extra'] ?? '',
      imageUrl: json['imagem_url'] ?? '',
    );
  }

  @override
  String toString() {
    return 'SearchItem(origin: $origin, title: $title, price: $priceText, link: $link, image: $imageUrl, extra: $extraInfo)';
  }

  Map<String, dynamic> toJson() {
    return {
      'origem': origin,
      'cor': color,
      'id': id,
      'titulo': title,
      'preco_texto': priceText,
      'link': link,
      'info_extra': extraInfo,
      'imagem_url': imageUrl,
    };
  }
}
