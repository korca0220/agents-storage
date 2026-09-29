// 분류를 다 채우기 전에는 쓰이지 않는 값이 있다.
// ignore_for_file: unused_field

import 'package:flutter_test/flutter_test.dart';

/// 컴포넌트 문서 번호별 Semantics 검증 분류 — 정의는 lib/AGENTS.md §8.
enum _SemanticsDisposition { contract, conditional, delegated, excluded }

void main() {
  test('classifies every design-system component for semantics verification', () {
    // docs/components/NN-*.md 번호를 빠짐없이 적는다. scripts/verify-docs.mjs가 문서 수와 대조한다.
    const dispositions = <int, _SemanticsDisposition>{
      // 1: _SemanticsDisposition.excluded,
    };

    expect(dispositions.keys, orderedEquals(List<int>.generate(dispositions.length, (index) => index + 1)));
  });
}
