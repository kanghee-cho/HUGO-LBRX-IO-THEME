---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
fiction_type: "standalone"   # standalone | (series uses fiction-series archetype)
description: ""
genre: ""                    # 단편소설 | 시 | 에세이 등
word_count: 0
tags: []
outputs:
  - HTML
  - RSS
---

<!-- Write your story here. Use --- to insert a section break (✦ ornament). -->
