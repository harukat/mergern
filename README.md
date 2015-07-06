mergern.py
===============
概要：リリースノートを統合するためのスクリプト

目的：release-9.0.sgmlやrelease-9.1.sgmlには多くの同じ記述があり<BR>
　　　これのを他のリリースノートにコピーする作業には多くの時間が<BR>
　　　必要だった。コピーペースト作業は手動で行う作業である必要は<BR>
　　　無く、これを自動化する。<BR>
<BR>
動作確認環境：python 2.7.8 <BR>
<BR>
使用方法： ./merge.py 翻訳文があるsgmlファイル(原文)　翻訳対象のsgmlファイル　[翻訳対象のセクション(実質マイナーバージョン)]<BR>
<BR>
<BR>
動作仕様：<BR>
1.原文から<!--で始まる行を搜す<BR>
2.2行目に英文1行目があるのでこれをキーとするディクショナリを作る<BR>
3.1.の<!--から</para>までをリストオブジェクトとして格納し2.のvalueとする<BR>
4.翻訳対象と3.で作成したディクショナリを照合し、以降、</para>までを<BR>
　置き換える。<BR>
<BR>
サンプル：<BR>
　　　　　sample以下にファイルを配置しています。<BR>
　　　　　release-9.0.sgml　サンプル原文<BR>
          release-9.1.orid.sgml 翻訳前翻訳対象<BR>
　　　　　release-9.1.sgml      翻訳後はこのファイルのようになっていなければならない <BR>
<BR>
<BR>
          実行例1)<BR>
　　　　　%./mergern.py sample/release-9.0.sgml sample/release-9.1.orid.sgml<BR>
<BR>
          最もシンプルなケース。9.1.7をコピーする<BR>
<BR>
　　　　　実行例2)<BR>
<BR>
　　　　　%./mergern.py sample/release-9.0.sgml sample/release-9.1.orid.sgml 2<BR>
<BR>
          release-9.1.orid.sgmlにdummyデータを3行含ませている。9.1.6をコピーする。<BR>
　　　　　3件の警告が発生する<BR>
<BR>
<BR>
FAQ:<BR>
1.英文の1行目だけを比較しているようですが、1行目がたまたま同じということが<BR>
　あるのではないでしょうか。誤動作しませんか。<BR>
　<BR>
　はい、可能性はあります。2行目以降も照合し、異なる場合は警告を出します。<BR>
　警告が上がった場合は警告箇所を必ず確認ください。<BR>
<BR>
2.HTMLの解析方法が力技です。HTMLParserやBeautifuｌSoupeは利用しないのでしょうか。<BR>
<BR>
　はい。HTMLparserでは外部参照の自動変換の問題や、バージョンごとに動作が若干<BR>
　異なる可能性がありました。また、BeautifulSoupeは別途インストールの手間が必要です。<BR>
　PostgreSQLのマニュアルは厳格に構造化されていたため、外部のパーサーを使わなくても<BR>
　十分解析が可能と判断しました。<BR>

