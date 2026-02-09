import 'package:flutter/material.dart';
import '../core/theme/app_colors.dart';
import '../dtos/product_dto.dart';
import 'products_carousel.dart';

class ProductsArea extends StatelessWidget {
  final List<ProductDto> bestPriceProducts;
  final List<ProductDto> recentProducts;
  final int totalProducts;
  final Function(ProductDto)? onProductTap;

  const ProductsArea({
    super.key,
    required this.bestPriceProducts,
    required this.recentProducts,
    this.totalProducts = 0,
    this.onProductTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: AppColors.outputBackground,
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                const Text(
                  'Os ouros que estamos encontrando',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 6),
                RichText(
                  text: TextSpan(
                    style: const TextStyle(fontSize: 13),
                    children: [
                      const TextSpan(
                        text: 'Encontramos ',
                        style: TextStyle(color: Colors.white),
                      ),
                      TextSpan(
                        text: '$totalProducts',
                        style: const TextStyle(
                          color: AppColors.accent,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const TextSpan(
                        text: ' New items today!',
                        style: TextStyle(color: Colors.white),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 14),
                Container(
                  width: double.infinity,
                  height: 2,
                  color: AppColors.divider,
                )
              ],
            ),
          ),
          Expanded(
            child: SingleChildScrollView(
              child: Column(
                children: [
                  ProductsCarousel(
                    title: 'Best prices!',
                    products: bestPriceProducts,
                    onProductTap: onProductTap,
                  ),
                  const SizedBox(height: 30),
                  ProductsCarousel(
                    title: 'Latest deals!',
                    products: recentProducts,
                    onProductTap: onProductTap,
                  ),
                  const SizedBox(height: 20),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}



