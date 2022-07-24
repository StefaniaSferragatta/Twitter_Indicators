import itertools

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