Title: Curiosidades de C++: operador flecha
Date: 2023-06-24
Category: Curiosidades de C++
Tags: C++
Summary: ¿Qué significa la línea ```while (x --> 0)```?

La siguiente pregunta está tomada de StackOverflow, pero me ha parecido curiosa:
[What is the '-->' operator in C/C++?](https://stackoverflow.com/q/1642028/218774)


# Pregunta

¿Es correcto el siguiente código?
¿Qué imprime?

```

#include <stdio.h>
int main()
{
    int x = 10;
    while (x --> 0) // x goes to 0
    {
        printf("%d ", x);
    }
}

```

# Respuesta corta

Es correcto e imprime los números del 9 al 0 en orden descendente.
Puedes verlo [aquí](https://coliru.stacked-crooked.com/a/b1d9d6b6ade3552e)


# Respuesta larga

La parte condicional del while se puede escribir como:

```
while ((x--) > 0)
```

Por lo tanto, la expresión de la condición realiza dos operaciones:

1. Decrementar la variable x.
2. Comparar la variable x con cero.

De esta manera, la variable x va decrementándose hasta que llega a cero.

Al usarse el operador sufijo, la condición se evalua con el número original pero se imprime el resultado de restarle uno.
Por eso, aunque la condición dice 'mayor que cero', el cero también se imprime.
