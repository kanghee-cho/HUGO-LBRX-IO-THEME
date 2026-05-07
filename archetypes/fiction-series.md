---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
fiction_type: "serial"
layout: "series"
description: ""
genre: ""                    # 연작소설 | 시리즈 등
status: "ongoing"            # ongoing | complete
tags: []
outputs:
  - HTML
  - RSS
---

<!-- 시리즈 소개글 (선택). 각 회차는 이 디렉토리 안에 fiction-episode 아키타입으로 생성하세요. -->
