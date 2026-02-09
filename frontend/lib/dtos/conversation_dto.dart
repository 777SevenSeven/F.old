import 'package:flutter/material.dart';

class ConversationDto {
  final String id;
  final String title;
  final IconData icon;
  final DateTime lastUpdated;

  ConversationDto({
    required this.id,
    required this.title,
    required this.icon,
    DateTime? lastUpdated,
  }) : lastUpdated = lastUpdated ?? DateTime.now();

  factory ConversationDto.fromJson(Map<String, dynamic> json) {
    return ConversationDto(
      id: json['id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      icon: _iconFromString(json['icon'] as String?),
      lastUpdated: json['lastUpdated'] != null ? DateTime.parse(json['lastUpdated'] as String) : DateTime.now(),
    );
  }

  static IconData _iconFromString(String? iconName) {
    switch (iconName) {
      case 'smartphone':
        return Icons.smartphone;
      case 'videogame':
        return Icons.videogame_asset;
      case 'laptop':
        return Icons.laptop;
      case 'tv':
        return Icons.tv;
      default:
        return Icons.chat_bubble_outline;
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'lastUpdated': lastUpdated.toIso8601String(),
    };
  }
  
}
