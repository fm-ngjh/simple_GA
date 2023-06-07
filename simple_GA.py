import cv2
import numpy as np
import numpy.random as nr
from copy import deepcopy
import matplotlib.pyplot as plt
import random
import copy
import os

# 画像を個体として，各画像はnbShapes個の図形が描画されていて，各図形は9個の実数値から生成されている
# よって1個体につきnbShapes * 9個の遺伝子情報が存在する

class genetic_algorythm:
    def __init__(self):
        # 画像サイズ
        self.width = 50
        self.height = 50

        # 1世代の個体数
        self.population = 50

        # 図形の数
        self.nbShapes = 100

        # 突然変異する割合
        self.mutationRate = 0.01
              
        # 世代
        self.generation = 1
        
        # スコアグラフ
        self.bestScore = []
    
    def show(self, img):
        # 画像をプロット，保存する
        plt.imshow(img, vmin = 0, vmax = 255)
        plt.title("generation = " + str(self.generation) + "  score = " + str(self.scores[0][1]))
        plt.savefig(self.path + 'simple_GA_result/' + str(self.generation) + '.jpg')
        #plt.pause(0.1)
    
    def read_img(self, path):
        # 画像読み込みとリサイズ
        self.path = path
        self.imgPath = path + 'target.png'
        self.targetImg = cv2.imread(self.imgPath)
        self.targetImg = cv2.cvtColor(self.targetImg, cv2.COLOR_BGR2RGB)
        self.targetImg = cv2.resize(self.targetImg, (self.width, self.height))
        plt.imshow(self.targetImg, vmin = 0, vmax = 255)
        plt.title("target")
        plt.savefig(self.path + 'simple_GA_result/target.jpg')
        
    def init_genoms_and_imgs(self):
        # 画像の初期化
        self.imgs = [np.ones((self.width, self.height, 3), np.uint8) * 128] * self.population
        
        # 遺伝子の初期化
        self.genoms = [[] for i in range(self.population)]
        for i in range(self.population):
            for j in range(self.nbShapes):
                self.genoms[i].append(nr.rand(9))
                self.imgs[i] = self.generate_img(self.imgs[i], self.genoms[i][j])
    
    def generate_img(self, img, genom):
        # 要素の分解
        center = [genom[0] * self.width, genom[1] * self.height]
        
        h = genom[2] * self.height / 3
        w = genom[3] * self.width / 3
        
        B = genom[4] * 255
        G = genom[5] * 255
        R = genom[6] * 255
        
        alpha = genom[7]
        
        shapeType = genom[8] + 0.5 
        
        # 図形の描画
        img_buf = img.copy()
        
        # 長方形描画
        if int(shapeType) == 0: 
            pt1 = [center[0] + w/2, center[1] + h/2]
            pt2 = [center[0] - w/2, center[1] - h/2]
            cv2.rectangle(img_buf, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (int(B), int(G), int(R)), thickness=-1, lineType=cv2.LINE_AA)
        
        # 楕円描画
        else:  
            cv2.ellipse(img_buf, ((int(center[0]), int(center[1])), (int(h), int(w)), 0), (int(B), int(G), int(R)), thickness=-1, lineType=cv2.LINE_AA)

        # 図形を書き加えた画像を作成して返す
        mat_img = cv2.addWeighted(img_buf, alpha, img, 1-alpha, 0)        
        return mat_img
        
    def evaluate_imgs(self):
        # 目的画像と比較してエラーを計算
        self.scores = []

        for i in range(self.population):
            error = 0
            for x in range(self.width):
                for y in range(self.height):
                    # 画素値の取得
                    targetImgPixel = self.targetImg[x, y]                    
                    imgPixel = self.imgs[i][x, y]
                    
                    # BGRのエラーを計算
                    error = error + abs(int(targetImgPixel[0]) - int(imgPixel[0]))
                    error = error + abs(int(targetImgPixel[1]) - int(imgPixel[1]))
                    error = error + abs(int(targetImgPixel[2]) - int(imgPixel[2]))

            # scoreは0から1で1が完全一致(1 - error率)
            score = 1 - float(error / (255 * 3 * self.width * self.height))
            self.scores.append([i, score])
        
        # scoreで降順にソート
        self.scores = sorted(self.scores, reverse=True, key=lambda x : x[1])
        print("generation =", self.generation, "best score =", self.scores[0][1])
        self.bestScore.append(self.scores[0][1])

        # 一定間隔で画像をプロットおよびフォルダへの保存をする
        if(self.generation % 20 == 0 or self.generation == 1):
            self.show(self.imgs[self.scores[0][0]])
        
    def mating(self):
        newGenoms_cand = [] # 次世代に残す個体の候補を選択
        newGenoms = []  # 上の配列から交配と突然変異をして次世代に残す個体を決定
        
        # エリート選択
        newGenoms_cand.append(copy.deepcopy(self.genoms[self.scores[0][0]]))
        newGenoms.append(copy.deepcopy(self.genoms[self.scores[0][0]]))


        # トーナメント方式
        for i in range(self.population - 1):
            # 個体群の中からランダムに2体選ぶ
            a = random.randrange(0, self.population)
            b = random.randrange(0, self.population)
            while(a == b):
                b = random.randrange(0, self.population)
            
            # scoreを比較して高い方を選出
            if(self.scores[a][1] > self.scores[b][1]):
                winner = self.scores[a][0]
            else:
                winner = self.scores[b][0]

            newGenoms_cand.append(copy.deepcopy(self.genoms[winner]))
        
        # 交叉と突然変異 全体の70%を交配させる
        while(len(newGenoms_cand) > self.population * 0.3):
            # 交配させる2個体の選出
            x = random.randrange(len(newGenoms_cand))
            parent_x = copy.deepcopy(newGenoms_cand.pop(x))
            y = random.randrange(len(newGenoms_cand))
            while(x == y):
                y = random.randrange(len(newGenoms_cand))
            parent_y = copy.deepcopy(newGenoms_cand.pop(y))
            
            # 遺伝子情報の数だけ繰り返す(1個体(画像)につきpopulationの数だけ図形があり，各図形が9個の遺伝子情報を持つ)
            child_x = []
            child_y = []
            for i in range(self.nbShapes):
                genom_x = []
                genom_y = []
                for j in range(9):                    
                    # 一様交叉
                    rand = random.randint(0, 1)
                    if(rand == 0):
                        genom_x.append(copy.deepcopy(parent_x[i][j]))
                        genom_y.append(copy.deepcopy(parent_y[i][j]))
                    else:
                        genom_x.append(copy.deepcopy(parent_y[i][j]))
                        genom_y.append(copy.deepcopy(parent_x[i][j]))
                    
                    # 突然変異
                    rand = nr.rand()
                    if(rand < self.mutationRate):
                        genom_x[j] = nr.rand()                   
                    rand = nr.rand()
                    if(rand < self.mutationRate):
                        genom_y[j] = nr.rand()
                child_x.append(copy.deepcopy(genom_x))
                child_y.append(copy.deepcopy(genom_y))
            newGenoms.append(copy.deepcopy(child_x))
            newGenoms.append(copy.deepcopy(child_y))
            
        # 突然変異
        for i in range(len(newGenoms_cand)):
            for j in range(self.nbShapes):
                for k in range(9):
                    rand = nr.rand()
                    if(rand < self.mutationRate):
                        newGenoms_cand[i][j][k] = nr.rand() 
                        
        # 世代交代
        for i in range(len(newGenoms_cand) - 1):
            newGenoms.append(copy.deepcopy(newGenoms_cand[i]))
        self.genoms = newGenoms
        
    def update_generarion(self):         
        while(1):
            # 交配
            self.mating()
            
            # 世代を進める
            self.generation = self.generation + 1
            
            # 次世代の画像群を生成
            self.imgs = [np.ones((self.width, self.height, 3), np.uint8) * 128] * self.population  
            for i in range(self.population):
                for j in range(self.nbShapes):
                    self.imgs[i] = self.generate_img(self.imgs[i], self.genoms[i][j])
            
            # 画像の評価        
            self.evaluate_imgs()
            
            # フォルダへの画像ファイルの保存
            plt.close()
            plt.plot(range(len(self.bestScore)), self.bestScore)
            plt.xlabel('Generation')
            plt.ylabel('Score')
            plt.savefig(self.path + 'simple_GA_result/score.jpg')
            
            plt.close()
            plt.imshow(self.imgs[self.scores[0][0]], vmin = 0, vmax = 255)
            plt.title("generation = " + str(self.generation) + "  score = " + str(self.scores[0][1]))
            plt.savefig(self.path + 'simple_GA_result/last.jpg')
            
            # 終了条件 途中で強制終了しても途中の画像，最終的な画像，スコアグラフは保存されている
            if(self.scores[0][1] > 0.98):    
                break                

    def main(self, imgPath):
        # 画像の読み込み
        self.read_img(imgPath)
        
        # 遺伝子と画像の初期化
        self.init_genoms_and_imgs()
        
        # 初期画像の評価
        self.evaluate_imgs()
        
        # 世代を更新していくループ
        self.update_generarion()        
 
ga = genetic_algorythm()

# resouce下に新しいフォルダを作成し，中にtarget.pngを保存しておく必要がある
path = './resource/TAT_logo/'
os.mkdir(path + "simple_GA_result")
ga.main(path)
