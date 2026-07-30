from identifier import find_similar_artworks

results = find_similar_artworks(
    r"D:\ArtMuse\data\imagesss\435621.jpg",
    top_k=5
)

for art in results:

    print("---------------------------")
    print(art["name"])
    print(art["artist"])
    print(art["similarity"])
