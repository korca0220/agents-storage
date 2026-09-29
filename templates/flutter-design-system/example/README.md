# {{package}} example — 컴포넌트 갤러리

디자인 시스템 컴포넌트를 눈으로 확인하는 쇼케이스 앱이다. 플랫폼 폴더는 템플릿에 없으므로 처음 한 번 만든다.

```bash
flutter create --platforms=ios,android .
flutter run
```

- 갤러리 뼈대(홈·카테고리·상세 화면)는 Material 기본 위젯만 쓴다 — 디자인 시스템이 비어 있어도 빌드된다.
- 토큰이 생기면 `main.dart`의 테마를 `{{PREFIX}}Theme.light()`로 바꾼다.
- 컴포넌트를 추가하면 `lib/showcases/<group>/<name>_showcase.dart`를 만들고 `lib/data/gallery_data.dart`에 등록한다. 쇼케이스는 명세의 **모든 변형 축과 Disabled**를 한 화면에 펼친다 — 수동 렌더 대조의 기준이 된다.
