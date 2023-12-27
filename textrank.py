# import module
from module import *

# draw image network
def mat_adjency(similarity):
    G=nx.from_numpy_array(G)
    layout = nx.spring_layout(G)
    nx.draw(G, layout)
    nx.draw_networkx_edge_labels(G, pos=layout)

# mengitung matrik adjence
def res_graph_adjencey(similarity): 
    nx_graph=nx.from_scipy_sparse_array(similarity)
    return nx_graph

# perhitungan pagerank
def _pagerank_scipy(
    G,
    alpha=0.85,
    personalization=None,
    max_iter=100,
    tol=1.0e-6,
    nstart=None,
    weight="weight",
    dangling=None,
):

    N = len(G)
    if N == 0:
        return {}

    nodelist = list(G)
    A = nx.to_scipy_sparse_array(G, nodelist=nodelist, weight=weight, dtype=float)
    S = A.sum(axis=1)
    S[S != 0] = 1.0 / S[S != 0]
    # TODO: csr_array
    Q = sp.sparse.csr_array(sp.sparse.spdiags(S.T, 0, *A.shape))
    A = Q @ A

    # initial vector
    if nstart is None:
        x = np.repeat(1.0 / N, N)
    else:
        x = np.array([nstart.get(n, 0) for n in nodelist], dtype=float)
        x /= x.sum()

    # Personalisasi vektor
    if personalization is None:
        p = np.repeat(1.0 / N, N)
    else:
        p = np.array([personalization.get(n, 0) for n in nodelist], dtype=float)
        if p.sum() == 0:
            raise ZeroDivisionError
        p /= p.sum()
    # Dangling nodes
    if dangling is None:
        dangling_weights = p
    else:
        # konversi kamus dangling ke dalam array dalam urutan node list 
        dangling_weights = np.array([dangling.get(n, 0) for n in nodelist], dtype=float)
        dangling_weights /= dangling_weights.sum()
    is_dangling = np.where(S == 0)[0]

    # power iterasi : membuat sampai iterasi max_iter
    for _ in range(max_iter):
        xlast = x
        x = alpha * (x @ A + sum(x[is_dangling]) * dangling_weights) + (1 - alpha) * p # Perhitungan Pagerank 
        # cek konvergen, l1 norm
        err = np.absolute(x - xlast).sum() 
        if err < N * tol:
            return dict(zip(nodelist, map(float, x)))
    raise nx.PowerIterationFailedConvergence(max_iter)

# fungsi perhitungan pagerank
def pagerank(
    G, 
    alpha=0.85,
    personalization=None,
    max_iter=100,
    tol=1.0e-6,
    nstart=None,
    weight="weight",
    dangling=None,
):
    # Mengembalikan nilai pagerank dalam dictionary
    return _pagerank_scipy(
        G, alpha, personalization, max_iter, tol, nstart, weight, dangling
    )

# mengurutkan kalimat dengan urutan nilai bobot tertinggi ke nilai bobot terendah
def sorted_sentences(pageranks, sentences): 
    sentence_array = sorted(((pageranks[i], s) for i, s in enumerate(sentences)), reverse=True) 
    sentence_array = np.asarray(sentence_array)

    return sentence_array 

# get summary with top_n
def summarytopn(sentence_array,top_n):
    summary_text=[]

    for i in range(top_n):
        summary_text.append(sentence_array[i][1])

    return " ".join(summary_text)