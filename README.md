# CambiarNombrePlex

Herramienta desarrollada en ****Python**** para renombrar automáticamente archivos de series y prepararlos para que ****Plex**** pueda identificarlos correctamente.

El proyecto nace para solucionar un problema muy habitual al descargar contenido: los archivos pueden tener nombres diferentes, poco descriptivos o formatos que Plex no reconoce correctamente. La aplicación analiza los nombres de los archivos, detecta el número de episodio y los convierte a un formato compatible con Plex.

> 🚧 ****Proyecto en desarrollo:**** esta es una primera versión. Se irán incorporando nuevas funcionalidades y mejoras progresivamente.

## ✨ Características actuales

-   📁 Obtención automática del nombre de la serie a partir de la carpeta seleccionada.
-   🎬 Detección de archivos de vídeo.
-   🔎 Detección automática del número de episodio.
-   📺 Soporte para diferentes formatos de nombres, por ejemplo:
-   -   `S01E03`
    -   `S1E3`
    -   `1x03`
    -   `E03`
    -   `Episode 03`
    -   `Episodio 03`
    -   `Capitulo 03`
    -   `2329_2_SUB`
-   🔢 Formato de salida compatible con Plex:
    
    ```
    Nombre de la serie - S01E01.mkv
    ```
    
-   💬 Vista previa de los cambios antes de modificar los archivos.
-   🛡️ Comprobación de conflictos para evitar sobrescribir archivos existentes.
-   💬 Renombrado de subtítulos asociados (`.srt`, `.ass`, `.ssa`, `.sub`, `.vtt`).
-   💻 Funcionamiento mediante terminal en Windows.
-   📦 Sin dependencias externas.

## 🖥️ Ejemplo

Supongamos que tenemos la siguiente carpeta:

```
D:\Series\Solo Leveling
```

Con estos archivos:

2329\_1\_SUB.mkv  
2329\_2\_SUB.mkv  
2329\_3\_SUB.mkv  
2329\_4\_SUB.mkv

La aplicación detectará automáticamente:

Serie: Solo Leveling  
  
2329\_1\_SUB.mkv → Episodio 1  
2329\_2\_SUB.mkv → Episodio 2  
2329\_3\_SUB.mkv → Episodio 3  
2329\_4\_SUB.mkv → Episodio 4

Y los convertirá en:

Solo Leveling - S01E01.mkv  
Solo Leveling - S01E02.mkv  
Solo Leveling - S01E03.mkv  
Solo Leveling - S01E04.mkv

De esta forma, Plex puede identificar correctamente la serie y sus episodios.

## 🚀 Instalación

### Requisitos

-   Windows
-   Python 3.11 o superior
-   No se requieren paquetes externos.

Puedes comprobar que Python está instalado ejecutando:

```
py --version
```

### Clonar el repositorio

```
git clone https://github.com/paula-ayllon-perez/RenombrarArchivosPlex.git
```

Entrar en el proyecto:

```
cd RenombrarArchivosPlex
```

## ▶️ Uso

Ejecuta:

```
py renombrarArchivosPlex.py
```

La aplicación solicitará la carpeta que contiene los episodios:

Introduce la ruta de la carpeta principal donde están los capítulos:  
\> D:\\Series\\Solo Leveling

El nombre de la carpeta se utilizará automáticamente como nombre de la serie.

A continuación, se indicará la temporada:

Número de temporada:  
\> 1

La aplicación analizará los archivos y las subcarpetas y mostrará una vista previa:

\======================================================================  
VISTA PREVIA DE LOS CAMBIOS  
\======================================================================  
  
📄 2329\_1\_SUB.mkv  
   ↓  
📺 Solo Leveling - S01E01.mkv  
  
📄 2329\_2\_SUB.mkv  
   ↓  
📺 Solo Leveling - S01E02.mkv  
  
📄 2329\_3\_SUB.mkv  
   ↓  
📺 Solo Leveling - S01E03.mkv

Finalmente, solicitará confirmación antes de realizar los cambios.

## 🗂️ Estructura del proyecto

CambiarNombrePlex/  
│  
├── renombrarArchivosPlex.py
├── README.md  
└── ...

La estructura podrá cambiar a medida que el proyecto evolucione y se incorporen nuevas funcionalidades.

## 🤝 Contribuciones

El proyecto está en desarrollo y cualquier sugerencia, mejora o propuesta de nuevos formatos de nombres es bienvenida.

Si encuentras un formato de archivo que la aplicación no detecta correctamente, puedes abrir un ****Issue**** indicando:

1.  El nombre del archivo.
2.  Qué número de episodio debería detectar.
3.  El resultado obtenido por la aplicación.

Esto ayudará a mejorar progresivamente el sistema de detección.
