import 'package:flutter/material.dart';

import 'screens/home_screen.dart';

void main() {
  runApp(const GalleryApp());
}

class GalleryApp extends StatelessWidget {
  const GalleryApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '{{product}} Design System',
      debugShowCheckedModeBanner: false,
      // 토큰이 생기면 {{PREFIX}}Theme.light()로 바꾼다.
      theme: ThemeData(useMaterial3: true),
      home: const HomeScreen(),
    );
  }
}
