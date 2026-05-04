#!/bin/bash
# Standardize Le Chat filenames across raw and clean trees.
# Targets:
#   lechat_fast_* → le_chat_fast_*
#   lechat_thinking_* → le_chat_thinking_*
#   le_chat_think_* → le_chat_thinking_*
#   Strip descriptive suffixes from prompt_011 and prompt_012 in thinking/blog/
#   Fix lechat_fast_news_prompt_012txt.txt typo

set -e

for tree in llm_continuations llm_continuations_clean; do
  base="data/experiment/$tree"
  
  # 1. lechat_fast → le_chat_fast
  find "$base/le_chat_fast/" -name "lechat_fast_*.txt" 2>/dev/null | while read -r f; do
    new=$(echo "$f" | sed 's|lechat_fast_|le_chat_fast_|')
    mv "$f" "$new"
  done
  
  # 2. lechat_thinking → le_chat_thinking
  find "$base/le_chat_thinking/" -name "lechat_thinking_*.txt" 2>/dev/null | while read -r f; do
    new=$(echo "$f" | sed 's|lechat_thinking_|le_chat_thinking_|')
    mv "$f" "$new"
  done
  
  # 3. le_chat_think → le_chat_thinking (prefix only, careful not to double-rename)
  find "$base/le_chat_thinking/" -name "le_chat_think_*.txt" -not -name "le_chat_thinking_*.txt" 2>/dev/null | while read -r f; do
    new=$(echo "$f" | sed 's|le_chat_think_|le_chat_thinking_|')
    mv "$f" "$new"
  done
  
  # 4. Fix the .txt.txt typo
  if [ -f "$base/le_chat_fast/news/le_chat_fast_news_prompt_012txt.txt" ]; then
    mv "$base/le_chat_fast/news/le_chat_fast_news_prompt_012txt.txt" "$base/le_chat_fast/news/le_chat_fast_news_prompt_012.txt"
  fi
done

# 5. Strip descriptive suffixes from the two prompt_011 and prompt_012 files
# Run only in clean tree (raw versions may still have descriptive names; check separately)
for tree in llm_continuations_clean llm_continuations; do
  base="data/experiment/$tree/le_chat_thinking/blog"
  
  for old in "$base"/le_chat_thinking_blog_prompt_011_*.txt; do
    [ -e "$old" ] || continue
    mv "$old" "$base/le_chat_thinking_blog_prompt_011.txt"
  done
  
  for old in "$base"/le_chat_thinking_blog_prompt_012_*.txt; do
    [ -e "$old" ] || continue
    mv "$old" "$base/le_chat_thinking_blog_prompt_012.txt"
  done
done

echo "Done. Verifying..."
echo ""
echo "Le Chat Fast distinct prefixes:"
find data/experiment/llm_continuations_clean/le_chat_fast/ -name "*.txt" -exec basename {} \; | grep -oE '^[a-z_]+(_prompt)' | sed 's|_prompt||' | sort | uniq -c
echo ""
echo "Le Chat Thinking distinct prefixes:"
find data/experiment/llm_continuations_clean/le_chat_thinking/ -name "*.txt" -exec basename {} \; | grep -oE '^[a-z_]+(_prompt)' | sed 's|_prompt||' | sort | uniq -c

