Title: Curiosidades de C++: usar la misma variable en dos bucles anidados
Date: 2019-11-09 13:14
Category: Curiosidades de C++


# Pregunta

¿Es correcto el siguiente código para imprimir un triángulo invertido?

```

for(int i=0; i<5; ++i) {
    const auto limit = 5 - i;
    for(int i=0; i<limit; ++i) {
        std::cout << '-';
    }
 std::cout << std::endl;
}

```

# Respuesta corta

[Sí](https://coliru.stacked-crooked.com/a/c4049493567cbfa8)


# Respuesta larga

Es posible crear dos variables con el mismo nombre si están en un *scope* diferente, aunque sean *scopes* anidados.

Por otro lado, cada bucle *for* crea un nuevo *scope* para su variable interna.

Por lo tanto, en el ejemplo, tenemos dos scopes independientes: uno para cada *for* y en cada uno hay una variable ```i``` declarada.
