from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import re
from unidecode import unidecode
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from itertools import combinations
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob.exceptions import NotTranslated
import re
import numpy as np
import nltk
nltk.download('punkt')

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
    



class sentence_similarity:
    """
    Clase para calcular la similitud entre sentencias usando embeddings y PCA para reducción de dimensionalidad,
    seguida de un agrupamiento con K-Means.

    Atributos:
        model: Modelo de embeddings para codificar las sentencias.
        pca: Objeto PCA para reducción de dimensionalidad.
        embeddings: Embeddings generados para las sentencias.
        component: Componentes principales tras aplicar PCA.
    """

    def __init__(self, model, sentencias, n_componentes=2):
        """Inicializa el modelo, codifica las sentencias y aplica PCA."""
        self.model = model
        self.pca = PCA(n_components=n_componentes)
        self.embeddings = self.model.encode(sentencias)
        self.pca = self.pca.fit(self.embeddings)
        self.component = self.pca.fit_transform(self.embeddings)

    def varianza_explicada(self):
        """Retorna la varianza explicada por los componentes principales."""
        return self.pca.explained_variance_

    def componentes(self):
        """Retorna los componentes principales de las sentencias."""
        return self.component

    def k_means(self, clusters):
        """Aplica K-Means a los componentes principales."""
        return KMeans(n_clusters=clusters).fit(self.component)

  



class graficos():

  def plot_column_combinations(coordinates, colors=None, labels=None):
    """
    Genera gráficos combinando las columnas de un array de coordenadas.
    Puede pintar los puntos usando un vector de colores y agregar etiquetas a los puntos.

    Parámetros:
    - coordinates: np.ndarray (n x m) donde n son puntos y m son dimensiones.
    - colors: List o np.ndarray (opcional) para colorear los puntos.
    - labels: List o np.ndarray (opcional) con nombres o etiquetas para los puntos.

    Retorna:
    - Gráficos de las combinaciones posibles de columnas.
    """
    num_cols = coordinates.shape[1]
    col_combinations = list(combinations(range(num_cols), 2))  # Combinaciones de columnas
    
    # Configurar los subgráficos
    n_combinations = len(col_combinations)
    fig, axes = plt.subplots(1, n_combinations, figsize=(5 * n_combinations, 5))

    if n_combinations == 1:
        axes = [axes]  # Para manejar el caso de un solo gráfico
    
    # Iterar sobre combinaciones de columnas
    for ax, (col1, col2) in zip(axes, col_combinations):
        # Pintar los puntos con o sin colores
        if colors is not None:
            scatter = ax.scatter(coordinates[:, col1], coordinates[:, col2], c=colors, cmap='viridis', s=50)
        else:
            ax.scatter(coordinates[:, col1], coordinates[:, col2], color='blue', s=50)
        
        # Agregar etiquetas a los puntos si se proporcionan
        if labels is not None:
            for i, label in enumerate(labels):
                ax.text(coordinates[i, col1], coordinates[i, col2], str(label), fontsize=8, ha='right', va='bottom')
        
        ax.set_title(f"Plano {col1+1} vs Plano {col2+1}")
        ax.set_xlabel(f"Plano {col1+1}")
        ax.set_ylabel(f"Plano {col2+1}")
        ax.grid(True)
    
    plt.tight_layout()
    plt.show()

  
  def generar_wordcloud(lista_oraciones):
    """
    Genera un WordCloud basado en la frecuencia de palabras a partir de una lista de oraciones.

    Parámetros:
    - lista_oraciones: lista de strings, cada string es una oración.
    """
    # 1. Unir todas las oraciones en un solo texto
    texto_completo = " ".join(lista_oraciones)
    
    # 2. Tokenizar y contar la frecuencia de palabras
    palabras = texto_completo.split()
    frecuencia_palabras = Counter(palabras)
    
    # 3. Crear el objeto WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frecuencia_palabras)
    
    # 4. Mostrar el WordCloud
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de Palabras")
    plt.show()

def analisis_sentimientos(textos):
    sentimientos = []
    for texto in textos:
        blob = TextBlob(texto)
        try:
            polaridad = blob.translate(from_lang='es', to='en').sentiment.polarity
        except NotTranslated:
            polaridad = blob.sentiment.polarity

        sentimiento = 1 if polaridad > 0.5 else -1 if polaridad < -0.5 else 0
        
        sentimientos.append(sentimiento)
    sentimiento = np.array([sentimiento])
    return sentimientos