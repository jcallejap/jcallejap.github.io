Title: 8 cosas que todo programador de C++ debería saber sobre el optimizador
Date: 2019-11-09 13:14
Category: Iniciación C++
Status: draft


# 0. ¿Qué es el optimizador de C++?

Es una etapa de la compilación en la que se hacen modificaciones automáticas al código para que sea más eficiente.


# 1. ¿Puede cambiar lo que hace mi código?

No puede cambiar lo que hace tu código, pero sí puede cambiar cómo lo hace.

El optimizador tiene permiso para hacer cambios mientras sea imposible diferenciar las salidas del programa original frente al optimizado.

Por ejemplo, supongamos el siguiente código:

```
int main()
{
  int a = 3;
  ++a;
  std::cout << a << std::endl;
  
  return 0;  
}
```

El optimizador puede eliminar la variable a y generar un programa que únicamente imprima el número 4.


# 2. ¿En qué se fija el optimizador para decidir qué se puede o no se puede cambiar?

El optimizador puede hacer cambios en el código siempre que no cambie sus salidas.

Se considera una salida cualquier dato que salga al exterior de la aplicación. Por ejemplo:

 - Imprimir un valor por consola.
 - Mostrar un valor en un interfaz gráfico.
 - Guardar un dato en disco.
 - Enviar un dato por red.
 - Activar un pin de una tarjeta de entradas/salidas digitales.
 
De hecho, el conjunto de posibles salidas es tan amplio que se considera que cualquier función de la que no tiene el código fuente
puede generar una salida y no se puede optimizar.

Por ejemplo, el siguiente código:

```
int main()
{
  int a = 0;
  for(int i=0;i<10000;++i) {
    a += 3;
  }  
  return 0;  
}
```

La variable a no se muestra, por lo que se puede eliminar. Si se elimina esta variable, se puede eliminar el bucle.
Así pues, este programa no hace nada y el compilador puede generar un programa vacío que se ejecuta inmediatamente.

Si añadimos un uso a la variable a:

```
extern void f(int);

int main()
{
  int a = 0;
  for(int i=0;i<10000;++i) {
    a += 3;
  }  
  f(a);
  return 0;  
}
```

Ahora el optimizador no sabe si la función f(int) va a mostrar el dato que se le pasa.
Sin embargo, un optimizador suficientemente bueno, se daria cuenta que a siempre vale 30000 al final del bucle.
Por lo tanto, podría  eliminar la variable, eliminar el bucle y generar un programa que sólo llama a la función con un argumento de 30000.



# 3. ¿Qué tipo de cambios puede hacer?

Se permite cualquier cambio siempre que se cumplan las restricciones anteriores.

Por ejemplo:

*Eliminar una variable*

```
int main()
{
  int a = 3;
  ++a;
  std::cout << "Hello world" << std::endl;
  
  return 0;  
}
```

La variable a se puede eliminar.

*Reutilizar una variable*

```
extern int f(int);
int main()
{
  int a = f(1);
  std::cout << a << std::endl;
  int b = f(2);
  std::cout << b << std::endl;
  
  return 0;  
}
```

Las variables a y b pueden ser la misma.

*Reordenar código*

```
int main()
{
  int a = 4;
  if(a > 1) {
    std::cout << "Hello" << std::endl;
  }
  if(a > 1) {
    std::cout << "World" << std::endl;
  }
  
  return 0;  
}
```

La variable a puede desaparecer para usar la constante 4.
Eso hace que los if se puedan evaluar en tiempo de compilación y el código quedaría:

```
int main()
{
  std::cout << "Hello" << std::endl;
  std::cout << "World" << std::endl;
  
  return 0;  
}
```


*Inline functions*

```
int f(int a) {return a + 1;}
int main()
{
  int a = 4;
  std::cout << f(a) << std::endl;
 
  return 0;  
}
```

La llamada a la función f(int) se puede eliminar y dejar únicamente el cuerpo:
```
int main()
{
  int a = 4;
  std::cout << a + 1 << std::endl;
 
  return 0;  
}
```


*Loop unrolling*

```
int f(int a) {return a + 1;}
int main()
{
  int a[3];
  for(int i=0;i<3;++i) {
    a[i] = i;
  }
 
  return 0;  
}
```

El loop se puede quitar para dejar únicamente las asignaciones:

```
int f(int a) {return a + 1;}
int main()
{
  int a[3];
  a[0] = 0;
  a[1] = 1;
  a[2] = 2;
  
  return 0;  
}
```


*Compile time execution*

Parte del código se puede ejecutar en tiempo de compilación.

```
int f(int a) {return a + 1;}
int main()
{
  int a = 1;
  for(int i=0;i<10;++i) {
    a *= 2;
  }

  return 0;  
}
```



# 4. ¿Cómo se relaciona con los benchmarks?

Normalmente, uno de los parámetros que el optimizador intenta mejorar es el tiempo de ejecución. 
Para ello, puede hacer modificaciones en el código que se puede medir, estropeando las mediciones.

Por ejemplo, 

,
Para el optimizador, el código que se utiliza para leer tiempos no es diferente del código normal.
Por lo tanto, es posible reordenarlo.

Por ejemplo, tomemos el siguiente código que intenta medir el tiempo de la función ```f()```.

```
extern int f(int a);
int main()
{
  tic();
  for(int i=0;i<1000;++i) {
     f(a);
  }
  std::cout << toc() << std::endl;
 
  return 0;  
}
```

Por un lado, si el optimizador tiene acceso al código de la función f() y no tiene ningún efecto en la salida del programa, puede eliminar las llamadas a la función.



# 5. ¿Cómo se relaciona con el multi-hilo?




# 6. ¿Cómo se relaciona con el comportamiento indefinido?



# 7. ¿Cómo puedo ayudar al optimizador?



