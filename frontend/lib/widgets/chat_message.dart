import 'package:flutter/material.dart';
import '../core/theme/app_colors.dart';
import '../dtos/message_dto.dart';

class ChatMessage extends StatelessWidget {
  final MessageDto message;

  const ChatMessage({
    super.key,
    required this.message,
  });

  @override
  Widget build(BuildContext context) {
    final isUser = message.type == MessageType.user;

    return Row(
      mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (!isUser) ...[
          const CircleAvatar(
            radius: 16,
            backgroundColor: AppColors.sidebar,
            child: Icon(Icons.smart_toy, size: 18, color: AppColors.accent),
          ),
          const SizedBox(width: 10),
        ],
        Flexible(
          child: Container(
            constraints: const BoxConstraints(maxWidth: 400),
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: isUser ? AppColors.userBubble : AppColors.botBubble,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  isUser ? 'You' : 'Prospector AI',
                  style: const TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  message.text,
                  style: const TextStyle(
                    fontSize: 14,
                    color: Colors.white,
                  ),
                ),
                if (message.metadata != null) ...[
                  const SizedBox(height: 10),
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: Colors.black,
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Gemini is thinking:',
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: AppColors.accent,
                          ),
                        ),
                        const SizedBox(height: 6),
                        ...message.metadata!.entries.map((entry) => Padding(
                              padding: const EdgeInsets.only(top: 2),
                              child: Text(
                                '${entry.key}: ${entry.value}',
                                style: TextStyle(
                                  fontSize: 11,
                                  fontFamily: 'monospace',
                                  color: Colors.grey[400],
                                ),
                              ),
                            )),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
        if (isUser) ...[
          const SizedBox(width: 10),
          const CircleAvatar(
            radius: 16,
            backgroundColor: AppColors.badgeBackground,
            child: Icon(Icons.person, size: 18, color: Colors.white),
          ),
        ],
      ],
    );
  }
}


