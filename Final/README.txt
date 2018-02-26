Requirements:

Python 2.7.X
Numpy

################

Inicialização da simulação:
python tester.py <nome do labirinto> <número do modo exploração>

Por exemplo:
python tester.py test_maze_01.txt 1

Para a visualização dos caminho tomado após a execução da simulação, utiliza-se:
python showresult.py <nome do labirinto>

Os labirintos disponíveis são:
test_maze_01.txt
test_maze_02.txt
test_maze_03.txt
test_maze_04.txt

Modos de exploração disponíveis:
[1] Aleatório
[2] Comum
[3] Estendido

No caso do modo aleatório, phi pode ser alterado na seção de inicializacão do robô,
diretamente em robot.py.
