Title: 8 cosas que todo programador de C++ debería saber sobre el comportamiento indefinido
Date: 2023-07-04
Category: Iniciación C++
Tags: C++, UB


# 0. ¿Qué  tipos de comportamiento hay en C++?

El estándard C++ define cuatro tipos de comportamiento:

 - Comportamiento definido: la ejecución del programa es completamente predecible.
 - Comportamiento definido por la implementación (implementation-defined behavior): la ejecución es predecible, pero depende del compilador o del entorno dentro de ciertos márgenes y estas variaciones deben estar documentadas.  Por ejemplo, el valor de ```sizeof(int)```.
 - Comportamiento no especificado (unspecified behavior): la ejecución no es predecible pero está dentro de ciertas opciones. Por ejemplo, el orden de evaluación de los argumentos de una función.
 - Comportamiento sin definir (undefined behavior): la ejecución no es predecible y puede suceder cualquier cosa.

Por otro lado, dentro de esos comportamientos, el compilador puede encontrar tres tipos de construcciones:

 - Código mal formado (ill-formed): el código no se corresponde con C++ válido. El programa no es válido y el compilador genera un mensaje.
 - Código mal formado sin diagnóstico (ill-formed no diagnostic required): el código contiene un error que no se ha podido detectar (por ejemplo, violación de ODR). La resultado de la ejecución es indefinido.
 - Código bien formado (well-formed): el código se adhiere a las reglas de C++ y su ejecución se puede determinar dentro del estándar.

Si juntamos la primera con la segunda lista, vemos que existe un tipo de comportamiento en el que la ejecución no es predecible y no se ha podido detectar.
Es el *temido* comportamiento indefinido.


#1 ¿Hasta qué punto es indefinido el comportamiento indefinido?

El estándar da completa y absoluta libertad al compilador para decidir qué hacer en caso de comportamiento indefinido.
Posibles opciones son:

- Comportarse de forma esperada.
- Hacer fallar la aplicación.
- Hacer fallar la aplicación un tiempo después.
- Hacer fallar la aplicaicón un tiempo antes.
- [Hacer que salgan demonios de tu nariz](http://catb.org/jargon/html/N/nasal-demons.html).

Hay que tener en cuenta que cuando un programa pasa por comportamiento indefinido todo el programa es indefinido.
Es decir, la aplicación podría fallar antes de pasar por la línea donde ocurre.

Por ejemplo, queremos saber qué hace el siguiente código:

```
int call_fa(const A *a) {
  return a->fa();
}
```


A primera vista, parece fácil.
Llama a la función ```fa()``` del objeto ```a```.
Sin embargo, ¿qué pasa si el puntero ```a``` es nulo?
En ese caso, el comportamiento es indefinido y el compilador no tiene que rendir cuentas del comportamiento.

Lo más probable es que la aplicación falle porque se intenta acceder a una zona de memoria inválida.
Aunque también puede pasar que el procesador no tenga la capacidad de detectar ese fallo y la función se ejecute sobre un objeto A inválido provocando corrupción de datos que harán fallar la aplicación más adelante. 
También podría ser que el optimizador mueva la llamada de la función a otro punto y el programa falle antes o después de lo que se espera.

Si seguimos pensando, se nos pueden ocurrir otros escenarios, como que ```fa()``` sea una función virtual y, al ser inválido el objeto, el punto de ejecución salte a una zona de memoria aleatoria.

Lo importante es recordar que no hay ninguna limitación a lo que puede pasar. Incluso puede que el comportamiento cada vez que compilemos.


#2 ¿Por qué existe el comportamiento indefinido?

En general, el comportamiento indefinido permite que el compilador no tenga que comprobar ciertos casos y así pueda adaptarse mejor al hardware que se está usando
de forma que genere código más optimizado para diferentes plataformas. 

Por ejemplo, en el ejemplo del punto anterior:

```
int call_fa(const A *a) {
  return a->fa();
}
```

El comportamiento indefinido le dice al compilador que no tiene que comprobar el caso en el que ```a``` es nulo porque si se da ese caso puede hacer lo que quiera.
De esta forma, se evita la comprobación y se genera código más optimizado. 

Pongamos otro ejemplo:

```
int f() {
  g();
}
```

El estándar no dice lo que tiene que pasar si una función que debe devolver un valor no devuelve nada.
Tal vez el programador sepa que g() nunca retorna porque siempre lanza una excepción o cierra la aplicación, por lo que no va a haber problemas.
Pero el compilador no lo sabe y tiene que decidir qué hacer. Aquí se encuentra un problema:

 - Si el estándar definiese el comportamiento, le obligaría a añadir código que nunca se va a usar.
 - Si no se define, podría pasar cualquier cosa.

Así pues, el estándard no indica qué debe pasar y el desarrollador del compilador puede hacer lo que más le convenga para su plataforma.


#3 ¿Por qué es tan peligroso el comportamiento indefinido?

El comportamiento indefinido es una de las caracteristicas más peligrosas C++.

Los motivos son varios, aunque los dos principales son:

 - Al dar libertad total al compilador, un programa indefinido podría listar todas las contraseñas del sistema.
   Obviamente, el error no va a ser tan directo, pero nadie te asegura que no lo haga.
   De hecho, muchos errores de seguridad se basan en el comportamiento indefinido de C o C++.
   
 - Cuando hay un comportamiento indefinido, es muy difícil depurar el error.
   Hay que entender que, si se da un comportamiento indefinido, todo el programa es indefinido.
   Por lo que el error puede darse en la línea problemática o podría comportarse según lo esperado durante un tiempo y fallar más adelante.
   Por ejemplo, una vez tuvimos un programa que violaba la ODR (más sencillo de lo que parece al usar templates) y
   la aplicación fallaba nada más arrancar a pesar de que no se había llamado todavía a la función problemática.

De hecho, el comportamiento indefinido es una de las mayores quejas de los programadores de C++ y, a la vez, 
lo que le da a C++ la capacidad de generar código optimizado en muchas arquitecturas.


#4. ¿El compilador puede avisar del comportamiento indefinido?

El compilador no tiene obligación de avisar del comportamiento indefinido en todos los casos.

Algunos compiladores avisan de los casos sencilos de detectar como:

```
int f() {}
```

Es comportamiento indefinido porque claramente la función no devuelve nada pese a que está declarada para devolver un entero.

Sin embargo, algunos casos son muy complicados de detectar o sólo pueden detectarse en tiempo de ejecución, como por ejemplo:

```
void f(T *object)
{
  object->f();
}
```

Si object es nulo, el programa es indefinido.

En estos casos, para detectarlo, habría que añadir instrucciones que comprobasen que la variable no es nula. 
Si el programador ya sabe que nunca lo será, se está penalizando la ejecución.


#5 Ejemplos de comportamiento indefinido

Los casos de comportamiento indefinido con los que más me he encontrado son:

## Usar un objeto nulo

```
void f(const A* a)
{
  a->fa();
}
```

En este caso, es comportamiento indefinido si ```a``` es nulo. 

Existen varias formas de defenderse de este comportamiento. 
La más directa es comprobar el valor del puntero antes de usarlo.
Si creemos que nunca debería ser nulo, podemos poner un assert al principio de la función para que también muestre un error en debug:

```
void f(const A* a)
{
  assert(a);
  if(a) { a->fa(); }
}
```

## Acceder a índices incorrectos de un array

```
double f(int index)
{
  const double a[2] = {1.0, 2.0};
  return a[index];
}
```

Esta función es indefinida cuando la variable ```index``` es mayor o igual que dos porque accedería a una posición incorrecta del array.

Una posible solución es comprobar el valor de la variable index y usar un objeto de tipo std::array en vez de un array ya que, generalmente, 
comprueban el índice en debug:

```
double f(int index)
{
  const std::array<double, 2> a = {1.0, 2.0};
  if(index >= 0 && index < 2) { return a[index]; }
  return 0.0;
}
```

Dependiendo del programa, sería conveniente discutir qué debe ocurrir si el valor de index es incorrecto.
Por ejemplo, podríamos devolver un valor por defecto o lanzar una excepción.


## Acceder a memoria sin inicializar

```
bool f(int index)
{
  int a;
  
  return a == 3;
}
```

Acceder a memoria sin inicializar es comportamiento indefinido. 

Antiguamente, se decía que el valor de la variable sin inicializar era aleatorio.
Sin embargo, esto no es cierto, ya que el compilador puede hace lo que crea conveniente en cada caso.
Por ejemplo, la función anterior podría devolver siempre ```true``` y cumpliría el estándar.

La solución más sencilla es inicializar siempre las variables:

```
bool f(int index)
{
  int a{0};

  return a == 3;
}
```

## Desbordamiento de enteros con signo

```
bool foo(int x)
{
  return x + 1 > x;
}
```

La condición ```return x + 1 > x;``` parece inocente. 
Sin embargo, cuando x ya está en el máximo valor de un entero, se produce un desbordamiento que puede volver el número negativo.
Ahora bien, un desbordamiento de entero con signo es comportamiento indefinido por lo que lo más probable es que el compilador 
no tenga en cuenta ese caso y siempre devuelva ```true```.
Por otro lado, algún procesador podría decidir lanzar una excepción por lo que tampoco podemos confiar en este comportamiento.

Por eso, si creemos que el valor de ```x``` puede provocar un desbordamiento, habría que comprobar el valor o modificar la función.

Hay que hacer notar que esto no ocurre en los enteros sin signo, por lo que en la siguiente función:

```
bool foo(unsigned int x)
{
  return x + 1 > x;
}
```

El compilador tiene que añadir código para gestionar el desbordamiento y puede resultar más lenta que la anterior.


## Violación de la ODR

La ODR indica que un elemento puede ser definido una única vez o, en caso de hacerlo varias veces (por ejemplo si está en un archivo de cabecera),
las definiciones deben ser idénticas.

Normalmente, cuando se incumple esta regla, el linker puede detectarlo y emite un mensaje.
Sin embargo, no siempre es así.

Por ejemplo, si se tienen dos archivos:
```
// A.cpp
struct A{
  char a;
};

// B.cpp
struct A{
  int a;
};
```

Al ser ambas definiciones de la estructura ```A``` distintas, puede probocar comportamiento indefinido.

La solución es no declarar estructuras globales dentro de unidades de compilación. 
En caso de tener que hacerlo, utilizar namespaces anónimos para indicar que la declaración no debe salir fuera de la unidad de compilación.


#6. ¿Qué se puede hacer para minimizar los riesgos?

En general, hay que seguir un conjunto de buenas prácticas de C++. 
Por ejemplo:

 - Activar todos los avisos del compilador.
 - No usar punteros en bruto sino alguna de las múltiples alternativas para gestionar la memoria (std::vector, std::unique_ptr, std::shared_ptr, ...).
 - Usar std::array en vez de arrays de C. 
 - Usar conversiones de C++ (static_cast, ...) en vez de conversiones de C.
 
Además, también es importante utilizar herramientas de análisis estático como:

 - [Cppcheck](http://cppcheck.sourceforge.net/)
 - [CLang Static Analyzer](https://clang-analyzer.llvm.org/)

Hay una lista de herramientas en [Wikipedia](https://en.wikipedia.org/wiki/List_of_tools_for_static_code_analysis).

 
#7 ¿Cómo está relacionado el comportamiento indefinido con el optimizador?

El comportamiento indefinido permite al optimizador eliminar casos que no deberían darse. 

Por ejemplo, hemos visto que el comportamiento indefinido permite ignorar el desbordamiento de los enteros con signo.
También permite eliminar la comprobación de los límites de un array o si el puntero es nulo.

En algunos casos, permite optimizaciones más agresivas.
Por ejemplo, ¿qué pasa si llamamos a la función g() en el siguiente código?

```
int f(int *number)
{
  int a = *number;
  if(number != nullptr) {
    return 0;
  }
  return 2;
}
```

El optimizador puede pensar:
 
En la primera línea de la función se usa el puntero:

  - Si el puntero no es nulo, asigno la variable y me apunto que el puntero no es nulo.
  - Si el puntero es nulo puedo hacer lo que quiera porque es comportamiento indefinido, así que hago lo mismo que en el caso anterior.
  
En la segunda línea, la comprobación se ha vuelto redundante porque hemos definido que el puntero no es nulo, así que se puede eliminar.
De esta manera, la función f siempre devuelve cero y quedaría:

```
int f(int *number)
{
  return 0;
}
```




# Referencias

[Difference between Undefined Behavior and Ill-formed, no diagnostic message required](https://stackoverflow.com/q/22180312/218774)
[https://en.cppreference.com/w/c/language/behavior](https://stackoverflow.com/q/2397984/218774)
[C99 List of Undefined Behavior](https://gist.github.com/Earnestly/7c903f481ff9d29a3dd1)
[CUndefined behavior](https://en.cppreference.com/w/c/language/behavior)
[A Guide to Undefined Behavior in C and C++](https://blog.regehr.org/archives/213)
[The One-Definition Rule](https://akrzemi1.wordpress.com/2016/11/28/the-one-definition-rule/)
