Title: Resolver el Puzzle-A-Day para niños
Date: 2023-25-08
Category: Resolución de problemas en C++
Status: draft


# 0. El puzzle

Hace un tiempo, un compañero de trabajo me habló de un puzzle para niños que resultaba difícil de resolver. 
Consta de un tablero y 8 piezas de diferentes formas. 
Estas pizas pueden encajar sobre el tablero de manera que quedan dos huecos libres.
El objetivo es colocar todas las piezas sobre el tablero de manera que los huecos libres estén sobre el día y el mes del año.
Su nombre es Puzzle-A-Day y se puede podía jugar una versión online [aquí](https://mathigon.org/polypad/A62G5zIdDPthg).

# 1. Resolución

Puesto que sólo hay 8 piezas, se puede plantear usar un algoritmo de backtracking.
Vamos a calcular unos números generales jugando un poco con el emulador:

Podemos 
Jugando 

De forma general, el tablero está dentro de un cuadrado de 7x7 casillas, las pizas tienen un tamaño de 5 o 6 casillas y cada pieza puede colocarse de 8 formas distintas (cuatro giros y un espejo).
Todas las piezas ocupan al menos un rectángulo de 2x3 casillas, por lo que no se pueden colocar en las esquinas.
De esta forma, podemos estimar que se podrán colocar en máximo de 200 posiciones ((6x5-6)x8).

Cuando colocamos una pieza, queda menos espacio para las demás por lo que el área completa de búsqueda sería de 5.943.246.655.500.000.000:


# 2. EMScripten

Para instalar EMScripten:

git clone https://github.com/emscripten-core/emsdk
cd emsdk
emsdk install latest

Después, hay que abrir una ventana de comandos y teclear:

emsdk activate latest
emcc Solver\Solver.cpp PuzzleADaySolver\main.cpp -std=c++17 -O2 -o main.html -sSINGLE_FILE -sEXPORTED_FUNCTIONS=_solveAndShow,_main -sEXPORTED_RUNTIME_METHODS=ccall,cwrap --shell-file=EMS\base.html -sUSE_SDL=2
