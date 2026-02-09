import 'package:flutter/material.dart';
import '../core/theme/app_colors.dart';
import '../dtos/message_dto.dart';
import 'chat_message.dart';

class ChatArea extends StatelessWidget {
  final List<MessageDto> messages;
  final TextEditingController inputController;
  final VoidCallback? onSend;
  final VoidCallback? onBoost;

  const ChatArea({
    super.key,
    required this.messages,
    required this.inputController,
    this.onSend,
    this.onBoost,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: AppColors.chatBackground,
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            decoration: const BoxDecoration(
              border: Border(
                bottom: BorderSide(color: AppColors.divider),
              ),
            ),
            child: Row(
              children: [
                const Text(
                  'F.OLD',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                    color: Colors.white,
                    letterSpacing: 0.5,
                  ),
                ),
                const Spacer(),
                const Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Text(
                      'Chat with our deal-hunting assistant',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      'Most requested item: iPhone 12',
                      style: TextStyle(
                        fontSize: 12,
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ],
                ),
                const Spacer(),
                Row(
                  children: [
                    GestureDetector(
                      onTap: () => _showPlansDialog(context),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                        decoration: BoxDecoration(
                          color: AppColors.freeTierBadge,
                          borderRadius: BorderRadius.circular(999),
                        ),
                        child: const Text(
                          'FREE TIER',
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                            letterSpacing: 0.5,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    CircleAvatar(
                      radius: 16,
                      backgroundColor: AppColors.userBubble,
                      child: ClipOval(
                        child: Image.network(
                          'https://images.macrumors.com/t/vONeHh9Md_kfQ6gR6CFPjVffrwA=/1600x0/article-new/2023/09/iPhone-15-Models.jpg',
                          width: 28,
                          height: 28,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) => const Icon(
                            Icons.person,
                            size: 18,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(20),
              itemCount: messages.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.only(bottom: 16),
                  child: ChatMessage(message: messages[index]),
                );
              },
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              decoration: BoxDecoration(
                color: AppColors.userBubble,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: inputController,
                      style: const TextStyle(color: Colors.white, fontSize: 14),
                      decoration: const InputDecoration(
                        hintText: 'Type the used product you want, or use voice if you prefer...',
                        hintStyle: TextStyle(color: AppColors.textSecondary, fontSize: 13),
                        border: InputBorder.none,
                      ),
                      onSubmitted: (_) => onSend?.call(),
                    ),
                  ),
                  Container(
                    height: 32,
                    width: 1,
                    margin: const EdgeInsets.symmetric(horizontal: 12),
                    color: AppColors.divider,
                  ),
                  IconButton(
                    onPressed: () {},
                    icon: const Icon(Icons.mic, color: Colors.white),
                  ),
                  const SizedBox(width: 6),
                  Container(
                    height: 32,
                    width: 1,
                    color: Colors.white.withOpacity(0.4),
                  ),
                  TextButton.icon(
                    onPressed: onBoost,
                    icon: const Text('Use Boost', style: TextStyle(color: Colors.white, fontSize: 13)),
                    label: const Text('Boost', style: TextStyle(fontSize: 16)),
                    style: TextButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                      foregroundColor: Colors.white,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showPlansDialog(BuildContext context) {
    showDialog(
      context: context,
      barrierColor: Colors.black.withOpacity(0.65),
      builder: (_) => const _PlansDialog(),
    );
  }
}

class _PlansDialog extends StatelessWidget {
  const _PlansDialog();

  static const List<_PlanInfo> _plans = [
    _PlanInfo(
      name: 'FREE',
      subtitle: 'Free',
      oldPrice: null,
      features: ['3 items', 'Site/App alerts', 'Affiliate links'],
      buttonLabel: 'START FREE',
      highlighted: false,
    ),
    _PlanInfo(
      name: 'TRIGGER',
      subtitle: 'R\$ 29.90/mo',
      oldPrice: 'R\$ 59.90/mo',
      features: ['15 items', 'WhatsApp alerts', 'AI: Trade-in check', 'Sniper badge'],
      buttonLabel: 'SUBSCRIBE TRIGGER',
      highlighted: false,
    ),
    _PlanInfo(
      name: 'PROSPECTOR PRO',
      subtitle: 'R\$ 79.90/mo',
      oldPrice: 'R\$ 149.90/mo',
      ribbon: 'Most Popular',
      features: ['100 items', 'Price history', 'AI: Condition/defects', 'Stocker badge'],
      buttonLabel: 'SUBSCRIBE PRO',
      highlighted: true,
    ),
    _PlanInfo(
      name: 'ENTERPRISE',
      subtitle: 'R\$ 197.90/mo',
      oldPrice: 'R\$ 397.90/mo',
      features: ['Unlimited', 'Reports', 'AI: Logistics/shipping', 'Entrepreneur badge'],
      buttonLabel: 'SUBSCRIBE ENTERPRISE',
      highlighted: false,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    const double horizontalPadding = 24;
    const double verticalPadding = 20;
    const double separatorWidth = 1;
    const double cardSpacing = 8;
    final int separatorsCount = _plans.length - 1;
    final double totalCardsWidth = _PlanCard.cardWidth * _plans.length;
    final double totalSeparatorsWidth = separatorsCount <= 0 ? 0 : separatorsCount * (separatorWidth + cardSpacing);
    final double containerWidth = totalCardsWidth + totalSeparatorsWidth + (horizontalPadding * 2);
    final double modalWidth = containerWidth + 40;

    final planRowChildren = <Widget>[];
    for (var i = 0; i < _plans.length; i++) {
      if (i > 0) {
        planRowChildren.add(const SizedBox(width: cardSpacing / 2));
        planRowChildren.add(Container(
          width: separatorWidth,
          height: _PlanCard.cardHeight,
          color: AppColors.divider,
        ));
        planRowChildren.add(const SizedBox(width: cardSpacing / 2));
      }
      planRowChildren.add(_PlanCard(info: _plans[i]));
    }

    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
      child: SingleChildScrollView(
        child: Container(
          width: modalWidth,
          constraints: BoxConstraints(maxWidth: modalWidth + 40),
          decoration: BoxDecoration(
            color: AppColors.chatBackground,
            borderRadius: BorderRadius.circular(18),
            border: Border.all(color: AppColors.divider),
          ),
          padding: const EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: verticalPadding),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                children: [
                  const Text(
                    'Plans',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                  const Spacer(),
                  IconButton(
                    splashRadius: 18,
                    onPressed: () => Navigator.of(context).pop(),
                    icon: const Icon(Icons.close, color: Colors.white70),
                  ),
                ],
              ),
              const Divider(color: AppColors.divider),
              const SizedBox(height: 12),
              Align(
                alignment: Alignment.center,
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: planRowChildren,
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'Launch promo valid for the first 100 users. 12 spots left.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Color(0xFFFF4D4F),
                  fontSize: 11,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(height: 6),
              const Center(
                child: Text(
                  '02:15:45',
                  style: TextStyle(
                    color: Color(0xFFFF4D4F),
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _PlanInfo {
  final String name;
  final String subtitle;
  final String? oldPrice;
  final List<String> features;
  final String buttonLabel;
  final bool highlighted;
  final String? ribbon;

  const _PlanInfo({
    required this.name,
    required this.subtitle,
    this.oldPrice,
    required this.features,
    required this.buttonLabel,
    this.ribbon,
    this.highlighted = false,
  });
}

class _PlanCard extends StatelessWidget {
  static const double cardWidth = 218;
  static const double cardHeight = 300;
  final _PlanInfo info;

  const _PlanCard({required this.info});

  @override
  Widget build(BuildContext context) {
    final cardColor = info.highlighted ? const Color(0xFF1E1B12) : AppColors.botBubble;
    final accentColor = info.highlighted ? const Color(0xFFF3C347) : Colors.white;

    return SizedBox(
      width: cardWidth,
      height: cardHeight,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: cardColor,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: info.highlighted ? const Color(0xFFF3C347) : AppColors.divider),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (info.ribbon != null)
              Container(
                margin: const EdgeInsets.only(bottom: 8),
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFFF3C347),
                  borderRadius: BorderRadius.circular(999),
                ),
                child: Text(
                  info.ribbon!,
                  style: const TextStyle(
                    color: Colors.black,
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            Text(
              info.name,
              style: TextStyle(
                color: accentColor,
                fontSize: 16,
                fontWeight: FontWeight.w700,
                letterSpacing: 0.8,
              ),
            ),
            const SizedBox(height: 4),
            if (info.oldPrice != null)
              Text(
                info.oldPrice!,
                style: const TextStyle(
                  color: Colors.white54,
                  fontSize: 12,
                  decoration: TextDecoration.lineThrough,
                ),
              ),
            Text(
              info.subtitle,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 12),
            ...info.features.map(
              (feature) => Padding(
                padding: const EdgeInsets.only(bottom: 6),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('- ', style: TextStyle(color: Colors.white70)),
                    Expanded(
                      child: Text(
                        feature,
                        style: const TextStyle(color: Colors.white70, fontSize: 13),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 12),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {},
                style: ElevatedButton.styleFrom(
                  backgroundColor: info.highlighted ? const Color(0xFFF3C347) : Colors.transparent,
                  foregroundColor: info.highlighted ? Colors.black : Colors.white,
                  side: BorderSide(color: accentColor),
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
                child: Text(
                  info.buttonLabel,
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 13,
                    color: info.highlighted ? Colors.black : Colors.white,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}





