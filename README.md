# moving_files_automator

メタデータとしてダウンロード元URL情報を持っているファイルを自動でフォルダに移動させる自動化プログラムです．PythonとTkinterの環境があれば動かせます．作動させるには以下の情報が必要になります．

1. 移動させたいファイルが格納されているフォルダのパス
2. ダウンロード元URL(ここで登録したURLをメタデータとして持つファイルが移動される)
3. 2のそれぞれのURLに対して，移動先のフォルダのパス

## 各ファイルの説明
### mfa.py
動作の主体であり，このプログラムを実行することでウィンドウが現れます．ウィンドウを閉じるとプログラムは終了します．
- Cleaning：ファイルの移動を開始するボタン「Let's clean!」が現れます．
- Add link：移動先のフォルダのパスとURLを登録する際に使用します．．パスの部分はドラッグ&ドロップに対応しています．
- Remove link：Add linkで登録した情報を削除できます．
- Add source：移動したいファイルが格納されているフォルダのパスを登録する際に使用します．こちらもドラッグ&ドロップに対応しています．
- Remove source：Add sourceで登録した情報を削除できます．

### cleaning_directory.txt
移動したいファイルが格納されているフォルダのパスが書き込まれます．パスの追加は'Add source'メニューから行ってください．

### target_directory.txt
移動先のフォルダのパスが書き込まれます．urls.txtとは行で対応しています．登録は'Add link'メニューから行ってください．

### urls.txt
検索対象となるURL情報が書き込まれます．target_directory.txtとは行で対応しています．登録は'Add link'メニューから行ってください．

### setup.py
py2appでアプリ化する場合に使用します．