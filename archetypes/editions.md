---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
edition_number: 0
description: ""
accent_color: "emerald"   # rose | pink | fuchsia | violet | indigo | sky | cyan | teal | emerald | lime | amber | orange
books:
  - slug: ""              # shelf 콘텐츠 파일명 (확장자 제외, 예: norwegian-wood)
    reason: ""            # 선정 이유 (한 줄 인용 형식)
tags: []
outputs:
  - HTML
  - RSS
---

<!-- 편집자 노트 (선택) — prose 영역에 표시됩니다 -->
