#define main full_solver_main
#include "full_solver.cpp"
#undef main
int main(int argc,char**argv){try{
 if(argc!=3)throw runtime_error("diagnose_tolerance BASE_PHASE8_POLICY OUTPUT_CSV");Solver l;l.u=136;l.wallet=999;l.price=300;l.ntsc=false;l.phase=8;l.mode="optimal";l.tolerance=1e-7;l.advance=nullptr;vector<double> next(N),tight(N);vector<uint16_t> selected(N),old(N);ifstream base(argv[1],ios::binary);ofstream out(argv[2]);out<<setprecision(15)<<"owned,changed_states,max_old_action_bellman_gap,max_old_layer_value_gap\n";
 for(int f=135;f>=0;f--){l.f=f;l.next=next.data();l.solve();tight=l.v;selected=l.action;base.seekg((int64_t)f*N*2);base.read((char*)old.data(),N*2);if(!base)throw runtime_error("policy read");l.action=old;l.graph();double qgap=0;int changes=0;for(int i=0;i<N;i++){if(old[i]!=selected[i])changes++;qgap=max(qgap,l.c[i]+(l.weight[i]?l.weight[i]*tight[l.to[i]]:0)-tight[i]);}l.evaluate();double vgap=0;for(int i=0;i<N;i++)vgap=max(vgap,l.v[i]-tight[i]);out<<f<<","<<changes<<","<<qgap<<","<<vgap<<"\n";l.v=tight;l.action=selected;next=tight;}
 return 0;
 }catch(exception&e){cerr<<e.what()<<"\n";return 1;}}
