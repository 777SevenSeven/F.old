enum MessageType { user, bot }

class MessageDto {
  final String text;
  final MessageType type;
  final DateTime timestamp;
  final Map<String, dynamic>? metadata;

  MessageDto({
    required this.text,
    required this.type,
    DateTime? timestamp,
    this.metadata,
  }) : timestamp = timestamp ?? DateTime.now();

  factory MessageDto.fromJson(Map<String, dynamic> json) {
    return MessageDto(
      text: json['text'] as String? ?? '',
      type: json['type'] == 'user' ? MessageType.user : MessageType.bot,
      timestamp: json['timestamp'] != null ? DateTime.parse(json['timestamp'] as String) : DateTime.now(),
      metadata: json['metadata'] as Map<String, dynamic>?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'text': text,
      'type': type == MessageType.user ? 'user' : 'bot',
      'timestamp': timestamp.toIso8601String(),
      'metadata': metadata,
    };
  }
}
