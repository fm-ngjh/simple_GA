# simple_GA
個人的に興味があったので作ってみたプログラムです．遺伝的アルゴリズムを用いてランダムな色，形をした図形群から構成された画像を目的の画像に近づけていきます．各ピクセルのRGB値を比較した差分をエラーと定義し，これを用いて「0から1で表現され1に近づくほど元画像と一致する」という定義のスコアを作成し評価値としました．

# 実行例1
白い背景に黄色い正方形が写ったシンプルな画像を目的画像に設定しました．
<p align="center">  
  <img src="https://github.com/fm-ngjh/simple_GA/blob/main/resource/yellow_square/target.png" width="300" height="300">
</p>

ランダムに生成した画像から出発し，3000世代ほど進化させることで目的画像に近い状態になりました．

<table>
  <tr>
    <td><img src="https://github.com/fm-ngjh/simple_GA/blob/main/resource/yellow_square/simple_GA_result_ex/1.jpg"></td>
    <td><img src="https://github.com/fm-ngjh/simple_GA/blob/main/resource/yellow_square/simple_GA_result_ex/3000.jpg"></td>
    <td><img src="https://github.com/fm-ngjh/simple_GA/blob/main/resource/yellow_square/simple_GA_result_ex/score.jpg"></td>
  </tr>
</table>

<img src=https://github.com/fm-ngjh/simple_GA/blob/main/resource/yellow_square/simple_GA_result_ex/result.gif>

# 実行例2
所属している大学のロゴを目的画像に設定しました．
<p align="center">  
  <img src="https://github.com/fm-ngjh/simple_GA/blob/main/resource/TAT_logo/target.png" width="300" height="300">
</p>

10000世代ほど進化させた結果，惜しい感じにはなったものの文字の形を再現しきることができませんでした．画像のピクセル数や図形の数などを変更することによってより目的画像に近づくかもしれませんが，計算負荷を考えるとより効率のいいアルゴリズムを採用する必要があると感じました．

<table>
  <tr>
    <td><img src="https://github.com/fm-ngjh/simple_GA/blob/main/resource/TAT_logo/simple_GA_result_ex/1.jpg"></td>
    <td><img src="https://github.com/fm-ngjh/simple_GA/blob/main/resource/TAT_logo/simple_GA_result_ex/10000.jpg"></td>
    <td><img src="https://github.com/fm-ngjh/simple_GA/blob/main/resource/TAT_logo/simple_GA_result_ex/score.jpg"></td>
  </tr>
</table>

<img src="https://github.com/fm-ngjh/simple_GA/blob/main/resource/TAT_logo/simple_GA_result_ex/result.gif">
