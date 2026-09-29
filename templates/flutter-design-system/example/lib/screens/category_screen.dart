import 'package:flutter/material.dart';

import '../model/gallery_category.dart';
import 'showcase_screen.dart';

class CategoryScreen extends StatelessWidget {
  const CategoryScreen({super.key, required this.category});

  final GalleryCategory category;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(category.title)),
      body: ListView.separated(
        itemCount: category.entries.length,
        separatorBuilder: (_, _) => const Divider(height: 1),
        itemBuilder: (context, index) {
          final entry = category.entries[index];

          return ListTile(
            title: Text(entry.title),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute<void>(builder: (_) => ShowcaseScreen(entry: entry)),
            ),
          );
        },
      ),
    );
  }
}
