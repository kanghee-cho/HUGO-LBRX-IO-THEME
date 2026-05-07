---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
episode: 1                   # 회차 번호
description: ""
word_count: 0
tags: []
outputs:
  - HTML
  - RSS
---

<!-- Write this episode here. Use --- to insert a section break (✦ ornament). -->
