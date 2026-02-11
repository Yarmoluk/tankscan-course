#!/usr/bin/env python3
"""
Build the TankScan knowledge base from the textbook markdown files.
This script reads all chapter content and creates a single knowledge base file
that the chatbot uses as context.
"""

import os
from pathlib import Path


def build_knowledge_base():
    """Read all markdown files and compile into a single knowledge base."""
    docs_dir = Path(__file__).parent.parent / "docs"
    knowledge_parts = []

    # Read the course description
    course_desc = docs_dir / "course-description.md"
    if course_desc.exists():
        knowledge_parts.append(f"# COURSE DESCRIPTION\n\n{course_desc.read_text()}")

    # Read the glossary
    glossary = docs_dir / "glossary" / "index.md"
    if glossary.exists():
        knowledge_parts.append(f"# GLOSSARY\n\n{glossary.read_text()}")

    # Read all chapter files
    chapters_dir = docs_dir / "chapters"
    if chapters_dir.exists():
        for chapter_dir in sorted(chapters_dir.iterdir()):
            if chapter_dir.is_dir():
                index_file = chapter_dir / "index.md"
                if index_file.exists():
                    content = index_file.read_text()
                    knowledge_parts.append(content)

    # Read the learning graph
    learning_graph = docs_dir / "learning-graph" / "index.md"
    if learning_graph.exists():
        knowledge_parts.append(
            f"# LEARNING GRAPH\n\n{learning_graph.read_text()}"
        )

    # Combine all parts
    knowledge_base = "\n\n---\n\n".join(knowledge_parts)

    # Write the knowledge base file
    output_path = Path(__file__).parent / "knowledge_base.txt"
    output_path.write_text(knowledge_base)

    # Print stats
    word_count = len(knowledge_base.split())
    print(f"Knowledge base built successfully!")
    print(f"  - Source: {docs_dir}")
    print(f"  - Output: {output_path}")
    print(f"  - Word count: {word_count:,}")
    print(f"  - Character count: {len(knowledge_base):,}")
    print(f"  - Sections: {len(knowledge_parts)}")

    return knowledge_base


if __name__ == "__main__":
    build_knowledge_base()
