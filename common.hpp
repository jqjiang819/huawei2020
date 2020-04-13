#include <cstdio>
#include <algorithm>
#include <sstream>
#include <cstring>
#include <string>
#include <vector>
#include <map>
#include <set>


using namespace std;

typedef uint32_t Node;
typedef map<Node, set<Node>> Graph;
typedef vector<Node> Path;
typedef map<int, vector<string>> Cycles;


string vec2str(Path&);
void judge(string, string);
void load_data(string, Graph&);
void save_result(string, Cycles&);


string vec2str(Path& pvec) {
    stringstream ss;
    for_each(pvec.begin(), pvec.end(), 
             [&ss, sep=""](uint32_t n) mutable {ss<<sep<<n;sep=",";});
    return ss.str();
}


void judge(string path_0, string path_1) {
    FILE *fp0 = NULL, *fp1 = NULL;
    char tmp0[100], tmp1[100];
    
    fp0 = fopen(path_0.c_str(), "r");
    fp1 = fopen(path_1.c_str(), "r");

    if (fp0 == NULL) {
        fprintf(stderr, "file: %s open error", path_0.c_str());
        exit(-1);
    }

    if (fp1 == NULL) {
        fprintf(stderr, "file: %s open error", path_1.c_str());
        exit(-1);
    }

    while (fgets(tmp0, 100, fp0) != NULL && fgets(tmp1, 100, fp1) != NULL) {
        if (strcmp(tmp0, tmp1) != 0) {
            printf("results check: False\n");
            return;
        }
    }

    if (fgets(tmp0, 100, fp0) != NULL || fgets(tmp1, 100, fp1) != NULL) {
        printf("results check: False\n");
        return;
    }

    fclose(fp0);
    fclose(fp1);

    printf("results check: True\n");
}

void load_data(string path, Graph& graph) {
    FILE *fp = NULL;
    Node fr, to, am;

    fp = fopen(path.c_str(), "r");

    if (fp == NULL) {
        fprintf(stderr, "file: %s open error", path.c_str());
        exit(-1);
    }

    while (fscanf(fp, "%u,%u,%u", &fr, &to, &am) == 3) {
        graph[fr].insert(to);
    }

    fclose(fp);

    printf("found %d nodes in graph\n", graph.size());
}

void save_result(string path, Cycles& cycles) {
    FILE *fp = NULL;
    stringstream ss;
    int count = 0;

    fp = fopen(path.c_str(), "w");

    if (fp == NULL) {
        fprintf(stderr, "file: %s open error", path.c_str());
        exit(-1);
    }

    for (const auto& [len, len_cycles] : cycles) {
        count += len_cycles.size();
        for_each(len_cycles.begin(), len_cycles.end(), 
                 [&ss](string s) mutable {ss<<s<<endl;});
    }
    fprintf(fp, "%d\n%s", count, ss.str().c_str());

    fclose(fp);

    printf("found %d cycles in graph\n", count);

}