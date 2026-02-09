import 'package:flutter/material.dart';
import '../dtos/product_dto.dart';
import 'product_card.dart';

class ProductsCarousel extends StatefulWidget {
  final String title;
  final List<ProductDto> products;
  final Function(ProductDto)? onProductTap;

  const ProductsCarousel({
    super.key,
    required this.title,
    required this.products,
    this.onProductTap,
  });

  @override
  State<ProductsCarousel> createState() => _ProductsCarouselState();
}

class _ProductsCarouselState extends State<ProductsCarousel> {
  final ScrollController _scrollController = ScrollController();
  static const double _scrollAmount = 200;

  void _scrollLeft() {
    final target = (_scrollController.offset - _scrollAmount).clamp(
      0.0,
      _scrollController.position.maxScrollExtent,
    );
    _scrollController.animateTo(
      target,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  void _scrollRight() {
    final target = (_scrollController.offset + _scrollAmount).clamp(
      0.0,
      _scrollController.position.maxScrollExtent,
    );
    _scrollController.animateTo(
      target,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Text(
            widget.title,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
            textAlign: TextAlign.center,
          ),
        ),
        const SizedBox(height: 16),
        SizedBox(
          height: 265.74,
          child: Row(
            children: [
              IconButton(
                onPressed: _scrollLeft,
                icon: const Icon(Icons.chevron_left, color: Colors.white, size: 32),
              ),
              Expanded(
                child: ListView.builder(
                  controller: _scrollController,
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                  itemCount: widget.products.length,
                  itemBuilder: (context, index) {
                    return Padding(
                      padding: const EdgeInsets.only(right: 16),
                      child: ProductCard(
                        product: widget.products[index],
                        onTap: () => widget.onProductTap?.call(widget.products[index]),
                      ),
                    );
                  },
                ),
              ),
              IconButton(
                onPressed: _scrollRight,
                icon: const Icon(Icons.chevron_right, color: Colors.white, size: 32),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
