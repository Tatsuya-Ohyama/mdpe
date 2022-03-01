# mdpe.py

## 概要
* **m**ark**d**own **p**aper **e**ditor
* 本プログラムは、VSCode + markdown preview enhanced で、他言語の文章 (論文や報告書など) を markdown 形式で書くことを想定している。
* `<!-- -->` で囲まれた部分はコメントであり、プレビュー画面には非表示されないため、プレビューでは片方の言語で書かれた文章のみ確認できる。
* コメント側の言語の文章を読みたい場合には、`swap` モードで変換したファイルをプレビューすることで確認できる。
* 最終的に文章を `main` か `comment` モードで変換することで、連続するリストは一段落にまとめられ、片側の言語のみの markdown 形式で出力される。
* VSCode には、行をそのまま上や下に移動できる機能 (Windows では Alt+Shift + up/down; Mac では option + up/down; Linux では Shift+Ctrl + up/down) があるので、文章の構成を練り直しやすい。
* インデントでネストされたリストは、文の内包・並列関係を直感的に表示できるので、分かりやすい。なお、インデントは `main` あるいは `comment` モードでの変換時に削除される。


## 使用方法
```sh
$ mdpe.py [-h] [-O] OPERATION INPUT.md [OUTPUT.md]
```

* `-h`, `--help`
	: ヘルプメッセージを表示して終了する。
* `OPERATION`
	: 処理方法
	: * `swap`: 本文とコメントを入れ替える。
	: * `main`: 本文のみを出力する。
	: * `comment`: コメントのみを出力する。
* `INPUT.md`
	: 入力 markdown ファイル
* `OUTPUT.md`
	: 出力 markdown ファイル (Default: `-i` と同じファイル)
* `-O`
	: 上書きプロンプトを出さずに上書きする。


### 対象の markdown ファイルのルール
* 各文は、箇条書き (リスト) (`*`) で始める。この `*` は `main` や `comment` 処理での変換時に削除される。
* 各文の日本語に対応する英語は HTML のコメント `<!-- TEXT -->` として記述する (英語を本文とする場合は、コメントに日本語を記述する)。
* 同じ段落の文にする場合は、連続するリストとして記述する。
* 段落を分ける場合は、連続するリストブロック間に空行を加える。
* 段落に対する説明は第四見出し (`####` で始まる行) に記述する。この説明は `main` や `comment` 処理での変換時に削除される。
* 上記ルール以外の行は、そのまま出力される。
* 例:
	* 編集ファイル

		```txt
		## 電流結果の段落
		* 駆動電流の増加とともにその発光強度も増加する。 <!-- The luminous intensity is also increased with the increase of a driving current. -->
		* それは時の経過とともに増加していった。 <!-- That was increasing with the passage of time. -->

		## 圧力結果の段落
		* この圧力制御機構２は、空洞１１内部の圧力を制御する。 <!-- The pressure control mechanism 2 controls the pressure in a cavity 11. -->
		```

	* `comment` での出力ファイル

		```txt
		The luminous intensity is also increased with the increase of a driving current. That was increasing with the passage of time.

		The pressure control mechanism 2 controls the pressure in a cavity 11.
		```


## 動作要件
* Python3


## License
The MIT License (MIT)

Copyright (c) 2022 Tatsuya Ohyama


## Authors
* Tatsuya Ohyama


## ChangeLog
### Ver. 1.3 (2022-03-01)
* プログラム名を `papereditor.py` から `mdpe.py` に変更し、リポジトリに公開した。

### Ver. 1.2 (2022-03-01)
* `swap` モード時にネストされたリストのインデントが消えるバグを修正した。

### Ver. 1.1 (2022-02-21)
* 段落の説明を `####` に変更した。

### Ver. 1.0 (2022-02-21)
* 公開した。
