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
void find_cycle_path(Graph&, Path&, Cycles&, int);


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

    for (int l = min_len; l <= max_len; l++) {
        cout<<"processing length "<<l;
        clock_t start = clock();
        for (auto const& n : g) {
            path = {n.first};
            find_cycle_path(g, path, cycles, l);
        }
        cout<<"\tfinished in "<<(clock() - start)*1000/CLOCKS_PER_SEC<<" ms"<<endl;
    }
}


void find_cycle_path(Graph& g, Path& p, Cycles& results, int len) {
    int p_len = p.size();
    uint32_t p_node = p.back();

    if (g.find(p_node) == g.end()) {
        return;
    }

    if (p_len == len - 1) {
        for (const auto& n_node : g[p_node]) {
            if (n_node < p.front() || find(p.begin(), p.end(), n_node) != p.end()) {
                continue;
            }
            p.push_back(n_node);
            if (g.find(n_node) != g.end() && g[n_node].find(p.front()) != g[n_node].end()) {
                results[len].push_back(vec2str(p));
            }
            p.pop_back();
        }
    } else {
        for (const auto& n_node : g[p_node]) {
            if (n_node < p.front() || find(p.begin(), p.end(), n_node) != p.end()) {
                continue;
            }
            p.push_back(n_node);
            find_cycle_path(g, p, results, len);
            p.pop_back();
        }
    }
}
