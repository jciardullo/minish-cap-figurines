#pragma once
#include <algorithm>
#include <array>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <vector>
using namespace std;
// Only this struct is passed to the human-policy interpreter. No F, U, event, or RNG.
struct Observable{int shells,rupees,wallet,chance;bool fortress_done,water,wind,full,ntsc;};
struct Routine{int trigger,stop,threshold,target;};
struct HumanPolicy{int id,boundary;Routine early,late;int band1,band2;array<int,3> threshold,target;int restock,partial,startchance=0;Routine fortress{},waterstage{};};
inline vector<HumanPolicy> loadpolicies(const string& path){ifstream in(path);vector<HumanPolicy> out;string line;while(getline(in,line)){if(line.empty())continue;istringstream row(line);HumanPolicy p;if(!(row>>p.id>>p.boundary>>p.early.trigger>>p.early.stop>>p.early.threshold>>p.early.target>>p.late.trigger>>p.late.stop>>p.late.threshold>>p.late.target>>p.band1>>p.band2>>p.threshold[0]>>p.target[0]>>p.threshold[1]>>p.target[1]>>p.threshold[2]>>p.target[2]>>p.restock>>p.partial))throw runtime_error("Bad policy row");row>>p.startchance;if(p.boundary==-2){if(!(row>>p.fortress.trigger>>p.fortress.stop>>p.fortress.threshold>>p.fortress.target>>p.waterstage.trigger>>p.waterstage.stop>>p.waterstage.threshold>>p.waterstage.target))throw runtime_error("Bad story table");}out.push_back(p);}if(out.empty())throw runtime_error("Empty policies");return out;}

inline bool islate(const HumanPolicy&p,const Observable&x){return p.boundary==3?x.fortress_done:p.boundary==4?x.water:p.boundary==6?x.wind:false;}
inline Routine routine(const HumanPolicy&p,const Observable&x){if(p.boundary==-2)return x.wind?p.late:x.water?p.waterstage:x.fortress_done?p.fortress:p.early;return islate(p,x)?p.late:p.early;}
inline int requested(int b,int threshold,int target){if(b>threshold)return 1;if(target<0)return min(-target,101-b);return max(1,target-b+1);}
// Session activation is observable and retained only until leaving Carlov.
inline bool beginvisit(const HumanPolicy&p,const Observable&x){return x.full||(x.shells>=routine(p,x).trigger&&x.chance>=p.startchance);}
// 0=end visit; 1..100=wager; 101+(B-1)+maxB*n=restock.
inline int choosehuman(const HumanPolicy&p,const Observable&x,bool active){
 int desired;
 if(!x.full){auto a=routine(p,x);if(!active||x.shells<=a.stop||x.chance==0)return 0;desired=requested(x.chance,a.threshold,a.target);if(desired>x.shells)return p.partial&&x.shells?x.shells:0;return desired;}
 int band=x.shells<=p.band1?0:x.shells<=p.band2?1:2;
 desired=requested(x.chance,p.threshold[band],p.target[band]);if(desired<=x.shells)return desired;
 if(p.partial&&x.shells)return x.shells;
 int price=x.ntsc?200:300,maxB=x.ntsc?4:3;
 int q=min({maxB,x.wallet/price,(999-x.shells)/30});
 if(p.restock==1)q=min(q,max(1,(desired-x.shells+29)/30));
 if(p.restock==2&&x.rupees>=price)q=min(q,x.rupees/price);
 if(q<=0)throw runtime_error("No feasible purchase");int n=max(0,(q*price-x.rupees+19)/20);return 101+(q-1)+maxB*n;
}
inline array<array<int,101>,101> inputcounts(){array<array<int,101>,101>d{};for(int limit=1;limit<=100;limit++){d[limit].fill(999);d[limit][1]=0;vector<int>q{1};for(size_t i=0;i<q.size();i++)for(int delta:{-10,-1,1,10}){int y=clamp(q[i]+delta,1,limit);if(d[limit][y]==999){d[limit][y]=d[limit][q[i]]+1;q.push_back(y);}}}return d;}
