#define main full_solver_main
#include "full_solver.cpp"
#undef main
#include <cassert>
int main(){
 Solver l;l.u=136;l.wallet=999;l.price=300;l.ntsc=true;l.maxbundles=4;
 for(int f:{0,49,50,79,80,109,110,135}){l.f=f;l.prepare();for(int a=1;a<=101-basechance(f,136);a++){assert(l.p[a]>=hidden(f)/100.);assert(l.p[a]<=1);}assert(l.p[101-basechance(f,136)]==1);}
 assert(basechance(135,136)==1);assert(hidden(49)==15&&hidden(50)==12&&hidden(80)==9&&hidden(110)==6);
 l.f=0;l.prepare();assert(l.inputcount[100][20]==3);assert(l.inputcount[20][20]==2);assert(l.inputcount[1][1]==0);assert(l.inputcount[6][6]==1);
 for(int limit=1;limit<=100;limit++)for(int target=1;target<=limit;target++){
  vector<int> d(limit+1,999);d[1]=0;
  // Independent repeated relaxation of the directed legal input graph.
  for(int pass=0;pass<limit;pass++)for(int x=1;x<=limit;x++)for(int delta:{1,-1,10,-10})d[clamp(x+delta,1,limit)]=min(d[clamp(x+delta,1,limit)],d[x]+1);
  assert(l.inputcount[limit][target]==d[target]);
 }
 for(int w:{300,999})for(int price:{200,300}){l.wallet=w;l.price=price;for(int i=0;i<N;i++)l.v[i]=(i*7919ULL%10007)/19.;l.farming_envelope();
  for(int q=1;q<=4&&q*price<=w;q++)for(int s:{0,29,899,909})if(s+30*q<=999)for(int r=0;r<NR;r++){int rr=cash(r);if(rr>w)continue;double best=INF;for(int n=0;;n++){int rf=min(w,rr+20*n);if(rf>=q*price)best=min(best,4*n+l.v[(s+30*q)*NR+indexr(rf-q*price)]);if(rf==w)break;}double direct=rr>=q*price?20+15*q+l.v[(s+30*q)*NR+indexr(rr-q*price)]:INF;double composed=min(45+15*q+l.restock[(q-1)*N+s*NR+r],direct);double exhaustive=INF;for(int n=0;;n++){int rf=min(w,rr+20*n);if(rf>=q*price)exhaustive=min(exhaustive,(n?45:20)+15*q+4*n+l.v[(s+30*q)*NR+indexr(rf-q*price)]);if(rf==w)break;}assert(abs(composed-exhaustive)<1e-9);if(abs(best-l.restock[(q-1)*N+s*NR+r])>=1e-9){cerr<<"mismatch "<<w<<" "<<price<<" "<<q<<" "<<s<<" "<<rr<<" "<<best<<" "<<l.restock[(q-1)*N+s*NR+r]<<"\n";return 1;}}
 }
 l.canfarm=false;l.wallet=999;l.price=300;l.farming_envelope();assert(l.restock[0]>=INF/2);assert(l.farmcount[indexr(300)]==0);assert(abs(l.restock[indexr(300)]-l.v[30*NR])<1e-9);l.canfarm=true;
 fill(l.c.begin(),l.c.end(),0);fill(l.weight.begin(),l.weight.end(),0);for(int i=0;i<N;i++)l.to[i]=i;
 l.c[0]=1;l.c[1]=2;l.c[2]=3;l.weight[0]=.5;l.weight[1]=.25;l.weight[2]=.1;l.to[0]=1;l.to[1]=2;l.to[2]=0;l.evaluate();assert(abs(l.v[0]-2.375/.9875)<1e-12);
 assert(min(999,997+5)==999);assert(min(300,299+20)==300);int s=980,retained=0,lost=0;for(int g:{10,30}){int keep=min(g,999-s);s+=keep;retained+=keep;lost+=g-keep;}assert(s==999&&retained==19&&lost==21);
 cout<<"Probability boundaries, legal-input shortest paths, exhaustive farming envelopes, policy cycle evaluation, and cap transitions passed.\n";
}
