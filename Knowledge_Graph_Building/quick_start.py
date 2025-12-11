from pathlib import Path

# 1. 创建示例Markdown文件
sample_md = """
---
title: Python编程基础
tags: [编程, Python, 教程]
categories: [技术]
date: 2024-01-15
---

# Python编程语言

Python是一种高级编程语言，由Guido van Rossum创建。它广泛应用于**数据科学**、**Web开发**和**人工智能**领域。

## 主要特性

- 简单易学：Python语法清晰简洁
- 强大的库：如NumPy、Pandas用于数据分析
- 面向对象：支持面向对象编程

## 相关技术

Python经常与以下技术一起使用：
- Django：Web框架
- TensorFlow：机器学习库
- Neo4j：图数据库
"""

# 创建示例文件
Path("./sample_markdown").mkdir(exist_ok=True)
with open("./sample_markdown/python_intro.md", "w", encoding="utf-8") as f:
    f.write(sample_md)

# 2. 运行知识图谱构建
from md_kg_builder import MDKnowledgeGraphBuilder

builder = MDKnowledgeGraphBuilder(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="12345678"
)

# 处理示例文件
processed = builder.process_directory("./sample_markdown")
builder.save_to_neo4j(processed)
builder.visualize_graph("sample_kg.html")