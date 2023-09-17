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

Este conjunto de ecuaciones puede tener muchas formas, pero generalmente se usa la forma CNF 
([Conjuntive Normal Form](https://en.wikipedia.org/wiki/Conjunctive_normal_form)):

- Se compone de un conjunto de ecuaciones que deben evaluar a *true*.
- Cada ecuación está compuesta por una sucesión de variables (que pueden estar negadas) enlazadas por la operación OR.

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
 
  (a' * b' * c')' = 1
  (a + b)' = 1
  
  
# 1. SAT Solver en C++

Existen [múltiples librerías](https://stackoverflow.com/q/41057441/218774) para resolver el problema SAT en C++.

La librería más conocida probablemente sea [MiniSAT](https://github.com/niklasso/minisat).
Aunque ya no se mantiene, el código es funcional.

Otra opción es [GLUCOSE](https://www.labri.fr/perso/lsimon/research/glucose/). 
Tiene una interfaz similar a MiniSAT, pero sigue siendo mantenida y está más optimizada para ciertos casos.

En este ejemplo, vamos a usar MiniSAT porque está integrada dentro de VCPKG.


# 2. Uso de la librería MinSAT

Como ejemplo, veamos cómo resolver las ecuaciones

```
 v0 + v1' = 1
 v0' = 1
```

El primer paso es crear un objeto del tipo ```Minisat::Solver```. 

```
Minisat::Solver solver;
```

Este es el objeto principal de la librería y se encarga de gestionar las variables, las ecuaciones y de la resolución del problema.

El segundo paso es crear las variables. Para esto, se utiliza la función ```AddVar``` del objeto ```Minisat::Solver``` que acabamos de crear.
Internalmente, las variables son únicamente un índice, de cero al número de variables.
Por lo tanto, aunque esta función devuelve un objeto de tipo ```Var```, no es estrictamente obligatorio almacenarlo porque es sencillo referenciar una variable usando su índice con el método ```mkLit```.

En nuestro caso, vamos a crear dos variables:
```
  solver.newVar();
  solver.newVar();
}
```

El tercer paso es crear las ecuaciones. 
Como deben estar en formato CNF, una ecuación es únicamente un vector de variables, algunas de las cuales podrían estar negadas.
Por ello, podemos almacenar una única ecuación mediante un vector: ```Minisat::vec<Minisat::Lit>```.
Se utiliza el operador ```~``` para indicar que la variable está negada.

Para añadir la ecuación a nuestro objeto, usamos el método ```addClause```, al que podemos pasar uno, dos, tres literales o un vector.

En el ejemplo, queremos crear dos ecuaciones:

```
Vector equation_0;
equation_0.push(Minisat::mkLit(0));
equation_0.push(~Minisat::mkLit(1));
solver.addClause(equation_0);

Vector equation_1;
equation_1.push(~Minisat::mkLit(0));
solver.addClause(equation_1);
```

El paso final es llamar a la función ```solve``` para calcular la solución. Esta función devuelve un ```bool``` indicando si se ha podido encontrar una solución.
En caso positivo, se puede preguntar el valor de la solución encontrada usando el método ```modelValue```.



# 3. Planteamiento general del problema de las N reinas

El problema de las N reinas es una generalización del problema de las [8 reinas](https://en.wikipedia.org/wiki/Eight_queens_puzzle).
El objetivo es colocar N reinas de ajedrez dentro de un tablero de tamaño NxN de manera que ninguna de ellas pueda atacarse.

Como recordatorio, las reinas en ajedrez pueden moverse cualquier cantidad de casillas en horizontal, vertical y diagonal.

Se sabe que este problema tiene múltiples soluciones para N > 3.


# 4. Planteamiento del problema de las N reinas para un SAT Solver

## Variables

Como en cualquier problema de este tipo, el primer paso es decidir qué variables vamos a usar.
Puesto que vamos a usar variables booleanas (true o false), sería complicado usarlas para almacenar la posición de cada reina, ya que es un número natural.

Por lo tanto, lo más sencillo es usar las variables para representar las casillas del tablero, donde:

- True: hay una reina en esta casilla.
- False: la casilla está vacía.

De esta manera, necesitaremos NxN variables booleanas para definir un tablero. 

La numeración de las casillas se hará partiendo de la esquina superior izquierda y de forma vertical. 
Es decir, para un tablero 4x4:

```
1 5 9 D
2 6 A E
3 7 B F
4 8 C G
```


## Ecuaciones

Todas las ecuaciones son del tipo: "en este conjunto de casillas debe haber una y sólo una reina".
Esto se consigue con las siguientes ecuaciones:

**Tiene que haber al menos una variable a *true* **

Esto se consigue con una sóla ecuación que incluye todas las variables.
Por ejemplo, para la primera fila de un tablero 4x4:

```
a1 + a2 + a3 + a4 = 1
```

**No puede haber dos variables a *true* **

Esto se consigue añadiendo una ecuación para todas las parejas de variables del grupo, del tipo:

```
ai' + aj' = 1
```

Por ejemplo, en el caso de la primera fia del tablero 4x4, tendríamos las siguientes ecuaciones:

```
a1' + a2' = 1
a1' + a3' = 1
a1' + a4' = 1
a2' + a3' = 1
a2' + a4' = 1
a3' + a4' = 1
```



Primero debemos localizar cuáles son los conjuntos de casillas donde sólo debe haber una línea:

- Filas: en cada fila del tablero sólo puede haber un *true*. 
  Hay una fila de N elementos cada N casillas.
- Columna: en cada columna del tablero sólo puede haber un *true*. 
  Hay una columna de N elementos desde cada una de las casillas de 1 a N.
- Diagonales: en cada diagonal del tablero sólo puede haber un *true*.
  Hay dos tipos de diagonales. las que van de arriba-izquierda a abajo-derecha y las que van de arriba-derecha a abajo-izquierda.
  
Después, para cada conjunto, añadimos las siguientes ecuaciones:



## Implementación de las ecuaciones en MiniSAT





