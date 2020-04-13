#include <iostream>
#include <sstream>
#include <algorithm>
#include <string>
#include <map>
#include <vector>
#include <set>
#include <time.h>
#include "common.hpp"

#define DATA_PATH "data/54/test_data.txt"
#define RES_PATH "data/54/result.txt"
#define OUT_PATH "output/results.txt"

using namespace std;


void find_cycles(Graph&, int, int, Cycles&);
void dfs_step(Graph&, Path&, Cycles&, Node, int, int);

int main(int argc, char* argv[]) {

    Graph graph;
    Cycles cycles;
    
    clock_t start = clock();
    load_data(DATA_PATH, graph);
    cout<<"load data finished in "<<(clock() - start)*1000/CLOCKS_PER_SEC<<" ms"<<endl;
    find_cycles(graph, 3, 7, cycles);
    save_result(OUT_PATH, cycles);
    cout<<"all finished in "<<(clock() - start)*1000/CLOCKS_PER_SEC<<" ms"<<endl;
    judge(OUT_PATH, RES_PATH);
    return 0;
}

void find_cycles(Graph& g, int min_len, int max_len, Cycles& cycles) {
    Path path;

    for (auto const& n : g) {
        dfs_step(g, path, cycles, n.first, min_len, max_len);
    }
}

void dfs_step(Graph& g, Path& p, Cycles& c, Node n, int lmin, int lmax) {
    p.push_back(n);
    for (const auto& ch : g[n]) {
        if (ch == p[0]) {
            if (p.size() >= lmin) c[p.size()].push_back(vec2str(p));
        } else if (ch < p[0] || find(p.begin(), p.end(), ch) != p.end()) {
            continue;
        } else if (p.size() < lmax) {
            dfs_step(g, p, c, ch, lmin, lmax);
        }
    }
    p.pop_back();
}