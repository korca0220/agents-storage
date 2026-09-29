import 'package:flutter/material.dart';

import '../data/gallery_data.dart';
import 'category_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('{{product}} Design System')),
      body: galleryData.isEmpty
          ? const Center(child: Text('등록된 쇼케이스가 없습니다.'))
          : ListView.separated(
              itemCount: galleryData.length,
              separatorBuilder: (_, _) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final category = galleryData[index];

                return ListTile(
                  title: Text(category.title),
                  subtitle: Text('${category.entries.length}개'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () => Navigator.of(context).push(
                    MaterialPageRoute<void>(builder: (_) => CategoryScreen(category: category)),
                  ),
                );
              },
            ),
    );
  }
}
