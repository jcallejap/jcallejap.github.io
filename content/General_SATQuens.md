Title: Usar SAT Solver para resolver el problema de las N reinas.
Date: 2023-07-08
Category: Resolución de problemas en C++
Status: draft


# 0. Qué es un SAT Solver

Un [SAT Solver](https://en.wikipedia.org/wiki/SAT_solver) es un programa de ordenador cuyo objetivo es resolver el 
[Problema de satisfacibilidad booleana](https://en.wikipedia.org/wiki/SAT_solver). 

De forma informal, se podría definir como:

Dado un conjunto de variables booleanas *(true/false)* y un conjunto de ecuaciones booleanas sobre esas variables, 
comprobar si el sistema de ecuaciones tiene alguna solución.

Este conjunto de ecuaciones puede tener muchas formas, pero generalmente se usa la forma CNF ([Conjuntive Normal Form](https://en.wikipedia.org/wiki/Conjunctive_normal_form)):

- Se compone de un conjunto de ecuaciones que deben evaluar a *true*.
- Cada ecuación está compuesta por una sucesión de variables (que pueden estar negadas) unidas por la operación OR.

Por ejemplo, si usamos la siguiente nomenclatura:

- Operación OR: +
- Operación AND: *
- Operación NOT: '
- True: 1
- False: 0

Las siguientes ecuaciones estarían en forma CNF:

  a + b + c = 1
  a + b' + c = 1
  
Mientras que las siguientes ecuaciones no están en forma CNF:
 
  ab + c = 1
  (a+b)' = 1
  
# 1. Uso de un SAT Solver en C++

Existen [múltiples librerías](https://stackoverflow.com/q/41057441/218774) para resolver el problema SAT en C++.

La librería más conocida probablemente sea [MiniSAT](https://github.com/niklasso/minisat).
Aunque ya no se mantiene, el código es funcional.

Otra opción es [GLUCOSE](https://www.labri.fr/perso/lsimon/research/glucose/). 
Tiene una interfaz similar a MiniSAT, pero sigue siendo mantenida y está más optimizada para ciertos casos.

En este ejemplo, vamos a usar MiniSAT porque está integrado dentro de VCPKG.


# 2. Planteamiento general del problema de las N reinas

El problema de las N reinas es una generalización del problema de las [8 reinas](https://en.wikipedia.org/wiki/Eight_queens_puzzle).
El objetivo es colocar N reinas dentro de un tablero de ajedrez NxN de manera que ninguna de ellas pueda atacarse.

Como recordatorio, las reinas en ajedrez pueden moverse cualquier cantidad de casillas en horizontal, vertical y diagonal.

Se sabe que este problema tiene múltiples soluciones para N > 3.


# 3. Planteamiento del problema de las N reinas para un SAT Solver

## Variables

Como en cualquier problema de este tipo, el primer paso es decidir qué variables vamos a usar.
Puesto que vamos a usar variables booleanas (true o false), sería complicado usarlas para almacenar la posición de cada reina, ya que es un número natural.

Por lo tanto, lo más sencillo es usar las variables para representar las casillas del tablero, donde:

- True: hay una reina en esta casilla.
- False: la casilla está vacía.

De esta manera, necesitaremos NxN variables booleanas para definir un tablero. 

La numeración de las casillas se hará partiendo de la esquina superior izquierda y de forma horizontal. 
Es decir, para un tablero 4x4:

```
1 2 3 4
5 6 7 8
9 A B C
D E F G
```


## Ecuaciones horizontales y verticales

Las ecuaciones horizontales y verticales son las más sencillas.
Únicamente tenemos que añadir que debe haber una y sólo una reina en cada fila o columna.

Para ello, podemos usar las siguientes expresiones:

### Como mucho una variable de cada grupo es *true*

Esta condición no se puede expresar con una única ecuación, sino que es un conjunto de ecuaciones.
Para cada pareja ai, aj, decir que ambas no pueden ser *true* implica que:

```
ai' + aj' = 1
```

En el caso de la primera fia del tablero 4x4, tendríamos las siguientes ecuaciones:

```
a1' + a2' = 1
a1' + a3' = 1
a1' + a4' = 1
a2' + a3' = 1
a2' + a4' = 1
a3' + a4' = 1
```

Hay que resaltar que estas ecuaciones sólo impiden que más de una variable se active.
No obliga a que no se active ninguna variable.


### Al menos una variable es *true*

Está ecuación es la más sencilla, basta con hacer OR de todas las variables que se necesiten.
El resultado es que debe haber al menos una variable *true* entre ellas:

Por ejemplo, la primera file del tablero 4x4 usaría la siguiente ecuación para que, al menos, una de las casillas contenga una reina:

```
a1 + a2 + a3 + a4 = 1
```


## Ecuaciones diagonales







