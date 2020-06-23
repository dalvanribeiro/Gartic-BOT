# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:14:46 2020

@author: Dalvan
"""

sinonimos = ["casa","boteco", "carretilha", "biscoito", "cassetete", "morango"]
dicas={"num" : 10, 1 : "c", 2 : "a"}
num= int(dicas["num"])
del dicas["num"]

filtrada = []
for item in sinonimos:
    if len(item) == num :
        filtrada.append(item)

for index, item in enumerate(filtrada):
    for dica in dicas:
        if item[dica-1] != dicas[dica]:
            try:
                filtrada.pop(index)
            except IndexError:
                pass

