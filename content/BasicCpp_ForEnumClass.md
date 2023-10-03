Title: ¿Cómo iterar un enum class?
Date: 2023-26-09
Category: Resolución de problemas en C++


# 0. Introducción al problema

Supongamos que tenemos una enumeración, basada en un entero y sin saltos entre sus elementos. 
Es decir, algo como: 

´´´
enum class Enumeration : int {A, B, C, D, E};
´´´

Ahora, queremos recorrer todos sus valores.

Por defecto, los valores de una enumeración son incrementales de uno en uno, así que podríamos pensar en algo como:

´´´
for(int i=Enumeration::A;i<=Enumeration::E;++i) {
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
enum class Enumeration : int {A, B, C, D, E};

for(int i=static_cast<int>(Enumeration::A);i<=static_cast<int>(Enumeration::E);++i) {
  // ...
}
´´´

Este código, aunque correcto, tiene varios problemas:

- Es una línea muy larga, difícil de comprobar de un simple vistazo.
- Si se cambia la enumeración, hay que cambiar todos los ´´´for´´´.


# 2. Añadir la información de la iteración dentro del propio enumerador

Una mejor aproximación es añadir el comienzo y el final de los valores dentro del enumerador:

´´´
enum class Enumeration : int {A, B, C, D, E, BEGIN=A, END=E};
´´´

De esta forma, el código para iterar quedaría:

´´´
for(int i=static_cast<int>(Enumeration::BEGIN);i<=static_cast<int>(Enumeration::END);++i) {
  // ...
}
´´´

La línea sigue siendo muy larga, pero la información sobre el comienzo y el final están incluidas dentro de la propia definición.
De esta forma, si se modifican los valores del enum, es fácil ver que también hay que modificar el comienzo y el final.


# 3. Crear una clase para iterar

Una solución algo más complicada consiste en crear una clase para iterar enumeradores:

´´´
#include <type_traits>


template <typename TYPE, TYPE begin_val, TYPE end_val>
class EnumClassIterator {
  typedef typename std::underlying_type<TYPE>::type value_type;

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


# 4. Enlaces

[What are commonly-used ways to iterate over an enum class in C++?](https://stackoverflow.com/q/69762598/218774)
[How can I iterate over an enum?(https://stackoverflow.com/q/261963/218774)