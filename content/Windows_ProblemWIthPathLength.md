Title: Problema con la longitud de las rutas en Windows
Date: 2023-10-28
Category: Windows
Tags: C++, Windows
Summary: Una ruta es el camino para llegar a un archivo pero, ¿qué límites tiene?


# Los paths en Windows

Como primer punto, conviene recordar cómo se contruyen la ruta de un archivo en Windows:

 - Letra de la unidad, seguido por el separador ':'.
 - Barra '\' para indicar el directorio raíz.
 - Nombres de directorios, separados por '\'.
 - Nombre del archivo.

Cada uno de estos puntos es opcional.
Por ejemplo, las siguientes rutas indican:

- **Directorio\archivo.pdf**: Ruta relativa desde el directorio actual.
- **C:\Directorio\archivo.pdf**: Ruta absoluta desde el raíz de la unidad C.
- **C:Directorio\archivo.pdf**: Ruta relativa desde el directorio actual de la unidad C.

Los directorios con significados especiales son:

 - **..**: directorio anterior.
 - **.**: directorio actual.


# El límite de tamaño de ruta

En las ediciones de Windows anteriores a Windows 10 versión 1607
el tamaño máximo de la ruta que se puede pasar a una función de Windows es de MAX_PATH, 
que se define como 260 caracteres incluyendo el último de terminación.
Es decir, no se puede pasar una ruta superior a 259 caracteres.

Además, la ruta de los directorios deben permitir archivos cuyo nombre tenga el formato 8+3 (8 caracteres + 3 de extensión). 
Por lo tanto, no pueden ser superior a 248 caracteres.

Esto choca con algunos los sistemas de archivos. 
Por ejemplo NTFS permite nombres de archivos hasta 255 caracteres.
Aún así Windows impone su propias limitaciones.


# Solución a partir de Windows 10 versión 1607

A partir de Windows 10 versión 1607 se permiten rutas más largas, pero no por defecto.
Son necesarias dos condiciones para que una aplicación pueda usarlas:

- La clave *Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled*del Registro debe existir y establecerse en 1.
- El manifiesto de aplicación también debe incluir el elemento *ws2:longPathAware*.

Si se cumplen estas dos condiciones, muchas de las funciones del API de Windows pierden la limitación de 260 caracteres.


# Solución usando rutas extendidas

Las versiones de Unicode del API de Windows admiten rutas de hasta 32676 caracteres, pero éstas deben empezar por el prefijo *"\\?\"*.
Por ejemplo, se podría usar:

*\\?\C:\NombreDirectorioMuyLargo\NombreDeArchivoLargo*.

Sin embargo, no se puede usar este sistema para referirse a rutas de acceso relativas, que siguen teniendo la limitación de MAX_PATH caracteres.

Existe un problema extra con este sistema. 
A día de hoy, el módulo **filesystem** de la librería estándar de C++ que viene con el compilador de Microsoft no gestiona correctamente los paths con este prefijo.


# Referencias

[Maximum Path Length Limitation](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry)

[Naming Files, Paths, and Namespaces](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file)

[File path formats on Windows systems](https://docs.microsoft.com/es-es/dotnet/standard/io/file-path-formats)

[Is there an equivalent to WinAPI's MAX_PATH under linux/unix?](https://stackoverflow.com/a/837855/218774)
