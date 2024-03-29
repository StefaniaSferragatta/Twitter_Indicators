import itertools
import networkx as nx


def add_edges_to_graph(df1_aggr,G):
    for row in df1_aggr['hashtag']:
        if type(row) == str or str(row[0]) == 'nan':
            ...
        else:
            for x in itertools.combinations(row, 2):

                if not G.has_edge(x[0], x[1]):
                    G.add_edge(x[0], x[1])
                    #   print('first if: ', x)
                    G[x[0]][x[1]]['weight'] = 1
                else:

                    G[x[0]][x[1]]['weight'] += 1
    return 


# REMOVE FROM THE GRAPH THE LESS CONNECTED COMUNITIES 
def less_connected_comunities(G,threshold = 5):
    long_edges = list(filter(lambda e: e[2] < threshold, (e for e in G.edges.data('weight'))))
    le_ids = list(e[:2] for e in long_edges)

    # remove filtered edges from graph G
    G.remove_edges_from(le_ids)
    G.remove_nodes_from(list(nx.isolates(G)))


def given_hashtag_return_community(hashtags, communities):
    for hashtag in set(hashtags):
        for community in communities:
            if hashtag in community:
                return communities.index(community)


def create_labels_matrix(df1_lemmatized, df1_aggr, communities):
    #Initialize the labels matrix
    labels = [[] for x in range(0, len(df1_lemmatized))]
    for id, row in df1_aggr.iterrows():
        community_index = given_hashtag_return_community(row['hashtag'], communities=communities)
        if community_index:
            labels[id].append(community_index)
    return labels