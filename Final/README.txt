Requirements:

Python 2.7.X
Numpy

################

Inicializa��o da simula��o:
python tester.py <nome do labirinto> <n�mero do modo explora��o>

Por exemplo:
python tester.py test_maze_01.txt 1

Para a visualiza��o dos caminho tomado ap�s a execu��o da simula��o, utiliza-se:
python showresult.py <nome do labirinto>

Os labirintos dispon�veis s�o:
test_maze_01.txt
test_maze_02.txt
test_maze_03.txt
test_maze_04.txt

Modos de explora��o dispon�veis:
[1] Aleat�rio
[2] Comum
[3] Estendido

No caso do modo aleat�rio, phi pode ser alterado na se��o de inicializac�o do rob�,
diretamente em robot.py.
