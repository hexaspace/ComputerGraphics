# hexaspace computer graphics 01
# numpy calculation
#################################################
import numpy as np

#A step

M=np.arange(25)+2   #[0 1 2 ... 24] +2 = [2 3 4 ... 25]
print(M)    #터미널에 출력
print()

#B step

M=M.reshape(5,5)    #1x25행렬을 5x5행렬로 재정렬
print(M)
print()

# C step

M[1:4, 1:4]=0   #[1~3,1~3]범위를 0으로 치환
print(M)
print()

#D step

M=M@M       #행렬의 곱
print(M)
print()

#E step

v=M[0,0:5]  #1열 복사
v=v@v   #행렬 곱
print(np.sqrt(v))   #루트 값 (행렬의 곱 후 제곱근, 즉 v의 크기(스칼라값)이 산출됨)