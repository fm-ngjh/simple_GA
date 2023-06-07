# simple_GA
個人的に興味があったので作ってみたプログラムです．遺伝的アルゴリズムを用いてランダムな色，形をした図形群から構成された画像を目的の画像に近づけていきます．各ピクセルのRGB値を比較した差分をエラーと定義し，これを用いて「0から1で表現され1に近づくほど元画像と一致する」という定義のスコアを作成し評価値としました．

# 実行例1
白い背景に黄色い正方形が写ったシンプルな画像を目的画像に設定しました．
![target](https://github.com/fm-ngjh/simple_GA/assets/135797163/3c6f240b-0ef9-4d3c-a5fc-20606d8144f2)

ランダムに生成した以下の画像から出発し，3000世代ほど進化させることで目的画像に近い状態になりました．
![1](https://github.com/fm-ngjh/simple_GA/assets/135797163/2bd9a5b8-08b1-4b29-84b3-a20ebd7273cf)

![score](https://github.com/fm-ngjh/simple_GA/assets/135797163/d90fa783-87f7-4989-a0df-7d4b90de34b1)

スコアグラフ

![3000](https://github.com/fm-ngjh/simple_GA/assets/135797163/391aa79d-ce74-4716-87cb-f6849f0563ab)

最終的な結果

![result](https://github.com/fm-ngjh/simple_GA/assets/135797163/7dbae0cc-1e36-4366-87b7-ed69ddc48395)
