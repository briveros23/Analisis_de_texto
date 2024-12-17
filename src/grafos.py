import nltk
import igraph as ig
from collections import Counter
import matplotlib.pyplot as plt

class grafos:
    def Generacion_de_skipgramas(text, n_palabras, k_saltos):
        '''Genera skipgrams de un texto dado con un tamaño de ventana n y un número de skips k.'''
        # Tokenize words
        words = nltk.word_tokenize(text)
        
        # Initialize list to store skipgrams
        skipgrams_list = []
        
        # Generate skipgrams
        for i in range(len(words)):
            # Create a window for the current position
            window = words[i:i+n_palabras+k_saltos]
            if len(window) < n_palabras:
                continue
            
            # Generate skipgrams from the window
            for j in range(len(window)):
                for k in range(j+1, min(j+1+k_saltos+1, len(window))):
                    skipgram = (window[j], window[k])
                    skipgrams_list.append(skipgram)
        skipgrams_list_final=[]
        for i in range(len(skipgrams_list)-1):
            if skipgrams_list[i]!=skipgrams_list[i+1]:
                skipgrams_list_final.append(skipgrams_list[i])
        return skipgrams_list_final

    def creacion_del_grafo(aristas):
        # Crear un grafo
        G = ig.Graph()

        # Conjunto de nodos existentes
        nodos_existentes = set()

        # Añadir las aristas al grafo
        for arista, peso in aristas:
            nodo1, nodo2 = arista

            if nodo1 != nodo2: 

                # Verificar si los nodos ya existen
                if nodo1 not in nodos_existentes:
                    G.add_vertex(nodo1)  # Agregar vértice origen
                    nodos_existentes.add(nodo1)  # Agregar nodo al conjunto de nodos existentes
                if nodo2 not in nodos_existentes:
                    G.add_vertex(nodo2)  # Agregar vértice destino
                    nodos_existentes.add(nodo2)  # Agregar nodo al conjunto de nodos existentes

                # Agregar arista con peso
                G.add_edge(nodo1, nodo2, weight=peso)

        return G

    def bigramas_para_grafo(lista_bigramas, umbral=10):
        # Utilizamos Counter para contar las ocurrencias de las tuplas en la lista
        lista_bigramas = [tuple(sorted(tupla)) for tupla in lista_bigramas]
        contador = Counter(lista_bigramas)
        
        # Filtramos las tuplas que tienen una frecuencia mayor que el umbral
        tuplas_filtradas = [(tupla ,frecuencia)for tupla, frecuencia in contador.items() if frecuencia > umbral]
        
        return tuplas_filtradas
    
    def plot_bigramas(skipgramas,top_n=10):
        # Conteo de bigramas
        conteo_bigramas = Counter(skipgramas)

        # Obtener los 10 bigramas más frecuentes
        bigramas_mas_frecuentes = conteo_bigramas.most_common(top_n)

        # Obtener datos para el gráfico
        bigramas_unicos = [bigrama[0] for bigrama in bigramas_mas_frecuentes]
        frecuencias = [frecuencia for _, frecuencia in bigramas_mas_frecuentes]

        # Graficar
    
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(bigramas_unicos)), frecuencias, tick_label=[f"{bigrama[0]} {bigrama[1]}" for bigrama in bigramas_unicos])
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Bigramas')
        plt.ylabel('Frecuencia')
        plt.title(f'Top {top_n} Bigramas más Frecuentes')
        plt.show()
        return plt
    def cluster_seleccion_componenteconexa_gigante(G, path_conexo_gigante,path_cluster):
        # Calcular la componente conexa gigante
        G_gigante = G.connected_components().giant()
        layout = G_gigante.layout("fr")
        # calcular la suma de los pesos de las aristas para cada nodo
        sum_pesos_aristas = G_gigante.strength(weights='weight')
        # Normalizar la suma de los pesos de las aristas para ajustarla al rango de tamaños de los nodos
        max_sum_pesos_aristas = max(sum_pesos_aristas)
        sizes = [x / max_sum_pesos_aristas * 40 for x in sum_pesos_aristas]  # Ajusta el rango de tamaño deseado
        G_gigante.vs["size"] = sizes
        ig.plot(G_gigante,path_conexo_gigante, layout=layout, bbox=(700, 700), margin=50,vertex_size=3,vertex_label_size=15,vertex_label_dist=2,edge_arrow_size=0.5,edge_width=0.5,vertex_label=G_gigante.vs['name'],vertex_color='lightblue',edge_color='gray')

        # Calcular la dendrograma de la comunidad
        dendrogram = G_gigante.community_edge_betweenness()

        # Obtener las comunidades finales
        communities = dendrogram.as_clustering()

        # Obtener el número de comunidades
        num_communities = len(communities)

        # Asignar colores a cada comunidad
        palette = ig.RainbowPalette(n=num_communities)
        community_colors = [palette.get(i) for i in communities.membership]

        # Definir transparencia para los nodos
        node_transparency = 0.5  # Valor entre 0 y 1, donde 0 es completamente transparente y 1 es completamente opaco

        # Convertir los colores de las comunidades a RGBA con la transparencia deseada
        community_colors_with_alpha = [color[:-1] + (node_transparency,) for color in community_colors]

        # Dibujar el grafo con nodos semi-transparentes
        ig.plot(G_gigante,path_cluster, layout=layout,vertex_color=community_colors_with_alpha)

        
        for community_id in range(num_communities):
            # Obtener los nodos de la comunidad actual
            community_nodes = [node for node, membership in enumerate(communities.membership) if membership == community_id]
            
            # Calcular el grado de cada nodo en la comunidad
            node_degrees = [G_gigante.degree(node) for node in community_nodes]
            
            # Encontrar el nodo con el mayor grado
            node_with_max_degree_index = node_degrees.index(max(node_degrees))
            node_with_max_degree = community_nodes[node_with_max_degree_index]
            
            # Obtener la palabra asociada al nodo con el mayor grado
            most_connected_word = G_gigante.vs[node_with_max_degree]['name']
            
            # Imprimir la palabra más importante de la comunidad actual
            print(f"Comunidad {community_id}: Palabra más importante (según grado): {most_connected_word}")
        return G_gigante
    def estadisticas_descriptivas(G):
        # Calculate centrality measures and add them as vertex attributes
        G.vs["closeness"] = G.closeness()
        G.vs["betweenness"] = G.betweenness()
        G.vs["eigen"] = G.eigenvector_centrality()
        strengths = G.strength(weights='weight')
        max_strength = max(strengths)
        max_strength_node_index = strengths.index(max_strength)
        
        return {
            # Caracterizar vertices del grafo
            # Diametro del grafo
            'diametro': G.diameter(),
            # Nodo de mayor grado
            'nodo_mayor_grado': G.vs.select(_degree=G.maxdegree())['name'],
            # mayor grado:
            'grado_mayor': G.maxdegree(),
            # nodo de mayor fuerza:
            'nodo_mayor_fuerza': G.vs[max_strength_node_index]['name'],
            # mayor fuerza:
            'fuerza_mayor': max_strength,
            # Nodo con mayor centralidad closeness
            'nodo_centralidad_closeness': G.vs.select(closeness=max(G.vs["closeness"]))[0]['name'],
            # Nodo con mayor centralidad betweenness
            'nodo_centralidad_betweenness': G.vs.select(betweenness=max(G.vs["betweenness"]))[0]['name'],
            # Nodo con mayor centralidad propia
            'nodo_centralidad_eigen': G.vs.select(eigen=max(G.vs["eigen"]))[0]['name'],
            # Caracterizar conectividad del grafo
            # Grado promedio
            'grado_promedio': sum(G.degree()) / len(G.degree()),
            # Clan mas grande
            'clan_mas_grande': len(G.largest_cliques()[0]),
            # Densidad de la red
            'densidad': G.density(),
        }

        