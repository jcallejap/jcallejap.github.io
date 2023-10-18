Title: ¿Cómo iterar un enum class?
Date: 2023-18-10
Category: Resolución de problemas en C++


# 0. Introducción al problema

Supongamos que tenemos una enumeración, de tipo entero y sin saltos entre sus elementos. 
Es decir, algo como: 

´´´
enum class MyEnumeration : int {A, B, C, D, E};
´´´

Ahora, queremos recorrer todos sus valores.

Si no se indica lo contrario, los valores de una enumeración empiezan en cero y se incrementan de uno en uno.
Así que podríamos pensar en algo como:

´´´
for (int i = MyEnumeration::A; i <= MyEnumeration::E; ++i) {
  // ...
}
´´´

Este código tiene un problema importante: 
no compila porque los ´´´enum class´´´ no se convierten automáticamente a un entero. 

¿Qué formas existen para iterar un enumerador cuyos valores no tienen saltos?


# 1. Solución rápida


La solución más sencilla es iterar directamente sobre los valores iniciales y finales.
Algo parecido al código anterior pero añadiendo las conversiones:

´´´
enum class MyEnumeration : int { A, B, C, D, E };

for (int i = static_cast<int>(MyEnumeration::A); i <= static_cast<int>(MyEnumeration::E); ++i) {
  // ...
}
´´´

Este código, aunque correcto, tiene varios problemas:

- Es una línea muy larga, difícil de comprobar de un simple vistazo.
- Si se cambia la enumeración, hay que cambiar todos los ´´´for´´´.


# 2. Añadir la información de la iteración dentro del propio enumerador

Una mejor aproximación es añadir el comienzo y el final de los valores dentro del enumerador:

´´´
enum class MyEnumeration : int {A, B, C, D, E, BEGIN=A, END=E};
´´´

De esta forma, el código para iterar quedaría:

´´´
for(int i=static_cast<int>(MyEnumeration::BEGIN);i<=static_cast<int>(MyEnumeration::END);++i) {
  // ...
}
´´´

La línea sigue siendo muy larga, pero la información sobre el comienzo y el final están incluidas dentro de la propia definición.
De esta forma, si se modifican los valores del enum, es fácil ver que también hay que modificar el comienzo y el final.


# 3. Crear una clase para iterar

Una solución algo más complicada consiste en crear una clase para iterar enumeradores.
El objetivo es incluir esta clase en una cabecera para poder reusarla y añadir la forma del iterador junto a la declaración.

´´´
enum class MyEnumeration : int {A, B, C, D, E};
using MyEnumerationIterator = EnumClassIterator<MyEnumeration, MyEnumeration::A, MyEnumeration::E>;
´´´

De esta forma, si modificamos la enumeración, tenemos justo al lado la forma en la que se itera.

Posteriormente, podemos recorrer los valores de la enumeración mediante:

´´´
for (auto my_enum : MyEnumerationIterator{}) {
  // ...
}
´´´

En teoría, podríamos hacer una clase para generar la iteración y otra para los iteradores.
Sin embargo, por simplicidad, es preferible crear una única clase que haga ambas funciones aunque eso viole el [SRP](https://es.wikipedia.org/wiki/Principio_de_responsabilidad_%C3%BAnica).

La parte que genera la iteración debe cumplir:

- Tiene que estar templatizada.
- Tiene que tener el método begin() que devuelve un iterator.
- Tiene que tener el método end() que devuelve un iterator.

La parte del iterador tiene que cumplir:

- Tener un operador de dereferencia (*).
- Tener un operador de no igualdad (!=)
- Tener un operador de incremento (++)

En nuestro caso, cada iterador almacena un entero con el valor al que apunta, 
por lo que todas las comparaciones, incrementos y referencias se basan en ese entero.
Como la enumeración puede basarse en diversos tipos de valores, añadiremos la siguiente comprobación para asegurar que se basa en un entero:

´´´
static_assert(std::is_integral<value_type>::value);
´´´

El iterador final será el siguiente al último valor a iterar. 
Para evitar que eso dé problemas, añadiremos otra comprobación:

´´´
static_assert(static_cast<value_type>(end_val) < std::numeric_limits<value_type>::max());
´´´

Si tomamos todo en consideración, la clase quedaría:

´´´
#include <type_traits>

template <typename TYPE, TYPE begin_val, TYPE end_val>
class EnumClassIterator {
  typedef typename std::underlying_type<TYPE>::type value_type;
  static_assert(std::is_integral<value_type>::value);
  static_assert(static_cast<value_type>(end_val) < std::numeric_limits<value_type>::max());

 public:
  EnumClassIterator(const TYPE& value)
      : m_value(static_cast<value_type>(value)) {}
  EnumClassIterator() : m_value(static_cast<value_type>(begin_val)) {}
  EnumClassIterator& operator++() {
    ++m_value;
    return *this;
  }
  TYPE operator*() { return static_cast<TYPE>(m_value); }
  EnumClassIterator begin() { return {begin_val}; }
  EnumClassIterator end() {
    return {static_cast<TYPE>(static_cast<value_type>(end_val) + 1)};
  }
  bool operator!=(const EnumClassIterator& other) {
    return m_value != other.m_value;
  }

 private:
  value_type m_value;
};
´´´

Podemos ver un ejemplo de su uso en el proyecto [PuzzleADaySolver](https://github.com/jcallejap/PuzzleADaySolver/blob/main/Solver/EnumClassIterator.h):


# 4. Enlaces interesantes

[What are commonly-used ways to iterate over an enum class in C++?](https://stackoverflow.com/q/69762598/218774)
[How can I iterate over an enum?(https://stackoverflow.com/q/261963/218774)