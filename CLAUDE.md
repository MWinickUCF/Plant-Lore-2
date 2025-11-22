# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains two Project Gutenberg eBooks related to plant folklore and botanical history:

1. **Plant Lore Legends and Lyrics Text File.txt** (1.8MB, 35,133 lines)
   - Author: Richard Folkard, Jun. (1884)
   - Content: Myths, traditions, superstitions, and folklore of the plant kingdom
   - Includes both Continental and Indian plant lore

2. **Plant Lore and Garden Craft of Shakespeare.txt** (918KB, 25,705 lines)
   - Author: Henry Nicholson Ellacombe
   - Content: Analysis of plants mentioned in Shakespeare's works
   - Combines literary history with botanical knowledge

## File Format

Both files are:
- UTF-8 encoded text with BOM
- CRLF line endings (Windows-style)
- Public domain content from Project Gutenberg

## Repository Structure

This is a content-only repository with no build system, tests, or executable code. The repository serves as an archive of historical botanical and literary texts.

## Potential Development Areas

If this repository evolves beyond simple text storage, future development might include:

- **Text parsing**: Extract structured data about specific plants, myths, or Shakespeare references
- **Index creation**: Build searchable indices of plant names, folklore themes, or literary quotations
- **Format conversion**: Convert to Markdown, HTML, or other formats for better readability
- **Cross-referencing**: Link related content between the two texts
- **Data extraction**: Create structured datasets (JSON/CSV) of plant folklore or Shakespeare botanical references

## Working with the Texts

When working with these files:
- Both files are large; use tools like `grep`, `head`, `tail`, or the Read tool with offset/limit parameters for efficient navigation
- The texts contain historical spellings and formatting conventions from the original publications
- Greek text is transliterated between +plus signs+ in the Shakespeare text
- Italicized text appears between _underscores_ in the original formatting
