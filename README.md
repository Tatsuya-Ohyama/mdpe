# papereditor.py

## 概要
論文用の markdown 形式のファイルを変換するプログラム


## 使用方法
```sh
$ papereditor.py [-h] OPERATION -i INPUT.md [-o OUTPUT.md] [-O]
```

* `-h`, `--help`
	: ヘルプメッセージを表示して終了する。
* `OPERATION`
	: 処理方法
	: * `swap`: 本文とコメントを入れ替える。
	: * `main`: 本文のみを出力する。
	: * `comment`: コメントのみを出力する。
* `-i INPUT.md`
	: 入力 markdown ファイル
* `-o OUTPUT.md`
	: 出力 markdown ファイル (Default: `-i` と同じファイル)
* `-O`
	: 上書きプロンプトを出さずに上書きする。

### 対象の markdown ファイルのルール
* 各文は、箇条書き (`*`) で始める。この `*` は `main` や `comment` 処理での変換時に削除される。
* 各文の日本語に対応する英語は HTML のコメント `<!-- TEXT -->` として記述する (英語を本文とする場合は、コメントに日本語を記述する)。
* 段落に対する説明は第二見出し (`####` で始まる行) とする。この説明は `main` や `comment` 処理での変換時に削除される。
* 上記以外のルールの文は、そのまま出力される。
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
### Ver. 1.1 (2022-02-21)
* 段落の説明を `####` に変更した。

### Ver. 1.0 (2022-02-21)
* 公開した。
