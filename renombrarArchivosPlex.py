from pathlib import Path
import re


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Extensiones de vídeo que queremos procesar
VIDEO_EXTENSIONS = {
    ".mkv",
    ".mp4",
    ".avi",
    ".mov",
    ".wmv",
    ".m4v",
    ".ts"
}

# Extensiones de subtítulos que también queremos renombrar
SUBTITLE_EXTENSIONS = {
    ".srt",
    ".ass",
    ".ssa",
    ".sub",
    ".vtt"
}


# ============================================================
# FUNCIONES PARA PEDIR DATOS
# ============================================================

def obtener_carpeta():
    """
    Pide al usuario la ruta de una carpeta hasta que introduzca
    una ruta válida.
    """

    while True:
        ruta = input(
            "\nIntroduce la ruta de la carpeta donde están los capítulos:\n> "
        ).strip().strip('"')

        carpeta = Path(ruta)

        if carpeta.exists() and carpeta.is_dir():
            return carpeta

        print("\n❌ La carpeta no existe o no es válida.")


def obtener_entero(mensaje, minimo=1):
    """
    Pide un número entero válido.
    """

    while True:
        valor = input(mensaje).strip()

        # Si el usuario no introduce nada, devolvemos None
        if valor == "":
            return None

        try:
            numero = int(valor)

            if numero >= minimo:
                return numero

            print(
                f"❌ Introduce un número mayor o igual que {minimo}."
            )

        except ValueError:
            print("❌ Introduce un número válido.")


# ============================================================
# DETECCIÓN DEL NOMBRE DE LA SERIE
# ============================================================

def obtener_nombre_serie(carpeta):
    """
    Obtiene el nombre de la serie directamente del nombre
    de la carpeta seleccionada.

    Ejemplo:

    D:\\Series\\Solo Leveling

    Resultado:
    Solo Leveling
    """

    nombre_serie = carpeta.name

    # Reemplazamos separadores habituales por espacios
    nombre_serie = nombre_serie.replace("_", " ")
    nombre_serie = nombre_serie.replace(".", " ")

    # Eliminamos espacios duplicados
    nombre_serie = " ".join(nombre_serie.split())

    return nombre_serie


# ============================================================
# BÚSQUEDA DE ARCHIVOS
# ============================================================

def buscar_archivos_video(carpeta):
    """
    Busca todos los archivos de vídeo directamente dentro
    de la carpeta seleccionada.

    No entra en subcarpetas.
    """

    archivos = []

    for archivo in carpeta.iterdir():

        if (
            archivo.is_file()
            and archivo.suffix.lower() in VIDEO_EXTENSIONS
        ):
            archivos.append(archivo)

    # Ordenamos alfabéticamente
    return sorted(
        archivos,
        key=lambda archivo: archivo.name.lower()
    )


# ============================================================
# DETECCIÓN DEL NÚMERO DE EPISODIO
# ============================================================

def detectar_episodio(nombre):
    """
    Intenta detectar el número del episodio a partir
    del nombre del archivo.

    Ejemplos soportados:

    Serie.S01E03
    Serie.S1E3
    Serie.1x03
    Episode 03
    Episodio 03
    Capitulo 03
    Ep 03
    E03
    2329_2_SUB
    """

    patrones = [

        # ----------------------------------------------------
        # S01E03
        # S1E3
        # ----------------------------------------------------
        r"[Ss]\d{1,2}[Ee](\d{1,3})",

        # ----------------------------------------------------
        # 1x03
        # 01x03
        # ----------------------------------------------------
        r"\d{1,2}[xX](\d{1,3})",

        # ----------------------------------------------------
        # Episode 03
        # Episodio 03
        # ----------------------------------------------------
        r"(?:episode|episodio)[ ._-]*(\d{1,3})",

        # ----------------------------------------------------
        # Capitulo 03
        # Capítulo 03
        # ----------------------------------------------------
        r"cap[ií]tulo[ ._-]*(\d{1,3})",

        # ----------------------------------------------------
        # Ep 03
        # EP.03
        # ----------------------------------------------------
        r"\bep\.?[ ._-]*(\d{1,3})",

        # ----------------------------------------------------
        # E03
        # ----------------------------------------------------
        r"\b[Ee](\d{1,3})\b",

        # ----------------------------------------------------
        # Formato:
        #
        # 2329_2_SUB
        # 12345_12_SUB
        #
        # Cogemos el número entre "_" y "_SUB"
        # ----------------------------------------------------
        r"_(\d{1,3})_[Ss][Uu][Bb]\b",
    ]

    for patron in patrones:

        coincidencia = re.search(
            patron,
            nombre,
            re.IGNORECASE
        )

        if coincidencia:

            return int(
                coincidencia.group(1)
            )

    # No se ha encontrado ningún episodio
    return None


# ============================================================
# BÚSQUEDA DE SUBTÍTULOS
# ============================================================

def obtener_subtitulos_relacionados(video):
    """
    Busca subtítulos relacionados con un archivo de vídeo.

    Ejemplos:

    episodio_01.mkv
    episodio_01.srt

    También:

    episodio_01.mkv
    episodio_01.es.srt
    episodio_01.eng.srt
    """

    subtitulos = []

    for archivo in video.parent.iterdir():

        if not archivo.is_file():
            continue

        if archivo.suffix.lower() not in SUBTITLE_EXTENSIONS:
            continue

        # Subtítulo con exactamente el mismo nombre base
        if archivo.stem == video.stem:

            subtitulos.append(
                (archivo, "")
            )

        # Ejemplo:
        #
        # episodio_01.es.srt
        #
        elif archivo.name.startswith(
            video.stem + "."
        ):

            parte_extra = archivo.name[
                len(video.stem):
                -len(archivo.suffix)
            ]

            subtitulos.append(
                (archivo, parte_extra)
            )

    return subtitulos


# ============================================================
# CREACIÓN DEL PLAN DE RENOMBRADO
# ============================================================

def crear_plan_renombrado(
    archivos,
    serie,
    temporada,
    episodio_inicial
):
    """
    Crea una lista con todos los cambios que se realizarán.

    Primero intenta detectar automáticamente el número
    de episodio de cada archivo.

    Si todos los archivos tienen un episodio detectable,
    utiliza esos números.

    Si alguno no puede detectarse, ordena todos los
    archivos alfabéticamente y los numera consecutivamente.
    """

    plan = []

    episodios_detectados = []

    print("\n🔎 Analizando archivos...\n")

    for archivo in archivos:

        episodio = detectar_episodio(
            archivo.stem
        )

        episodios_detectados.append(
            episodio
        )

        if episodio is not None:

            print(
                f"✔ {archivo.name}"
                f" → Episodio detectado: {episodio}"
            )

        else:

            print(
                f"⚠ {archivo.name}"
                f" → No se ha podido detectar el episodio"
            )

    # ========================================================
    # CASO 1:
    # Todos los archivos tienen un episodio detectable
    # ========================================================

    if all(
        episodio is not None
        for episodio in episodios_detectados
    ):

        print(
            "\n✅ Se han detectado todos los números "
            "de episodio automáticamente."
        )

        for archivo, episodio in zip(
            archivos,
            episodios_detectados
        ):

            nuevo_nombre = (
                f"{serie} - "
                f"S{temporada:02d}"
                f"E{episodio:02d}"
                f"{archivo.suffix.lower()}"
            )

            destino = archivo.with_name(
                nuevo_nombre
            )

            plan.append(
                (archivo, destino)
            )

    # ========================================================
    # CASO 2:
    # Alguno de los archivos no tiene episodio detectable
    # ========================================================

    else:

        print(
            "\n⚠️ Algunos archivos no tienen un número "
            "de episodio detectable."
        )

        print(
            "Se utilizará el orden alfabético de los archivos."
        )

        # Si el usuario no ha indicado episodio inicial
        if episodio_inicial is None:

            episodio_inicial = 1

        episodio_actual = episodio_inicial

        for archivo in archivos:

            nuevo_nombre = (
                f"{serie} - "
                f"S{temporada:02d}"
                f"E{episodio_actual:02d}"
                f"{archivo.suffix.lower()}"
            )

            destino = archivo.with_name(
                nuevo_nombre
            )

            plan.append(
                (archivo, destino)
            )

            episodio_actual += 1

    return plan


# ============================================================
# MOSTRAR VISTA PREVIA
# ============================================================

def mostrar_plan(plan):
    """
    Muestra todos los cambios antes de realizar
    el renombrado.
    """

    print("\n")
    print("=" * 70)
    print("VISTA PREVIA DE LOS CAMBIOS")
    print("=" * 70)

    for origen, destino in plan:

        print(f"\n📄 {origen.name}")
        print("   ↓")
        print(f"📺 {destino.name}")

    print("\n" + "=" * 70)


# ============================================================
# COMPROBAR CONFLICTOS
# ============================================================

def comprobar_conflictos(plan):
    """
    Comprueba si alguno de los nombres de destino
    ya existe.

    Esto evita sobrescribir accidentalmente archivos.
    """

    conflictos = []

    archivos_originales = {
        origen
        for origen, destino in plan
    }

    for origen, destino in plan:

        if (
            destino.exists()
            and destino not in archivos_originales
        ):

            conflictos.append(
                (origen, destino)
            )

    return conflictos


# ============================================================
# RENOMBRAR ARCHIVOS
# ============================================================

def renombrar_archivos(plan):
    """
    Renombra los vídeos y también los subtítulos
    relacionados.
    """

    for origen, destino in plan:

        # Buscamos los subtítulos antes de renombrar
        subtitulos = obtener_subtitulos_relacionados(
            origen
        )

        # Renombramos el vídeo
        origen.rename(destino)

        print(
            f"✔ Vídeo renombrado:"
            f"\n  {destino.name}"
        )

        # ----------------------------------------------------
        # Renombramos los subtítulos relacionados
        # ----------------------------------------------------

        for subtitulo, parte_extra in subtitulos:

            # Quitamos la extensión del vídeo
            nuevo_subtitulo_base = destino.with_suffix(
                ""
            )

            nuevo_nombre_subtitulo = (
                nuevo_subtitulo_base.name
                + parte_extra
                + subtitulo.suffix.lower()
            )

            destino_subtitulo = subtitulo.with_name(
                nuevo_nombre_subtitulo
            )

            try:

                subtitulo.rename(
                    destino_subtitulo
                )

                print(
                    f"   ↳ Subtítulo renombrado:"
                    f"\n     {destino_subtitulo.name}"
                )

            except FileExistsError:

                print(
                    f"   ⚠️ No se ha podido renombrar:"
                    f"\n     {subtitulo.name}"
                    f"\n     Ya existe un archivo con el "
                    f"nombre destino."
                )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("RENOMBRADOR DE SERIES PARA PLEX")
    print("=" * 70)

    print(
        "\nEl programa utilizará el nombre de la carpeta "
        "seleccionada como nombre de la serie."
    )

    print(
        "\nFormato final:"
    )

    print(
        "Nombre Serie - S01E01.ext"
    )

    # ========================================================
    # SELECCIONAR CARPETA
    # ========================================================

    carpeta = obtener_carpeta()

    print(
        f"\n📁 Carpeta seleccionada:"
        f"\n{carpeta}"
    )

    # ========================================================
    # OBTENER NOMBRE DE LA SERIE
    # ========================================================

    serie = obtener_nombre_serie(
        carpeta
    )

    print(
        f"\n📺 Serie detectada:"
        f" {serie}"
    )

    # ========================================================
    # BUSCAR ARCHIVOS
    # ========================================================

    archivos = buscar_archivos_video(
        carpeta
    )

    if not archivos:

        print(
            "\n❌ No se han encontrado archivos "
            "de vídeo en esta carpeta."
        )

        return

    print(
        f"\n🎬 Se han encontrado "
        f"{len(archivos)} archivos de vídeo."
    )

    print("\nArchivos encontrados:")

    for archivo in archivos:

        print(
            f" - {archivo.name}"
        )

    # ========================================================
    # PEDIR TEMPORADA
    # ========================================================

    temporada = obtener_entero(
        "\nNúmero de temporada: "
    )

    # ========================================================
    # PEDIR EPISODIO INICIAL
    # ========================================================

    print(
        "\nEl siguiente valor solo se utilizará si "
        "no se pueden detectar automáticamente "
        "todos los episodios."
    )

    episodio_inicial = obtener_entero(
        "Primer número de episodio "
        "(pulsa ENTER para usar 1): "
    )

    # ========================================================
    # CREAR PLAN
    # ========================================================

    plan = crear_plan_renombrado(
        archivos,
        serie,
        temporada,
        episodio_inicial
    )

    # ========================================================
    # MOSTRAR VISTA PREVIA
    # ========================================================

    mostrar_plan(
        plan
    )

    # ========================================================
    # COMPROBAR CONFLICTOS
    # ========================================================

    conflictos = comprobar_conflictos(
        plan
    )

    if conflictos:

        print(
            "\n❌ SE HAN ENCONTRADO CONFLICTOS:"
        )

        for origen, destino in conflictos:

            print(
                f"\nArchivo original:"
                f"\n{origen.name}"
            )

            print(
                f"Nombre destino:"
                f"\n{destino.name}"
            )

        print(
            "\nPor seguridad no se realizará "
            "ningún cambio."
        )

        return

    # ========================================================
    # CONFIRMACIÓN FINAL
    # ========================================================

    confirmacion = input(
        "\n¿Quieres realizar estos cambios? (s/n): "
    ).strip().lower()

    if confirmacion not in (
        "s",
        "si",
        "sí",
        "y",
        "yes"
    ):

        print(
            "\n❌ Operación cancelada."
        )

        print(
            "No se ha modificado ningún archivo."
        )

        return

    # ========================================================
    # RENOMBRAR
    # ========================================================

    print(
        "\n🚀 Renombrando archivos...\n"
    )

    try:

        renombrar_archivos(
            plan
        )

        print("\n")
        print("=" * 70)
        print("✅ PROCESO TERMINADO CORRECTAMENTE")
        print("=" * 70)

        print(
            f"\nSe han procesado "
            f"{len(plan)} episodios."
        )

    except Exception as error:

        print(
            "\n❌ HA OCURRIDO UN ERROR:"
        )

        print(
            f"\n{error}"
        )


# ============================================================
# EJECUTAR PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()