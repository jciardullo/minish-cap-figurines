// Full count/shell/rupee/route-state SSP. See corrected README for the input format.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <queue>
#include <string>
#include <vector>
#include <filesystem>
#include <sstream>
#include <unistd.h>
using namespace std;
constexpr int NS=1000,NR=400,N=NS*NR;
constexpr double INF=1e100;
int cash(int r){return 5*(r/2)+(r%2?4:0);}
int indexr(int r){return 2*(r/5)+(r%5==4);}
int basechance(int f,int u){return max(1,100*(u-f)/u);}
int hidden(int f){return f<50?15:f<80?12:f<110?9:6;}
struct Phase{int u,wallet;vector<int> pickups;bool entryfarm=false,canfarm=true;};
struct Solver{
 int f,u,wallet,price,phase,maxbundles=3;bool ntsc,finalphase,canfarm=true;string mode;
 int threshold=27;double tolerance=1e-6,pullbase=20,inputrate=15,farmrate=300;
 vector<double> v,c,weight,restock;vector<int> to,color,path;
 vector<uint16_t> action;vector<uint8_t> farmcount;
 array<array<uint8_t,101>,101> inputcount{};
 array<double,101> p{};
 const double *next,*advance;
 Solver():v(N),c(N),weight(N),restock(4*N),to(N),color(N),action(N),farmcount(4*N){}
 double pulltime(int s,int wager){return pullbase+(ntsc?inputcount[min(s,101-basechance(f,u))][wager]:wager-1)/inputrate;}
 void prepare(){
  for(int a=1;a<=100;a++)p[a]=max(hidden(f),min(100,basechance(f,u)+a-1))/100.;
  for(int limit=1;limit<=100;limit++){
   auto &d=inputcount[limit];d.fill(255);d[1]=0;queue<int> q;q.push(1);
   while(!q.empty()){int x=q.front();q.pop();for(int delta:{-10,-1,1,10}){int y=clamp(x+delta,1,limit);if(d[y]==255){d[y]=d[x]+1;q.push(y);}}}
  }
 }
 int fixedw(){int b=basechance(f,u);return mode=="one"?1:mode=="guarantee"?101-b:mode=="eighty"?max(1,81-b):b>threshold?1:101-b;}
 uint16_t buy(int q,int n){return 101+(q-1)+maxbundles*n;}
 void graph(){
  for(int s=0;s<NS;s++)for(int r=0;r<NR;r++){
   int i=s*NR+r;auto a=action[i];int rr=cash(r);
   if(rr>wallet){c[i]=INF;weight[i]=0;to[i]=i;continue;}
   if(a==0){c[i]=advance?advance[i]:0;weight[i]=0;to[i]=i;}
   else if(a<=100){int j=(s-a)*NR+r;c[i]=pulltime(s,a)+p[a]*next[j];weight[i]=1-p[a];to[i]=(s-a)*NR+indexr(min(wallet,rr+5));}
   else{int q=(a-101)%maxbundles+1,n=(a-101)/maxbundles;if(n&&!canfarm)throw runtime_error("Farm unavailable");int rf=min(wallet,rr+20*n);c[i]=(n?45:20)+15*q+1200./farmrate*n;weight[i]=1;to[i]=(s+30*q)*NR+indexr(rf-price*q);}
  }
 }
 void evaluate(){
  fill(color.begin(),color.end(),0);
  for(int root=0;root<N;root++){
   if(color[root]==2)continue;
   int x=root;path.clear();
   while(color[x]==0){color[x]=1;path.push_back(x);if(weight[x]==0)break;x=to[x];}
   int cycle=-1;
   if(weight[path.back()]!=0 && color[x]==1){cycle=find(path.begin(),path.end(),x)-path.begin();double prod=1,sum=0;
    for(int k=cycle;k<(int)path.size();k++){sum+=prod*c[path[k]];prod*=weight[path[k]];}
    if(prod>=1-1e-14)throw runtime_error("Improper policy cycle");v[x]=sum/(1-prod);
    for(int k=(int)path.size()-1;k>cycle;k--){int j=path[k];v[j]=c[j]+weight[j]*v[to[j]];}
    for(int k=cycle;k<(int)path.size();k++)color[path[k]]=2;
   }
   for(int k=cycle>=0?cycle-1:(int)path.size()-1;k>=0;k--){int j=path[k];v[j]=c[j]+(weight[j]?weight[j]*v[to[j]]:0);color[j]=2;}
  }
 }
 // Exact discrete-farm suffix envelope: all reachable 20-rupee pickup counts,
 // including farming beyond minimum funding, without a quadratic enumeration.
 void farming_envelope(){
  fill(restock.begin(),restock.end(),INF);
  for(int q=1;q<=maxbundles;q++)if(price*q<=wallet)for(int s=0;s+30*q<NS;s++)for(int r=NR-1;r>=0;r--){
   int rr=cash(r),i=(q-1)*N+s*NR+r;if(rr>wallet)continue;
   double best=rr>=price*q?v[(s+30*q)*NR+indexr(rr-price*q)]:INF;int n=0;
   int rf=min(wallet,rr+20);
   if(canfarm&&rf>rr){int j=(q-1)*N+s*NR+indexr(rf);double value=1200./farmrate+restock[j];if(value<best-1e-10){best=value;n=farmcount[j]+1;}}
   restock[i]=best;farmcount[i]=n;
  }
 }
 double improve(bool mutate){
  farming_envelope();double residual=0;
  for(int s=0;s<NS;s++)for(int r=0;r<NR;r++){
   int i=s*NR+r;if(cash(r)>wallet)continue;double best=v[i];auto a=action[i];
   if(advance && advance[i]<best-1e-10){best=advance[i];a=0;}
   int lo=mode=="optimal"?1:fixedw();int hi=f>=u?0:mode=="optimal"?min(s,101-basechance(f,u)):min(s,lo);
   for(int b=lo;b<=hi;b++){
    double value=pulltime(s,b)+p[b]*next[(s-b)*NR+r]+(1-p[b])*v[(s-b)*NR+indexr(min(wallet,cash(r)+5))];
    if(value<best-1e-10){best=value;a=b;}
   }
   for(int q=1;q<=maxbundles && s+30*q<NS;q++)if(price*q<=wallet){int j=(q-1)*N+i;double value=45+15*q+restock[j];if(value<best-1e-10){best=value;a=buy(q,farmcount[j]);}if(cash(r)>=price*q){double funded=20+15*q+v[(s+30*q)*NR+indexr(cash(r)-price*q)];if(funded<best-1e-10){best=funded;a=buy(q,0);}}}
   residual=max(residual,v[i]-best);if(mutate)action[i]=a;
  }
  return residual;
 }
 string tied(int s,int r){
  int i=s*NR+r; vector<pair<uint16_t,double>> candidates;
  if(advance)candidates.push_back({0,advance[i]});
  int lo=mode=="optimal"?1:fixedw(),hi=f>=u?0:mode=="optimal"?min(s,101-basechance(f,u)):min(s,lo);
  for(int a=lo;a<=hi;a++)candidates.push_back({(uint16_t)a,pulltime(s,a)+p[a]*next[(s-a)*NR+r]+(1-p[a])*v[(s-a)*NR+indexr(min(wallet,cash(r)+5))]});
  for(int q=1;q<=maxbundles&&s+30*q<NS;q++)if(price*q<=wallet)for(int n=0;;n++){
   int rr=min(wallet,cash(r)+20*n);
   if(rr>=price*q)candidates.push_back({buy(q,n),(n?45:20)+15*q+1200./farmrate*n+v[(s+30*q)*NR+indexr(rr-price*q)]});
   if(rr==wallet||!canfarm)break;
  }
  double best=INF;for(auto x:candidates)best=min(best,x.second);string out;
  for(auto x:candidates)if(abs(x.second-best)<=tolerance){if(!out.empty())out+=";";out+=to_string(x.first);}return out;
 }
 vector<uint16_t> warm;
 double solve(){
  prepare();
  for(int s=0;s<NS;s++)for(int r=0;r<NR;r++){
   if(advance || cash(r)>wallet)action[s*NR+r]=0;
   else if(s>0 && (mode=="optimal" || s>=fixedw()))action[s*NR+r]=mode=="optimal"?1:fixedw();
   else action[s*NR+r]=buy(1,max(0,(price-cash(r)+19)/20));
  }
  if(warm.size()==N)action=warm;
  if(!canfarm)for(auto &a:action)if(a>100&&(a-101)/maxbundles>0){if(!advance)throw runtime_error("No farming terminal requires feasible resources");a=0;}
  double residual;int iteration=0;
  do{graph();evaluate();residual=improve(true);if(++iteration>2000)throw runtime_error("No convergence");}while(residual>tolerance);
  graph();evaluate();residual=improve(false);if(residual>tolerance)throw runtime_error("Residual too high");
  cerr<<phase<<","<<f<<","<<iteration<<","<<residual<<"\n";return residual;
 }
};
// One discounted cycle at an actual farm entry; later decisions begin at Carlov.
void apply_farm_entry(Solver& l,vector<double>& values,const string& prefix,int phase,bool emit){
 ofstream entry;if(emit)entry.open(prefix+"_phase"+to_string(phase)+".entry",ios::binary);
 for(int f=0;f<=min(135,l.u);f++){
  copy(values.begin()+(int64_t)f*N,values.begin()+(int64_t)(f+1)*N,l.v.begin());l.farming_envelope();
  for(int s=0;s<NS;s++)for(int r=0;r<NR;r++){int i=s*NR+r;l.action[i]=0;double best=l.v[i];if(cash(r)>l.wallet)continue;
   for(int q=1;q<=l.maxbundles&&s+30*q<NS;q++)if(q*l.price<=l.wallet){int j=(q-1)*N+i;double candidate=25+15*q+l.restock[j];if(candidate<best-1e-10){best=candidate;l.action[i]=l.buy(q,l.farmcount[j]);}}
   values[(int64_t)f*N+i]=best;
  }
  if(emit)entry.write((char*)l.action.data(),N*2);
 }
}
int main(int argc,char **argv){try{
 if(argc<5)throw runtime_error("Usage: full_solver ROUTE_TEXT PREFIX PAL|NTSC-U MODE [threshold] [tolerance] [pullbase] [farmrate] [inputrate]");
 bool emitpolicy=argc<=10||string(argv[10])!="0";string prefix=argv[2];string warmprefix=argc>11?argv[11]:"";vector<Phase> route;ifstream in(argv[1]);int u,w,k;
 while(in>>u>>w>>k){Phase p{u,w,{}};for(int j=0,x;j<k;j++){in>>x;p.pickups.push_back(x);}string tail;getline(in,tail);istringstream extra(tail);int atfarm=0;if(extra>>atfarm){if(atfarm!=0&&atfarm!=1)throw runtime_error("Invalid farm-entry flag");p.entryfarm=atfarm;}int available=1;if(extra>>available)p.canfarm=available;route.push_back(p);}
 if(route.empty()||route.back().u!=136)throw runtime_error("Bad route");
 Solver l;l.ntsc=string(argv[3])=="NTSC-U";l.price=l.ntsc?200:300;l.maxbundles=l.ntsc?4:3;l.mode=argv[4];
 if(argc>5)l.threshold=stoi(argv[5]);if(argc>6)l.tolerance=stod(argv[6]);if(argc>7)l.pullbase=stod(argv[7]);if(argc>8)l.farmrate=stod(argv[8]);if(argc>9)l.inputrate=stod(argv[9]);
 vector<double> following((int64_t)137*N,INF),current(following.size(),INF),boundary(N),next(N);
 fill(following.begin()+136LL*N,following.end(),0);
 ofstream summary(prefix+"_values.csv");summary<<setprecision(15)<<"phase,owned,shells,rupees,seconds,action,tied_actions\n";
 double maxres=0;ostringstream ck;ck<<setprecision(17)<<"funded20-v1 "<<l.ntsc<<" "<<l.mode<<" "<<l.threshold<<" "<<l.tolerance<<" "<<l.pullbase<<" "<<l.farmrate<<" "<<l.inputrate;string cachekey=ck.str();uint64_t hash=1469598103934665603ULL;for(unsigned char ch:cachekey){hash^=ch;hash*=1099511628211ULL;}string cache=(filesystem::path(prefix).parent_path()/"postgame_cache"/to_string(hash)).string();filesystem::create_directories(filesystem::path(cache).parent_path());
 for(int phase=(int)route.size()-1;phase>=0;phase--){
  l.phase=phase;l.u=route[phase].u;l.wallet=route[phase].wallet;l.canfarm=route[phase].canfarm;bool last=phase==(int)route.size()-1;
  fill(current.begin(),current.end(),INF);fill(current.begin()+136LL*N,current.end(),0);fill(next.begin(),next.end(),0);
  if(last&&l.u==136&&l.wallet==999&&l.canfarm){ifstream meta(cache+".meta");string key;double residual=0;if(meta&&getline(meta,key)&&key==cachekey&&(meta>>residual)){ifstream vals(cache+".values",ios::binary);vals.read((char*)current.data(),current.size()*sizeof(double));if(!vals)throw runtime_error("Truncated exact cache");if(emitpolicy)filesystem::copy_file(cache+".policy",prefix+"_phase"+to_string(phase)+".policy",filesystem::copy_options::overwrite_existing);ifstream rows(cache+".rows");string row;while(getline(rows,row))summary<<phase<<row.substr(row.find(','))<<"\n";maxres=max(maxres,residual);if(route[phase].entryfarm)apply_farm_entry(l,current,prefix,phase,emitpolicy);swap(following,current);continue;}}
  ifstream warmfile;if(!warmprefix.empty()&&l.mode=="optimal")warmfile.open(warmprefix+"_phase"+to_string(phase)+".policy",ios::binary);ofstream policy;if(emitpolicy)policy.open(prefix+"_phase"+to_string(phase)+".policy",ios::binary);
  for(int f=min(135,l.u);f>=0;f--){l.f=f;l.next=next.data();
   if(!last){for(int s=0;s<NS;s++)for(int r=0;r<NR;r++){int ss=s;for(int q:route[phase+1].pickups)ss=min(999,ss+q);boundary[s*NR+r]=following[(int64_t)f*N+ss*NR+r];}l.advance=boundary.data();}else l.advance=nullptr;
   l.warm.clear();if(warmfile.is_open()){l.warm.resize(N);warmfile.seekg((int64_t)f*N*2);warmfile.read((char*)l.warm.data(),N*2);if(!warmfile)throw runtime_error("Warm policy truncated");}maxres=max(maxres,l.solve());if(emitpolicy){policy.seekp((int64_t)f*N*2);policy.write((char*)l.action.data(),N*2);}
   copy(l.v.begin(),l.v.end(),current.begin()+(int64_t)f*N);
   for(int s:{0,30,100,500,800,900,999})for(int r:{0,50,300})if(r<=l.wallet){int i=s*NR+indexr(r);summary<<phase<<","<<f<<","<<s<<","<<r<<","<<l.v[i]<<","<<l.action[i]<<","<<l.tied(s,indexr(r))<<"\n";}
   swap(next,l.v);
  }
  if(last&&l.u==136&&l.wallet==999&&l.canfarm&&emitpolicy){policy.close();summary.flush();string temp=cache+".tmp"+to_string(getpid());ofstream vals(temp+".values",ios::binary);vals.write((char*)current.data(),current.size()*sizeof(double));vals.close();filesystem::copy_file(prefix+"_phase"+to_string(phase)+".policy",temp+".policy",filesystem::copy_options::overwrite_existing);ifstream rowsin(prefix+"_values.csv");string heading;getline(rowsin,heading);ofstream rows(temp+".rows");rows<<rowsin.rdbuf();rows.close();ofstream meta(temp+".meta");meta<<cachekey<<"\n"<<setprecision(17)<<maxres<<"\n";meta.close();for(string ext:{".values",".policy",".rows",".meta"})filesystem::rename(temp+ext,cache+ext);}
  if(route[phase].entryfarm)apply_farm_entry(l,current,prefix,phase,emitpolicy);
  swap(following,current);
 }
 int s=0;for(int q:route[0].pickups)s=min(999,s+q);
 ofstream result(prefix+".json");result<<setprecision(15)<<"{\"expected_seconds\":"<<following[s*NR]<<",\"max_residual_seconds\":"<<maxres<<",\"threshold\":"<<l.threshold<<",\"price\":"<<l.price<<",\"max_bundles\":"<<l.maxbundles<<",\"tolerance_seconds\":"<<l.tolerance<<",\"pull_base_seconds\":"<<l.pullbase<<",\"farming_rupees_per_minute\":"<<l.farmrate<<",\"entry_inputs_per_second\":"<<l.inputrate<<"}\n";
 cout<<setprecision(15)<<following[s*NR]<<"\n";return 0;
 }catch(exception &e){cerr<<e.what()<<"\n";return 1;}}
