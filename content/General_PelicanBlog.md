Title: Crear un blog con Pelican en github
Date: 2023-07-04
Category: Blogs
Status: draft


# Introducción

Este blog está creado con Pelican y servido por GibHub Pages.

Pelican es una aplicación desarrollada en Python para crear páginas web estáticas a partir de archivos Markdown.

GitHub Pages es una utilidad de GitHub que permite alojar páginas web estáticas a partir de repositorios de GitHub.

Para mantener el blog actualizado, tenemos un único repositorio con dos ramas:

* main: contiene los archivos fuente necesarios para generar el blog.
* gh-pages: contiene los archivos del blog.

Además, se ha creado una acción para regenerar la rama *gh-pages* cada vez que se sube un cambio a la rama *main*.


# Instalación de Pelican

Los pasos para instalar Pelican son:

1. Instalar Python. En el momento de escribir este texto, estoy usando Python 3.11.4.
1. Instalar Pelican en Python: ```python -m pip install "pelican[markdown]"```

Hay más información en la [guía de inicio de Pelican](https://docs.getpelican.com/en/stable/quickstart.html#installation).


# Crear el repositorio de páginas de GitHub

GibHub permite alojar una página web estática a partir de un repositorio de GibHub.
Estas páginas pueden servir, por ejemplo, para la documentación de un proyecto. 
Sin embargo, hay un repositorio especial que sirve como presentación del perfil de GibHub que es el que vamos a usar para el blog.

Para crearlo, hay que seguir los siguientes pasos:

1. Crear un repositorio en GibHub con el nombre *username.github.io* donde username es nuestro nombre de usuario.
1. Crear una rama *gh-pages*.
1. Abrir las opciones del repositorio.
1. Entrar dentro de las opciones de Pages y seleccionar:
    * Source: deploy from branch.
    * Branch: gh-pages/root

1. Clonar el repositorio en local, usando ```git clone https://github.com/username/username.github.io```

En vez de generar los archivos del blog en local y subirlos a GitHub, podemos crear una acción para regenerarlos automáticamente.
Para ello, hay que crear un directorio *.github/workflows* dentro del repositorio y colocar un archivo.

Puedes ver un ejemplo en [pelican_blog.yml](https://github.com/jcallejap/jcallejap.github.io/blob/main/.github/workflows/pelican_blog.yml).

Este ejemplo está basado en el repositorio de [nelsonjchen](https://github.com/nelsonjchen/gh-pages-pelican-action)


# Creación de un proyecto de blog

Una vez instalado Pelican y preparado el repositorio, se puede ya comenzar con el blog:

1. Entrar dentro del directorio donde se ha clonado el repositorio de GitHub.
1. Crear el archivo de requerimientos de Python usando ```pip freeze > requirements.txt```
1. Ejecutar ```pelican-quickstart```.
1. Contestar a las preguntas que se va haciendo. Muchas de ellas se puede dejar el valor por defecto, aunque conviene personalizar:
    * Título del blog.
    * Autor del blog.
    * Prefijo URL. Se puede seleccionar que no, si no se va a publicar el blog en otra url.
    * Subir el blog a GitHub Pages: se selecciona que sí.
    * Es un blog personal de GitHub Pages: si es el caso, se puede seleccionar.

Una vez creado el esqueleto, los artículos se escriben en formato Markdown dentro del directorio *content*.

Para generar el blog localmente, se utiliza ```pelican content```.

Para visualizar el blog en local, se debe ejecutar: ```pelican --listen``` y abrir la página [local](http://localhost:8000/) con un navegador.


# Temas

Para listar los temas disponbiles basta con hacer:
pelican-themes --lista

