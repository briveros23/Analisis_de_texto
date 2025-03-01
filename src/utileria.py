from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from textblob import TextBlob
from textblob.exceptions import NotTranslated
import numpy as np
import nltk
nltk.download('punkt_tab')
from sklearn.metrics import silhouette_score

    
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

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
        return KMeans(n_clusters=clusters, random_state=42, n_init=10).fit(self.component)

    def silhouette_method(X, k_min=2, k_max=10):
        silhouette_scores = []
        k_values = range(k_min, k_max + 1)

        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)
            silhouette_scores.append(silhouette_score(X, labels))

        plt.figure(figsize=(8, 5))
        plt.plot(k_values, silhouette_scores, marker='o', linestyle='-')
        plt.xlabel("Número de Clústeres (k)")
        plt.ylabel("Coeficiente de Silueta")
        plt.title("Método de la Silueta para Selección de k")
        plt.show()

    def silhouette_method(self, k_min=2, k_max=10):
        """Aplica el método de la silueta para evaluar la calidad de los clústeres."""
        silhouette_scores = []
        k_values = range(k_min, k_max + 1)

        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(self.component)
            silhouette_scores.append(silhouette_score(self.component, labels))

        # Gráfica del coeficiente de silueta
        plt.figure(figsize=(8, 5))
        plt.plot(k_values, silhouette_scores, marker='o', linestyle='-')
        plt.xlabel("Número de Clústeres (k)")
        plt.ylabel("Coeficiente de Silueta")
        plt.title("Método de la Silueta para Selección de k")
        plt.show()

  

def analisis_sentimientos(textos):
    sentimientos = []
    polaridades = []
    for texto in textos:
        blob = TextBlob(texto)
        try:
            polaridad = blob.translate(from_lang='es', to='en').sentiment.polarity
        except NotTranslated:
            polaridad = blob.sentiment.polarity

        sentimiento = 1 if polaridad > 0.5 else -1 if polaridad < -0.5 else 0
        
        sentimientos.append(sentimiento)
        polaridades.append(polaridad)
    
    sentimiento = np.array([sentimiento])

    return sentimientos,polaridades