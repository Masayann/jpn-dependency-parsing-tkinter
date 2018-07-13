#!/usr/bin/env python
# coding : utf-8

import sys
import CaboCha
import pydot
import tkinter as tk
import numpy as np
from PIL import Image

parser = CaboCha.Parser()

# 係り受け解析した後，有向グラフを出力
def process(string):
    value = string.widget.get()
    tree =  parser.parse(value)
    cabocha_data = tree.toString(CaboCha.FORMAT_LATTICE)

    modify = [] # 1節文の文字列と修飾先の数字を格納
    modify_num = -1
    section = ""

    for line in cabocha_data.splitlines():
        if line == "EOS":
            modify.append([section ,modify_num])
        elif str(line[0]) == "*":
            if section != "":
                modify.append([section ,modify_num])
                section = ""
            modify_num = int(line.split(" ")[2].replace('D', ''))
        else:
            section = section + line.split("\t")[0]

    edges = []
    for line in modify:
        if line[1] == -1: break
        edges.append([line[0], modify[line[1]][0]])

    n = pydot.Node('node')
    n.fontname = "arialuni.ttf"
    n.fontsize = 9
    n.fontcolor = "blue"

    g = pydot.graph_from_edges(edges, directed=True)
    g.add_node(n)
    imgfname = 'modify-relation.png'
    g.write_png(imgfname, prog='dot')

    img = Image.open(imgfname)
    width, height = img.size
    img2 = img.resize((width*3, height*3))

    img2.show()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('係り受け解析器')
    root.geometry("400x100")
    
    frame = tk.Frame(root)

    # ラベル1
    label1 = tk.Label(text = '解析したい文を入力してください')
    label1.pack()

    # ラベル2
    label2 = tk.Label(text = 'Enterキーで確定')
    label2.pack()

    # エントリー
    sentence = tk.Entry(width=50)
    sentence.bind('<Return>', process)
    sentence.pack()

    root.mainloop()