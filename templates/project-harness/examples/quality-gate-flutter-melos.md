# 선택 항목: Flutter + Melos 모노레포

> 원본 프로젝트가 Flutter + Melos 모노레포라서 쓰던 설정입니다. 스택이 같을 때만 가져갑니다.

## 품질 게이트

FVM으로 고정한 Dart로 워크스페이스에 고정한 melos를 실행합니다. PATH의 bare `melos`는 전역 pub shim을 거쳐 시스템 Dart 버전에 따라 실패할 수 있어서 쓰지 않습니다.

```bash
fvm dart run melos bs                    # 의존성 설치
fvm dart run melos build                 # 코드 생성 (build_runner)
fvm dart run melos style:lint:analyze    # dart analyze
fvm dart run melos style:format          # 포맷 검사, 변경 있으면 exit 1
fvm dart run melos test                  # 전 패키지 테스트
```

`alias melos='fvm dart run melos'`를 걸어 두면 편합니다.

## 레이어 import 방향을 lint로 강제하기

`import_lint` 같은 패키지로 `domain/`이 `data/`, `presentation/`, `package:flutter`를 import하지 못하게 막으면 Invariant의 "문서" 항목 하나를 도구로 옮길 수 있습니다.

## 규칙 문서 크기 예산을 테스트로 강제하기

루트 `AGENTS.md`는 모든 세션에 들어가고, 주입되는 문서는 훅 출력 상한(약 10,000자)을 넘으면 경고로 대체됩니다. 커지는 것을 테스트로 막아 두면 편합니다.

```dart
// test/agents_doc_budget_test.dart
import 'dart:io';
import 'package:test/test.dart';

void main() {
  const injected = ['CONTRIBUTING.md', 'docs/coding-conventions.md'];
  const injectedLimit = 9000; // 훅 상한 10,000자에서 여유를 둔다

  for (final path in injected) {
    test('$path 는 주입 상한 안에 있다', () {
      final length = File(path).readAsStringSync().length;
      expect(length, lessThan(injectedLimit));
    });
  }

  test('중첩 AGENTS.md 마다 짝이 되는 CLAUDE.md 가 있다', () {
    final agents = Directory('.')
        .listSync(recursive: true)
        .whereType<File>()
        .where((f) => f.path.endsWith('/AGENTS.md') && !f.path.contains('/.'));
    for (final file in agents) {
      final claude = File(file.path.replaceFirst('AGENTS.md', 'CLAUDE.md'));
      expect(claude.existsSync(), isTrue, reason: '${claude.path} 없음');
    }
  });
}
```

Melos를 쓰면 루트 `test/`는 워크스페이스 패키지가 아니라서 `melos exec`에 걸리지 않습니다. 별도 스크립트(`melos test:utilities` 등)로 돌리고 `melos test`가 함께 실행하게 묶습니다.
