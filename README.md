# Hunter × Hunter Language Translator

Type something in Japanese and it gets rewritten in the Hunter × Hunter language. Kanji, hiragana, katakana all work. You can recolor
the result and save it as an image.

I made this because I'm a fan of the manga and have had the idea since long .


## Running it

Static page, nothing to install. Just open `index.html`.

One thing: the "Copy Image" button only works once the site is hosted (it needs HTTPS).
That's a browser rule, not a bug, so it won't copy if you open the file straight off your
disk. "Download PNG" works no matter what.

## What's in the folder

- `index.html` — the app, all of it
- `hxh_sprites.js` — every character as a tiny image, baked into one file
- `assets/` — the favicon and the artwork in the header
- `tools/` — the Python I used to cut the characters out of the reference chart and prep
  the header art. Not needed to run the site, I just keep them here so I don't lose them.
- `sources/` — the original images I traced everything from

## How it works under the hood

Kanji don't map onto the script one-to-one, so the text first gets turned into kana (its
reading). That part uses kuromoji.js, and it only downloads the moment you actually type a
kanji — if you stick to kana it never loads, so the page stays fast. From there each kana
is swapped for its glyph and painted onto a canvas, which is what you copy or download.

Fonts load from Google Fonts and the kanji dictionary from a CDN, so it wants internet the
first time around.


