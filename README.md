# Hunter × Hunter Language Translator

<img width="927" height="764" alt="image" src="https://github.com/user-attachments/assets/a8e48476-54e8-41ff-80cd-1e70120a6e3c" />

**Try it here: [hxhlanguage.org](https://hxhlanguage.org)**

Type something in Japanese and the website translates it to the Hunter × Hunter language. Kanji, hiragana and katakana all work. You can change the colors and save the result as an image.

I'm a big fan of the manga and of Togashi, and I've wanted to make this for a long time.

## Running it

It's a static page, so there's nothing to install. Just open `index.html`.

"Copy Image" only works when the site is hosted over HTTPS, because browsers block clipboard access otherwise. If you open the file locally, use "Download PNG" instead.

## Files

- `index.html`: the whole app
- `hxh_sprites.js`: every character as a small image, all in one file
- `assets/`: favicon and header art
- `tools/`: Python scripts I used to cut the characters out of the reference chart and prepare the header art. You don't need them to run the site.
- `sources/`: the original images I traced from
  
## How it works under the hood

Kanji don't map onto the script one-to-one, so the text first gets turned into kana (its
reading). That part uses kuromoji.js, and it only downloads the moment you actually type a
kanji — if you stick to kana it never loads, so the page stays fast. From there each kana
is swapped for its glyph and painted onto a canvas, which is what you copy or download.

Fonts load from Google Fonts and the kanji dictionary from a CDN, so it wants internet the
first time around.

<img width="1368" height="822" alt="image" src="https://github.com/user-attachments/assets/b0639af7-73e0-43c7-8f12-f058aaa01cd8" />

  "You should enjoy the little detours to the fullest. Because that's where you'll find the things more important than what you want."
  
