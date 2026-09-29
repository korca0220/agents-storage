import 'package:flutter/widgets.dart';

/// 갤러리의 항목 하나 — 컴포넌트 또는 토큰 그룹과 그 쇼케이스.
class GalleryEntry {
  const GalleryEntry(this.title, this.builder);

  final String title;

  final WidgetBuilder builder;
}
