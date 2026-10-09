#include "policy.hpp"
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <random>
struct Phase{int u,w;vector<int>g;bool farm;};
struct Totals{array<double,4>cost{};double used=0,purchased=0,dupes=0,trips=0,retained=0,lost=0,refund=0,farmrupees=0,endS=0,endR=0;};
uint64_t mix(uint64_t z){z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
int main(int argc,char**argv){try{if(argc<7)throw runtime_error("screen policies route region output runs seed [cash]");auto policies=loadpolicies(argv[1]);ifstream in(argv[2]);vector<Phase>route;int u,w,k;while(in>>u>>w>>k){Phase p{u,w,{}};for(int i=0,x;i<k;i++){in>>x;p.g.push_back(x);}string line;getline(in,line);istringstream tail(line);int loc=0,farm=1;tail>>loc>>farm;p.farm=farm;route.push_back(p);}bool ntsc=string(argv[3])=="NTSC-U";int price=ntsc?200:300,maxB=ntsc?4:3,runs=stoi(argv[5]),seed=stoi(argv[6]),external=argc>7?stoi(argv[7]):0;auto d=inputcounts();ofstream out(argv[4]);out<<setprecision(15);for(auto&p:policies){array<double,4>sum{};array<double,16>cross{};Totals mean;vector<double>times;
 for(int trial=0;trial<runs;trial++){int f=0,s=0,r=0,draws=0;Totals z;for(int j=0;j<(int)route.size()&&f<136;j++){auto&a=route[j];for(int g:a.g){int keep=min(g,999-s);s+=keep;z.retained+=keep;z.lost+=g-keep;}if(j+1==(int)route.size())r=min(a.w,r+external);Observable x{s,r,a.w,f==a.u?0:max(1,100*(a.u-f)/a.u),j>=3,j>=4,j>=6,j+1==(int)route.size(),ntsc};bool active=beginvisit(p,x);
 for(int count=0;;count++){if(count>100000)throw runtime_error("Nonterminating policy");x.shells=s;x.rupees=r;x.chance=f==a.u?0:max(1,100*(a.u-f)/a.u);int action=choosehuman(p,x,active);if(!action){if(x.full)throw runtime_error("Final wait");break;}
 if(action<=100){if(action>s||f>=a.u||action>101-x.chance)throw runtime_error("Illegal pull");int chance=max(f<50?15:f<80?12:f<110?9:6,x.chance+action-1);z.cost[0]++;z.cost[1]+=ntsc?d[min(s,101-x.chance)][action]:action-1;s-=action;z.used+=action;double v=(mix(((uint64_t)seed<<32)^((uint64_t)trial*0x9e3779b97f4a7c15ULL)^((uint64_t)draws++*0xd1b54a32d192ed03ULL))>>11)*0x1.0p-53;if(v<chance/100.){f++;if(f==136)break;}else{z.dupes++;int keep=min(5,a.w-r);r+=keep;z.refund+=keep;}}
 else{int q=(action-101)%maxB+1,n=(action-101)/maxB;if(n&&!a.farm)throw runtime_error("Farm unavailable");z.cost[2]+=n;z.cost[3]+=(n?45:20)+15*q;z.trips++;int keep=min(a.w,r+20*n)-r;r+=keep;z.farmrupees+=keep;r-=price*q;s+=30*q;z.purchased+=30*q;if(r<0||s>999)throw runtime_error("Illegal purchase");}
 }
 }if(f!=136)throw runtime_error("Incomplete");z.endS=s;z.endR=r;for(int i=0;i<4;i++){sum[i]+=z.cost[i];for(int j=0;j<4;j++)cross[i*4+j]+=z.cost[i]*z.cost[j];}mean.used+=z.used;mean.purchased+=z.purchased;mean.dupes+=z.dupes;mean.trips+=z.trips;mean.retained+=z.retained;mean.lost+=z.lost;mean.refund+=z.refund;mean.farmrupees+=z.farmrupees;mean.endS+=s;mean.endR+=r;times.push_back(20*z.cost[0]+z.cost[1]/15+4*z.cost[2]+z.cost[3]);}
 out<<"{\"id\":"<<p.id<<",\"runs\":"<<runs<<",\"seed\":"<<seed<<",\"cost_mean\":[";for(int i=0;i<4;i++)out<<(i?",":"")<<sum[i]/runs;out<<"],\"cost_cov\":[";for(int i=0;i<16;i++)out<<(i?",":"")<<(cross[i]-sum[i/4]*sum[i%4]/runs)/(runs-1);out<<"]";
 #define METRIC(x) out<<",\"" #x "\":"<<mean.x/runs
 METRIC(used);METRIC(purchased);METRIC(dupes);METRIC(trips);METRIC(retained);METRIC(lost);METRIC(refund);METRIC(farmrupees);METRIC(endS);METRIC(endR);
 if(runs>=20000){sort(times.begin(),times.end());double ave=0,sd=0;for(double v:times)ave+=v/runs;for(double v:times)sd+=(v-ave)*(v-ave);sd=sqrt(sd/(runs-1));out<<",\"mean_seconds\":"<<ave<<",\"ci95_mean_low\":"<<ave-1.95996398454*sd/sqrt(runs)<<",\"ci95_mean_high\":"<<ave+1.95996398454*sd/sqrt(runs)<<",\"median_seconds\":"<<(times[runs/2-1]+times[runs/2])/2<<",\"p90_seconds\":"<<times[(int)(.9*runs)]<<",\"p95_seconds\":"<<times[(int)(.95*runs)]<<",\"sd_seconds\":"<<sd;}
 out<<"}\n";
 }return 0;}catch(exception&e){cerr<<e.what()<<"\n";return 1;}}
