// Uniform-phase sampling on the verified boot-seed orbit; not a full-playthrough distribution.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>
int main(int argc,char**argv){if(argc!=2)return 1;constexpr uint64_t period=822119800;constexpr int count=200000;std::mt19937_64 rng(20261019);std::uniform_int_distribution<uint64_t> phase(0,period-1);std::vector<std::pair<uint64_t,int>> selected;for(int i=0;i<count;i++)selected.push_back({phase(rng),i});std::sort(selected.begin(),selected.end());std::vector<uint32_t> states(count);uint32_t state=0x1234567;size_t k=0;for(uint64_t n=0;n<period;n++){while(k<selected.size()&&selected[k].first==n){states[selected[k].second]=state;k++;}state*=3;state=(state>>13)|(state<<19);}if(state!=0x1234567||k!=count)return 2;std::ofstream out(argv[1]);for(auto x:states)out<<x<<"\n";std::cout<<"Uniform boot-orbit phases generated with seed 20261019.\n";}
