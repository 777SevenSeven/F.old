class ProductDto {
  final String title;
  final String price;
  final String imageUrl;
  final String marketplace;
  final String? badge;
  final String? link;

  ProductDto({
    required this.title,
    required this.price,
    required this.imageUrl,
    required this.marketplace,
    this.badge,
    this.link,
  });

  factory ProductDto.fromJson(Map<String, dynamic> json) {
    return ProductDto(
      title: json['title'] as String? ?? '',
      price: json['price'] as String? ?? '',
      imageUrl: json['imageUrl'] as String? ?? json['image_url'] as String? ?? '',
      marketplace: json['marketplace'] as String? ?? '',
      badge: json['badge'] as String?,
      link: json['link'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'price': price,
      'imageUrl': imageUrl,
      'marketplace': marketplace,
      'badge': badge,
      'link': link,
    };
  }
}
