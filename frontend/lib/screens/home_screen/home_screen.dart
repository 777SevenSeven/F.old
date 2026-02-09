import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/theme/app_colors.dart';
import '../../dtos/product_dto.dart';
import '../../dtos/message_dto.dart';
import '../../repositories/preferences_repository.dart';
import '../../repositories/search_repository.dart';
import '../../widgets/sidebar.dart';
import '../../widgets/chat_area.dart';
import '../../widgets/products_area.dart';
import 'home_screen_view_model.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _inputController = TextEditingController();
  final List<MessageDto> _messages = [];

  @override
  void initState() {
    super.initState();
  }

  HomeScreenViewModel _createViewModel(BuildContext context) {
    final prefsRepo = context.read<PreferencesRepository>();
    final searchRepo = context.read<SearchRepository>();
    final vm = HomeScreenViewModel(
      preferencesRepository: prefsRepo,
      searchRepository: searchRepo,
    );
    vm.loadInitialData();
    return vm;
  }

  Future<void> _onSendMessage(HomeScreenViewModel viewModel) async {
    final text = _inputController.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add(MessageDto(
        text: text,
        type: MessageType.user,
      ));
      _inputController.clear();
    });

    setState(() {
      _messages.add(MessageDto(
        text: 'Got it. Searching deals for "$text"...',
        type: MessageType.bot,
        metadata: {
          'status': 'searching',
          'filter': 'best_price',
        },
      ));
    });

    await viewModel.searchByTerm(text);

    Future.delayed(const Duration(milliseconds: 300), () {
      if (!mounted) return;
      setState(() {
        if (viewModel.offersStatus == HomeScreenStatus.content) {
          _messages.add(MessageDto(
            text: 'Found ${viewModel.totalProducts} items for "$text"!',
            type: MessageType.bot,
          ));
        } else if (viewModel.offersStatus == HomeScreenStatus.error) {
          _messages.add(MessageDto(
            text: 'Failed to search deals. Try again.',
            type: MessageType.bot,
          ));
        }
      });
    });
  }

  void _onNewChat() {
    setState(() {
      _messages.clear();
      _inputController.clear();
    });
  }

  void _onProductTap(ProductDto product) {
    // TODO: Implement navigation for the offer
    debugPrint('Selected product: ${product.title}');
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<HomeScreenViewModel>(
      create: _createViewModel,
      child: Consumer<HomeScreenViewModel>(
        builder: (context, viewModel, _) {
          final conversations = viewModel.conversations;
          final bestPriceProducts = viewModel.bestPriceProducts;
          final recentProducts = viewModel.recentProducts;
          final totalProducts = viewModel.totalProducts;

          return Scaffold(
            backgroundColor: AppColors.background,
            body: Row(
              children: [
                Sidebar(
                  conversations: conversations,
                  onNewChat: _onNewChat,
                  onConversationTap: (conversation) {
                    viewModel.fetchOffersByChatId(conversation.id);
                  },
                ),
                const VerticalDivider(width: 1, color: AppColors.divider),
                Expanded(
                  flex: 1,
                  child: ChatArea(
                    messages: _messages,
                    inputController: _inputController,
                    onSend: () => _onSendMessage(viewModel),
                    onBoost: () {
                      debugPrint('Boost ativado');
                    },
                  ),
                ),
                const VerticalDivider(width: 1, color: AppColors.divider),
                Expanded(
                  flex: 1,
                  child: ProductsArea(
                    bestPriceProducts: bestPriceProducts,
                    recentProducts: recentProducts,
                    totalProducts: totalProducts,
                    onProductTap: _onProductTap,
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  @override
  void dispose() {
    _inputController.dispose();
    super.dispose();
  }
}



