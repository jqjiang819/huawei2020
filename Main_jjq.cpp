#include <iostream>
#include <sstream>
#include <algorithm>
#include <string>
#include <map>
#include <vector>
#include <set>
#include <time.h>
#include "common.hpp"

#define DATA_PATH "data/1004812/test_data.txt"
#define RES_PATH "data/1004812/result.txt"
#define OUT_PATH "output/results.txt"

using namespace std;

typedef map<Node, Node> Cache;

void find_cycles(Graph&, Graph&, int, int, Cycles&);
void dfs_step(Graph&, Path&, Cycles&, Cache&, Node, int, int);
void prune(Graph&, Cache&, Node, Node, int);

int main(int argc, char* argv[]) {

    Graph graph, graph_r;
    Cycles cycles;
    
    clock_t start = clock();
    load_data(DATA_PATH, graph, graph_r);
    cout<<"load data finished in "<<(clock() - start)*1000/CLOCKS_PER_SEC<<" ms"<<endl;
    find_cycles(graph, graph_r, 3, 7, cycles);
    save_result(OUT_PATH, cycles);
    cout<<"all finished in "<<(clock() - start)*1000/CLOCKS_PER_SEC<<" ms"<<endl;
    judge(OUT_PATH, RES_PATH);
    return 0;
}

void find_cycles(Graph& g, Graph& g_r, int min_len, int max_len, Cycles& cycles) {
    Path path;
    Cache cache;

    for (auto const& n : g) {
        prune(g, cache, n.first, n.first, 0);
        prune(g_r, cache, n.first, n.first, 0);
        dfs_step(g, path, cycles, cache, n.first, min_len, max_len);
    }
}

void dfs_step(Graph& g, Path& p, Cycles& c, Cache& ca, Node n, int lmin, int lmax) {
    p.push_back(n);
    for (const auto& ch : g[n]) {
        if (ch == p[0]) {
            if (p.size() >= lmin) c[p.size()].push_back(vec2str(p));
            continue;
        } 
        if (ch < p[0] || find(p.begin(), p.end(), ch) != p.end()) {
            continue;
        }
        if (ca[ch] != p[0]) continue;
        if (p.size() < lmax) {
            dfs_step(g, p, c, ca, ch, lmin, lmax);
        }
    }
    p.pop_back();
}


void prune(Graph& g, Cache& c, Node n, Node s, int depth) {
    depth++;
    for (const auto& ch : g[n]) {
        if (ch < s) continue;
        c[ch] = s;
        if (depth < 3) {
            prune(g, c, ch, s, depth);
        }
    }
    depth--;
}