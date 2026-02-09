import 'package:flutter/material.dart';
import '../core/theme/app_colors.dart';
import '../dtos/conversation_dto.dart';

class Sidebar extends StatelessWidget {
  final List<ConversationDto> conversations;
  final VoidCallback? onNewChat;
  final Function(ConversationDto)? onConversationTap;

  const Sidebar({
    super.key,
    required this.conversations,
    this.onNewChat,
    this.onConversationTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 220,
      color: AppColors.sidebar,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.menu, color: Colors.white, size: 20),
                    Spacer(),
                    Icon(Icons.search, color: Colors.white, size: 20),
                  ],
                ),
                const SizedBox(height: 20),
                const Row(
                  children: [
                    Text(
                      'F.OLD',
                      style: TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.w900,
                        fontStyle: FontStyle.italic,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                InkWell(
                  onTap: onNewChat,
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                    decoration: BoxDecoration(
                      border: Border.all(color: AppColors.divider),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Row(
                      children: [
                        Icon(Icons.add, size: 16, color: Colors.white),
                        SizedBox(width: 8),
                        Text(
                          'Nova conversa',
                          style: TextStyle(fontSize: 13, color: Colors.white),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 16),
            child: Text(
              'Conversas',
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.bold,
                color: AppColors.textSecondary,
              ),
            ),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: conversations.isNotEmpty
                ? ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 8),
                    itemCount: conversations.length,
                    itemBuilder: (context, index) {
                      final conversation = conversations[index];
                      return InkWell(
                        onTap: () => onConversationTap?.call(conversation),
                        borderRadius: BorderRadius.circular(8),
                        child: Container(
                          margin: const EdgeInsets.symmetric(vertical: 2),
                          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
                          child: Row(
                            children: [
                              Icon(
                                conversation.icon,
                                size: 16,
                                color: AppColors.textSecondary,
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Text(
                                  conversation.title,
                                  style: const TextStyle(
                                    fontSize: 13,
                                    color: Color(0xFFDDDDDD),
                                  ),
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  )
                : const Center(
                    child: Padding(
                      padding: EdgeInsets.symmetric(horizontal: 16),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.forum_outlined, color: AppColors.textSecondary),
                          SizedBox(height: 8),
                          Text(
                            'Nenhuma conversa ainda',
                            style: TextStyle(color: AppColors.textSecondary, fontSize: 12),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                  ),
          ),
        ],
      ),
    );
  }
}
