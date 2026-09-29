import 'package:flutter/material.dart';

import '../model/gallery_entry.dart';

class ShowcaseScreen extends StatelessWidget {
  const ShowcaseScreen({super.key, required this.entry});

  final GalleryEntry entry;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(entry.title)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: entry.builder(context),
      ),
    );
  }
}
