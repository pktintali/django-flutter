import 'dart:convert';

class MisCard {
  final String title;
  final String mistake;
  final String lesson;
  final String created_at;
  MisCard({
    this.title,
    this.mistake,
    this.lesson,
    this.created_at,
  });

  MisCard copyWith({
    String title,
    String mistake,
    String lesson,
    String created_at,
  }) {
    return MisCard(
      title: title ?? this.title,
      mistake: mistake ?? this.mistake,
      lesson: lesson ?? this.lesson,
      created_at: created_at ?? this.created_at,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'title': title,
      'mistake': mistake,
      'lesson': lesson,
      'created_at': created_at,
    };
  }

  factory MisCard.fromMap(Map<String, dynamic> map) {
    return MisCard(
      title: map['title'],
      mistake: map['mistake'],
      lesson: map['lesson'],
      created_at: map['created_at'],
    );
  }

  String toJson() => json.encode(toMap());

  factory MisCard.fromJson(String source) => MisCard.fromMap(json.decode(source));

  @override
  String toString() {
    return 'MisCard(title: $title, mistake: $mistake, lesson: $lesson, created_at: $created_at)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
  
    return other is MisCard &&
      other.title == title &&
      other.mistake == mistake &&
      other.lesson == lesson &&
      other.created_at == created_at;
  }

  @override
  int get hashCode {
    return title.hashCode ^
      mistake.hashCode ^
      lesson.hashCode ^
      created_at.hashCode;
  }
}
