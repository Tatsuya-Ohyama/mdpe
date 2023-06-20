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
	: * `import`: 通常テキストファイルから変換する。
* `INPUT.md`
	: 入力 markdown ファイル
* `OUTPUT.md`
	: 出力 markdown ファイル (Default: `-i` と同じファイル)
* `-a`, `--append`
	: `import` モード時に、既存のファイルに追記する。
* `-O`
	: 上書きプロンプトを出さずに上書きする。


### 対象の markdown ファイルのルール
* 各文は、箇条書き (リスト) (`*`) で始める。この `*` は `main` や `comment` 処理での変換時に削除される。
* 各文の日本語に対応する英語は HTML のコメント `<!-- TEXT -->` として記述する (英語を本文とする場合は、コメントに日本語を記述する)。
* 同じ段落の文にする場合は、一段下げたリストとして記述する。
* 新たな段落は、レベル 1 のリストとして記述する。
* 上記ルール以外の行は、そのまま出力される。
* 例:
	* 編集ファイル

		```txt
		## Pangram
		* 素早い茶色の狐はのろまな犬を飛び越えた。 <!-- The quick brown fox jumped over the lazy dogs -->
			* 赤色の狐もその犬を飛び越えた。 <!-- The red fox also jumped over the dog. -->
			* しかし、白色の狐はその犬を飛び越えられなかった。 <!-- However, the white fox could not jumps over the dog. -->
		* これらの文章はパングラムと、その派生である。 <!-- These texts are pangrams and derivatives. -->

		## Other pangram
		* カミソリ跳びをするカエルが、6人のピチピチの体操選手をレベルアップさせる方法！ <!-- How razorback-jumping frogs can level six piqued gymnasts! -->
			* 仕事を依頼した賢いイカに、居心地のいいルンゼがペンを渡す。 <!-- Cozy lummox gives smart squid who asks for job pen. -->
		```

	* `comment` での出力ファイル

		```txt
		## Pangram

		The quick brown fox jumped over the lazy dogs The red fox also jumped over the dog. However, the white fox could not jumps over the dog.

		These texts are pangrams and derivatives.

		## Other pangram

		How razorback-jumping frogs can level six piqued gymnasts! Cozy lummox gives smart squid who asks for job pen.
		```


### `import` モードのテキストファイル
* `import` モードは、通常テキストファイルから、上記の markdown に変換する。
* 1 行が 1 段落に相当する。
* ピリオド (.) および句点 (。) で文が区切られる。
* ピリオドの場合、厳密には ". " (スペース) か、行末尾の "." を区切り文字として認識する。



## 動作要件
* Python3


## License
The MIT License (MIT)

Copyright (c) 2022 Tatsuya Ohyama


## Authors
* Tatsuya Ohyama


## ChangeLog
### Ver. 3.0 (2023-06-20)
* `import` モードを追加した。
* 正式に第四見出しでの段落認識を廃止した。

### Ver. 2.1 (2023-05-19)
* YAML の前後に空行を入れるようにした。

### Ver. 2.0 (2023-05-19)
* 複数の YAML を出力するバグを修正した。
* 文章ファイルをクラスで扱うようにした。

### Ver. 1.4 (2023-01-06)
* コメントを含まない行を変換できないバグを修正した。

### Ver. 1.3 (2022-03-01)
* プログラム名を `papereditor.py` から `mdpe.py` に変更し、リポジトリに公開した。

### Ver. 1.2 (2022-03-01)
* `swap` モード時にネストされたリストのインデントが消えるバグを修正した。

### Ver. 1.1 (2022-02-21)
* 段落の説明を `####` に変更した。

### Ver. 1.0 (2022-02-21)
* 公開した。
