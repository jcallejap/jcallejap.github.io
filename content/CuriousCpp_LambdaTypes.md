Title: Curiosidades de C++: todas las lambdas tienen tipos distintos
Date: 2024-1-2
Category: Curiosidades de C++
Tags: C++
Summary: ¿En qué influye que cada lambda sea un tipo distinto?

# Definición

El estándar da información sobre cómo debe ser el tipo de dato de una lambda.
De forma resumida (se han omitido algunos detalles en la traducción):

- [C++11: 5.1.2/3]: Es un tipo de clase único y sin nombre, no es un agregado ni una unión. La declaración está dentro del ámbito más pequeño que contiene la expresión lambda correspondiente.
- [C++11: 5.1.2/5]: Esta clase tiene un operador función, público, *inline* cuyos parámetros y tipo de retorno coinciden con los definidos en la lambda.
- [C++11: 5.1.2/6]: Si no se captura ningún dato, también tiene una conversión pública, no virtual y no explícita a un puntero a función con los mismos parámetros y tipo de retorno.

# Consecuencias

## Una variable de tipo lambda no se puede reasignar a una lambda distinta

Al tener todas las lambdas tipos distintos, es imposible reutilizar la variable.
Por ejemplo, el siguiente código no está permitido:

``` C++
auto a = [](int a) {return 2*a;};
auto b = [](int a) {return 2*a;};
a = b; //< Error
```

El error aparece porque el tipo de la variable ```a``` es distinto al de ```b```, por lo que no pueden asignarse.

## No se pueden usar lambdas con captura con el operador ternario

Al tener todas las lambdas tipos distintos, es imposible unificar el tipo de retorno del operador ternario.
Incluso aunque las dos lambdas sean idénticas, tienen tipos distintos.

Por ejemplo, el siguiente código da error:

``` C++
auto lambda = number == 3 ? ([var](int a) { return 2 * a; })
                          : ([var](int a) { return 2 * a; });

```

## Se pueden usar lambdas sin captura con el operacor ternario

El código anterior también sería inválido con lambdas que no capturan ningún argumento.
Sin embargo, en ese caso, las lambdas pueden convertirse a un puntero a función.
Por eso, aunque los tipos de dos lambdas sean distintos, ambos pueden convertirse a puntero y tomar ese resultado como el tipo de retorno del operator:

``` C++
int (*a)(int) = [](int a) { return 2 * a; };
int (*b)(int) = [](int a) { return 4 * a; };
auto lambda = number == 3 ? a : b;
```


# Para saber más

[What is the type of lambda when deduced with "auto" in C++11?](https://stackoverflow.com/a/7951438/218774)