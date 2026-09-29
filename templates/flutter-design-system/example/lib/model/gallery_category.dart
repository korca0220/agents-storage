import 'gallery_entry.dart';

/// Figma 페이지 그룹과 같은 단위의 묶음 — "Foundations", "Actions" 등.
class GalleryCategory {
  const GalleryCategory(this.title, this.entries);

  final String title;

  final List<GalleryEntry> entries;
}
