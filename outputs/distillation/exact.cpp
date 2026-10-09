#include "policy.hpp"
#include <cmath>
#include <iomanip>
#include <iostream>
#include <unordered_map>
constexpr int NR=400,N=400000;
int cash(int i){return 5*(i/2)+(i%2?4:0);}int ri(int r){if(r%5!=0&&r%5!=4)throw runtime_error("Unrepresented cash");return 2*(r/5)+(r%5==4);}
struct Phase{int u,w;vector<int>g;bool farm;};
int main(int argc,char**argv){try{if(argc<5)throw runtime_error("exact policy route region output [cash]");auto pol=loadpolicies(argv[1]);if(pol.size()!=1)throw runtime_error("One policy per exact evaluation");auto p=pol[0];ifstream in(argv[2]);vector<Phase>route;int u,w,k;while(in>>u>>w>>k){Phase a{u,w,{}};for(int j=0,x;j<k;j++){in>>x;a.g.push_back(x);}string line;getline(in,line);istringstream tail(line);int loc=0,available=1;tail>>loc>>available;a.farm=available;route.push_back(a);}bool ntsc=string(argv[3])=="NTSC-U";int price=ntsc?200:300,maxB=ntsc?4:3,external=argc>5?stoi(argv[5]):0;auto d=inputcounts();vector<unordered_map<int,double>>incoming(137),following(137);vector<double>flow(N),weight(N);vector<int>actions(N),to(N),indegree(N),order,touched;vector<unsigned char>seen(N);array<double,4>cost{};double used=0,purchased=0,dupes=0,trips=0,retained=0,lost=0,refund=0,refundlost=0,farmrupees=0,endS=0,endR=0,complete=0,external_retained=0;int s0=0;for(int g:route[0].g){int keep=min(g,999-s0);s0+=keep;retained+=keep;lost+=g-keep;}incoming[0][s0*NR]=1;
 for(int phase=0;phase<(int)route.size();phase++){auto&a=route[phase];bool full=phase+1==(int)route.size();for(auto&m:following)m.clear();if(full&&external){for(int f=0;f<136;f++)for(auto [ix,z]:incoming[f]){int keep=min(external,a.w-cash(ix%NR));external_retained+=z*keep;following[f][(ix/NR)*NR+ri(cash(ix%NR)+keep)]+=z;}incoming.swap(following);for(auto&m:following)m.clear();}
 auto advance=[&](int f,int s,int r,double z){if(full)throw runtime_error("Final wait");for(int g:route[phase+1].g){int keep=min(g,999-s);retained+=z*keep;lost+=z*(g-keep);s+=keep;}following[f][s*NR+r]+=z;};
 // Inactive arrivals advance immediately; all remaining probability mass is in active visits.
 if(!full)for(int f=0;f<=a.u;f++){vector<int>erase;for(auto [ix,z]:incoming[f]){int ss=ix/NR;Observable x{ss,0,a.w,f==a.u?0:max(1,100*(a.u-f)/a.u),phase>=3,phase>=4,phase>=6,full,ntsc};if(!beginvisit(p,x)){advance(f,ss,ix%NR,z);erase.push_back(ix);}}for(int ix:erase)incoming[f].erase(ix);}

 for(int f=0;f<=min(135,a.u);f++){if(incoming[f].empty())continue;int b=f==a.u?0:max(1,100*(a.u-f)/a.u),floor=f<50?15:f<80?12:f<110?9:6;order.clear();touched.clear();
 auto node=[&](int i){if(seen[i])return;seen[i]=1;touched.push_back(i);flow[i]=0;indegree[i]=0;};for(auto [ix,z]:incoming[f])node(ix);
 for(size_t cursor=0;cursor<touched.size();cursor++){int i=touched[cursor],s=i/NR,r=i%NR;weight[i]=0;to[i]=i;Observable x{s,cash(r),a.w,b,phase>=3,phase>=4,phase>=6,full,ntsc};int action=choosehuman(p,x,true);actions[i]=action;if(action>0&&action<=100){if(action>s||f>=a.u)throw runtime_error("Illegal pull");weight[i]=1-max(floor,b+action-1)/100.;to[i]=(s-action)*NR+ri(min(a.w,cash(r)+5));}else if(action>100){int q=(action-101)%maxB+1,n=(action-101)/maxB;int rr=min(a.w,cash(r)+20*n)-price*q;if(rr<0||s+30*q>999)throw runtime_error("Illegal purchase");weight[i]=1;to[i]=(s+30*q)*NR+ri(rr);}if(weight[i])node(to[i]);}
 for(auto [ix,z]:incoming[f])flow[ix]+=z;for(int i:touched)if(weight[i])indegree[to[i]]++;

 for(int i:touched)if(!indegree[i])order.push_back(i);for(size_t j=0;j<order.size();j++){int i=order[j];if(weight[i]){flow[to[i]]+=weight[i]*flow[i];if(!--indegree[to[i]])order.push_back(to[i]);}}
 for(int root:touched)if(indegree[root]){vector<int>cycle;int i=root;do{cycle.push_back(i);indegree[i]=0;i=to[i];}while(i!=root);double x=0,prod=1;for(int node:cycle){x=flow[to[node]]+weight[node]*x;prod*=weight[node];}if(prod>=1)throw runtime_error("Improper cycle");flow[root]=x/(1-prod);for(size_t j=0;j+1<cycle.size();j++){int node=cycle[j];flow[to[node]]+=weight[node]*flow[node];}}
 for(int i:touched){int s=i/NR,r=i%NR,action=actions[i];double z=flow[i];if(!z)continue;int rr=cash(r);if(!action)advance(f,s,r,z);else if(action<=100){double chance=max(floor,b+action-1)/100.;cost[0]+=z;cost[1]+=z*(ntsc?d[min(s,101-b)][action]:action-1);used+=z*action;dupes+=z*(1-chance);int keep=min(5,a.w-rr);refund+=z*(1-chance)*keep;refundlost+=z*(1-chance)*(5-keep);if(f==135){complete+=z*chance;endS+=z*chance*(s-action);endR+=z*chance*rr;}else incoming[f+1][(s-action)*NR+r]+=z*chance;}else{int q=(action-101)%maxB+1,n=(action-101)/maxB;if(n&&!a.farm)throw runtime_error("Farm unavailable");cost[2]+=z*n;cost[3]+=z*((n?45:20)+15*q);trips+=z;purchased+=z*30*q;farmrupees+=z*(min(a.w,rr+20*n)-rr);}}
 for(int ix:touched)seen[ix]=0;incoming[f].clear();
 }
 incoming.swap(following);
 }
 double shellerr=retained+purchased-used-endS,casherr=refund+farmrupees+external_retained-purchased/30*price-endR;if(abs(complete-1)>1e-8||abs(shellerr)>1e-7||abs(casherr)>1e-7)throw runtime_error("Conservation or completion failure");ofstream out(argv[4]);out<<setprecision(15)<<"{\"id\":"<<p.id<<",\"cost_mean\":[";for(int i=0;i<4;i++)out<<(i?",":"")<<cost[i];out<<"],\"expected_seconds\":"<<20*cost[0]+cost[1]/15+4*cost[2]+cost[3];
 #define METRIC(x) out<<",\"" #x "\":"<<x
 METRIC(used);METRIC(purchased);METRIC(dupes);METRIC(trips);METRIC(retained);METRIC(lost);METRIC(refund);METRIC(refundlost);METRIC(farmrupees);METRIC(endS);METRIC(endR);METRIC(complete);METRIC(shellerr);METRIC(casherr);METRIC(external_retained);out<<"}\n";
 }catch(exception&e){cerr<<e.what()<<"\n";return 1;}}
