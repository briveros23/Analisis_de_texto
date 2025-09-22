import matplotlib.pyplot as plt
from itertools import combinations
from wordcloud import WordCloud
from collections import Counter



class graficos():

  def plot_column_combinations(coordinates, max_dim=None, colors=None, labels=None):
    """
    Genera gráficos combinando las columnas de un array de coordenadas hasta una dimensión máxima especificada.
    Puede pintar los puntos usando un vector de colores y agregar etiquetas a los puntos.
    """
    num_cols = coordinates.shape[1]

    # Asegurar que max_dim sea válido
    if max_dim is None:
        max_dim = num_cols
    else:
        max_dim = min(int(max_dim), num_cols)

    col_combinations = list(combinations(range(max_dim), 2))  # Combinaciones de columnas
    
    # Configurar los subgráficos
    n_combinations = len(col_combinations)
    fig, axes = plt.subplots(1, n_combinations, figsize=(5 * n_combinations, 5))

    if n_combinations == 1:
        axes = [axes]  # Para manejar el caso de un solo gráfico
    
    # Iterar sobre combinaciones de columnas
    for ax, (col1, col2) in zip(axes, col_combinations):
        if colors is not None:
            scatter = ax.scatter(coordinates[:, col1], coordinates[:, col2], c=colors, cmap='viridis', s=50)
        else:
            ax.scatter(coordinates[:, col1], coordinates[:, col2], color='blue', s=50)
        
        if labels is not None:
            for i, label in enumerate(labels):
                ax.text(coordinates[i, col1], coordinates[i, col2], str(label), fontsize=8, ha='right', va='bottom')
        
        ax.set_title(f"Dimensión {col1+1} vs Dimensión {col2+1}")
        ax.set_xlabel(f"Dimensión {col1+1}")
        ax.set_ylabel(f"Dimensión {col2+1}")
        ax.grid(True)
    
    plt.tight_layout()
    plt.show()
  
  def generar_wordcloud(lista_oraciones, colormap="viridis"):
    """
    Genera un WordCloud basado en la frecuencia de palabras a partir de una lista de oraciones.
    Permite cambiar el color de las palabras usando un colormap.

    Parámetros:
    - lista_oraciones: lista de strings, cada string es una oración.
    - colormap: str (opcional), nombre de la paleta de colores de matplotlib. Ejemplo: 'viridis', 'plasma', 'inferno'.
    """
    # 1. Unir todas las oraciones en un solo texto
    texto_completo = " ".join(lista_oraciones)
    
    # 2. Tokenizar y contar la frecuencia de palabras
    palabras = texto_completo.split()
    frecuencia_palabras = Counter(palabras)
    
    # 3. Crear el objeto WordCloud con la paleta de colores definida
    wordcloud = WordCloud(width=800, height=400, background_color="white", colormap=colormap).generate_from_frequencies(frecuencia_palabras)
    
    # 4. Mostrar el WordCloud
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de Palabras")
    plt.show()
