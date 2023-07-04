Title: Problema con la longitud de las rutas en Windows
Date: 2019-11-09 13:14
Category: Windows
Status: draft


# Los paths en Windows

Las rutas de archivos en Windows se componen de:
 - Letra de la unidad, seguido por el separador ':'.
 - Barra '\' para indicar el directorio raíz.
 - Nombres de directorios, separados por '\'.
 - Nombre del archivo.

Por ejemplo, las siguientes rutas indican:
Directorio\archivo.pdf	Ruta relativa desde el directorio actual.
C:\Directorio\archivo.pdf	Ruta absoluta desde el raíz de la unidad C.
C:Directorio\archivo.pdf	Ruta relativa desde el directorio actual de la unidad C.

Los directorios con significados especiales son:
 - *..*: directorio anterior.
 - *.*: directorio actual.

# El límite de tamaño

En algunas versiones antiguas de Windows, el tamaño máximo de la ruta que se puede pasar a una función de Windows es de 260 caracteres, incluyendo el último de terminación.
Es decir, no se puede pasar una ruta superior a 259 caracteres.

Sin embargo, no es el tamaño máximo de un path absoluto de un archivo.
Por ejemplo, un si la ruta de un archivo es "C:\NombreGrande\NombrePequeño\a.txt", podemos poner la ruta actual de C: en "c:\NombreGrande" y luego pasar la ruta relativa "NombrePequeño\a".
Mientras ambas rutas no sobrepasen 259 caracteres, no habrá ningún problema.



# Referencias
https://docs.microsoft.com/es-es/windows/win32/fileio/naming-a-file
https://docs.microsoft.com/es-es/dotnet/standard/io/file-path-formats
https://stackoverflow.com/a/837855/218774
