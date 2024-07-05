class DisjointSet:
    #Bu sınıf, ayrık küme veri yapısını temsil eder. 
    def __init__(self, nodes):
        ## Her düğümü kendi alt kümesine atar, başlangıçta her düğümün rank'ı 0'dır.
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        #node düğümü kendi alt kümesinin temsilcisi değilse o zaman if bloğu içine girilir find işlemi devam eder
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        #İki alt kümenin temsilcilerini (root'larını) bulmak, bu temsilcileri birleştirme
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            #İki düğüm aynı alt kümede değilse birleştirme işlemi gerçekleştirilir
            if self.rank[root1] > self.rank[root2]:
                #Eğer root1 alt kümesinin derinliği (rank) daha büyükse, root2'yi root1'e bağlar.
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

def kruskal(graph):
    #her düğüm ve o düğüme bağlı kenarların ağırlıklarını içeren bir liste oluşturur.
    edges = [(weight, node1, node2) for node1, node_list in graph.items() for node2, weight in node_list]
    #Oluşturulan edges listesini ağırlıklarına göre küçükten büyüğe doğru sıralar
    edges.sort()
    #grafın tüm düğümlerini içeren bir küme oluşturur.
    nodes = set(node for node_list in graph.values() for node, _ in node_list)
    #Oluşturulan düğüm kümesi, DisjointSet sınıfından bir nesne oluşturmak için kullanılır.
    disjoint_set = DisjointSet(nodes)
    #oluşturulan ağacın kenarlarını ve ağırlıklarını içerir
    minimum_spanning_tree = []

    for edge in edges:
        weight, node1, node2 = edge
        # node1 ve node2 aynı alt kümede değillerse , bu kenarın eklenmesi gerektiği kontrol edilir.
        if disjoint_set.find(node1) != disjoint_set.find(node2):
            #bu iki alt küme birleştirilir
            disjoint_set.union(node1, node2)
            minimum_spanning_tree.append((node1, node2, weight))

    return minimum_spanning_tree

def main():
    node_count = int(input("Düğüm sayısını girin: "))
    edge_count = int(input("Kaç farklı yol olduğunu girin: "))

    # Graph'i temsil eden sözlük
    graph = {}

    print("Düğüm arasındaki mesafeleri girin (örnek: a-b:5):")

    for _ in range(edge_count):
        #kullanıcıdan grafın kenarlarını ve ağırlıklarını girmesini bekleyen bir döngüdür
        edge_input = input().strip().split('-')
        node1, node2 = edge_input[0], edge_input[1].split(':')[0]
        weight = int(edge_input[1].split(':')[1])

        # Graph'i güncelle
        # eğer graph sözlüğünde henüz yoklarsa (yani daha önce eklenmemişlerse), onları graph sözlüğüne ekler
        if node1 not in graph:
            graph[node1] = []
        if node2 not in graph:
            graph[node2] = []

        graph[node1].append((node2, weight))
        graph[node2].append((node1, weight))

    # Kruskal algoritması ile minimum kapsayan ağ yolu bul
    minimum_spanning_tree = kruskal(graph)

    # Sonuçları ekrana yazdır
    total_distance = 0
    print("Minimum Kapsayan Ağ Yolu:")
    for edge in minimum_spanning_tree:
        print(f"{edge[0]}-{edge[1]}: {edge[2]}")
        total_distance += edge[2]

    print("Toplam Mesafe:", total_distance)

if __name__ == "__main__":
    main()
