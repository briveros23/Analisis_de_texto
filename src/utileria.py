from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from textblob import TextBlob
from textblob.exceptions import NotTranslated
import numpy as np
import nltk
nltk.download('punkt_tab')

    
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