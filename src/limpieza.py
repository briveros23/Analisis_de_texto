import re 

class limpieza_regex:
    """
    Clase para realizar limpieza de texto, que incluye la eliminación de números, caracteres especiales,
    tildes, espacios dobles y stopwords de una lista de sentencias.

    Atributos:
        datos: Lista de sentencias a procesar.
    """

    def limpieza_de_textos(sentencias):
        """
        Realiza la limpieza de textos eliminando números, caracteres especiales, tildes y espacios dobles.

        Parámetros:
            sentencias (list): Lista de sentencias a limpiar.

        Retorna:
            list: Lista de sentencias limpiadas.
        """
        textos_limpios = []
        for texto in sentencias:
            texto = str(texto)  # Asegurarse de que el texto sea una cadena
            texto = texto.lower()  # Minimizar texto
            texto = re.sub(r'\b\w*\d\w*\b', '', texto)  # Eliminar números
            texto = re.sub(r'[^\w\s]', '', texto)  # Eliminar caracteres especiales
            texto = re.sub(r'[áéíóúÁÉÍÓÚ]', lambda x: 'aeiouAEIOU'['áéíóúÁÉÍÓÚ'.index(x.group(0))], texto)  # Eliminar tildes
            texto = re.sub(r'\s+', ' ', texto).strip()  # Eliminar espacios dobles
            textos_limpios.append(texto)
        return textos_limpios

    def stop_words( stop_words, sentencias):
        """
        Elimina las palabras vacías (stopwords) de las sentencias.

        Parámetros:
            stop_words (list): Lista de palabras vacías a eliminar.
            sentencias (list): Lista de sentencias de texto.

        Retorna:
            list: Lista de sentencias sin las stopwords.
        """
        textos_limpios = []
        for texto in sentencias:
            texto = ' '.join([word for word in texto.split() if word not in stop_words])  # Eliminar stopwords
            textos_limpios.append(texto)
        return textos_limpios
