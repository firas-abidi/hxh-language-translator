"""Build the Japanese version of the site (ja/index.html) from index.html.

The page itself is already bilingual, so the Japanese version is the same page
with a Japanese title and description for search results and link previews,
lang="ja", and file paths pointing one folder up. Google and Yahoo! JAPAN use the
hreflang links in both pages to show each searcher the version in their language.

Run it after every change to index.html, before committing:
    py -3 tools/build_ja.py
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
OUT_DIR = os.path.join(ROOT, 'ja')
OUT = os.path.join(OUT_DIR, 'index.html')

TITLE_JA = 'ハンター言語翻訳機 | Hunter × Hunter Language Translator'
DESC_JA = ('日本語を入力すると、ハンター×ハンターの文字で表示します。'
           '漢字・ひらがな・カタカナに対応。好きな色を選んで画像として保存できます。'
           '冨樫義博先生へのファンメイドのトリビュートです。')
OG_DESC_JA = '日本語を入力すると、ハンター×ハンターの文字で表示します。好きな色を選んで画像として保存できます。'

html = io.open(SRC, encoding='utf-8', newline='').read()


def swap(old, new, count=1):
    """Replace text that must exist exactly `count` times, so a changed index.html
    makes the build fail loudly instead of producing a half-Japanese page."""
    global html
    found = html.count(old)
    if found != count:
        raise SystemExit(f'build_ja: expected {count}x {old[:60]!r}, found {found}x')
    html = html.replace(old, new)


def swap_tag_content(prefix, new_content):
    """Replace the content="..." of the single tag that starts with `prefix`."""
    global html
    start = html.find(prefix)
    if start < 0 or html.find(prefix, start + 1) >= 0:
        raise SystemExit(f'build_ja: expected exactly one tag starting {prefix!r}')
    open_q = start + len(prefix)
    close_q = html.index('"', open_q)
    html = html[:open_q] + new_content + html[close_q:]


swap('<html lang="en">', '<html lang="ja">')
swap('<title>Hunter × Hunter Language Translator | ハンター言語翻訳機</title>', f'<title>{TITLE_JA}</title>')
swap_tag_content('<meta name="description" content="', DESC_JA)
swap('<link rel="canonical" href="https://hxhlanguage.org/">', '<link rel="canonical" href="https://hxhlanguage.org/ja/">')
swap('<meta property="og:locale" content="en_US">', '<meta property="og:locale" content="ja_JP">')
swap('<meta property="og:title" content="Hunter × Hunter Language Translator">',
     '<meta property="og:title" content="ハンター言語翻訳機 | Hunter × Hunter Language Translator">')
swap_tag_content('<meta property="og:description" content="', OG_DESC_JA)
swap('<meta property="og:url" content="https://hxhlanguage.org/">', '<meta property="og:url" content="https://hxhlanguage.org/ja/">')

# on the Japanese page the Japanese explanation may be used as the search snippet
swap('<span class="jp" lang="ja" data-nosnippet>', '<span class="jp" lang="ja">')

# files live one folder up
swap('href="assets/', 'href="../assets/', count=2)
swap('src="assets/', 'src="../assets/', count=3)
swap('<script src="hxh_sprites.js">', '<script src="../hxh_sprites.js">')

os.makedirs(OUT_DIR, exist_ok=True)
io.open(OUT, 'w', encoding='utf-8', newline='').write(html)
print('built ja/index.html')
