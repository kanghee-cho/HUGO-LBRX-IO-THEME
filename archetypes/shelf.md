---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
description: ""

# ── 서지 정보 (Bibliographic) ──────────────────────────────────────
author: ""
publisher: ""        # 출판사
publish_year: ""     # 출판연도 (예: 2021)
isbn: ""             # ISBN-13 (예: 978-0-00-000000-0)
pages: 0             # 총 페이지 수
translator: ""       # 번역자 (원서가 아닐 경우)
original_title: ""   # 원제 (번역서인 경우)

# ── 서고 정보 (Physical / Library) ─────────────────────────────────
call_number: ""      # 서고번호 (예: KOR-HAN-001)
owned: true          # 보유 여부 (true / false)
condition: ""        # 책 상태: 새것 / 양호 / 보통 / 불량

# ── 독서 기록 (Reading Record) ──────────────────────────────────────
status: "read"       # read / reading / wishlist / abandoned
rating: 0.0          # 평점 0.5~5.0 (반별 지원)
read_date: ""        # 완독일 (YYYY-MM-DD)

# ── 분류 & 큐레이션 (Classification) ───────────────────────────────
genre: ""            # 장르 (예: Literary Fiction, 역사소설, SF)
mood_tags: []        # 분위기 태그 (예: ["조용한", "우울한", "희망적"])
recommended_for: ""  # 추천 대상 (예: "깊은 슬픔을 마주하고 싶은 이")
tags: []             # 일반 태그

# ── 커버 이미지 ─────────────────────────────────────────────────────
cover: ""            # 이미지 경로 또는 URL
---

<!-- 책 리뷰를 여기에 작성하세요 -->
