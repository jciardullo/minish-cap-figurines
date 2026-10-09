// Independent forward simulation of exported full-state policies.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <sstream>
#include <vector>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
using namespace std;
constexpr int N=400000,NR=400;
int ri(int r){if(r%5!=0&&r%5!=4)throw runtime_error("unrepresented rupees");return 2*(r/5)+(r%5==4);}
struct Phase{int u,w;vector<int> pickups;const uint16_t *policy;size_t length;bool entryfarm=false,canfarm=true;const uint16_t*entrypolicy=nullptr;};
struct Stats{double time=0,pulls=0,duplicates=0,used=0,received=0,retained=0,lost=0,refund=0,refundlost=0,farm=0,farmrupees=0,purchased=0,trips=0,farm_start_trips=0,farm_start_funded_trips=0,shop_only_trips=0,earlyvisits=0,endS=0,endR=0;};
int main(int argc,char**argv){try{
 if(argc<5)throw runtime_error("simulate ROUTE PREFIX REGION OUTPUT [runs] [seed] [pullbase] [farmrate] [entryrate] [rngmode]");
 int runs=argc>5?stoi(argv[5]):20000;uint64_t seed=argc>6?stoull(argv[6]):20261007;
 double base=argc>7?stod(argv[7]):20,rate=argc>8?stod(argv[8]):300,entry=argc>9?stod(argv[9]):15;string rngmode=argc>10?argv[10]:"iid";
 string policy_prefix=argv[2];bool player=policy_prefix.rfind("player:",0)==0;if(player)policy_prefix=policy_prefix.substr(7);bool halfcap=policy_prefix.rfind("halfcap:",0)==0;bool halfmiddle=halfcap||policy_prefix.rfind("halfmid:",0)==0;bool middle=halfmiddle||policy_prefix.rfind("mid:",0)==0;bool observable=middle||policy_prefix.rfind("observable:",0)==0;if(observable)policy_prefix=policy_prefix.substr(halfmiddle?8:middle?4:11);string alternate_prefix;auto divider=policy_prefix.find('|');if(divider!=string::npos){alternate_prefix=policy_prefix.substr(divider+1);policy_prefix.resize(divider);}string endcap_prefix;auto capdivider=alternate_prefix.find('|');if(capdivider!=string::npos){endcap_prefix=alternate_prefix.substr(capdivider+1);alternate_prefix.resize(capdivider);}bool rules=string(argv[2]).rfind("rules:",0)==0;int reserves[8]={999,999,600,150,750,750,0,850};int rulethreshold=9,windthreshold=30,earlycutoff=100;if(rules){string spec=string(argv[2]).substr(6);replace(spec.begin(),spec.end(),':',' ');istringstream pars(spec);pars>>rulethreshold>>reserves[2]>>reserves[3]>>reserves[4]>>reserves[5]>>reserves[7];pars>>windthreshold>>earlycutoff;}bool practical=rules||string(argv[2]).rfind("@",0)==0; int threshold=27,pressure=900,earlytarget=100,stop=-1,lateTarget=-1,lateThreshold=100; if(practical&&!rules){string spec=string(argv[2]).substr(1);replace(spec.begin(),spec.end(),':',' ');istringstream pars(spec);pars>>threshold>>pressure>>earlytarget;if(!(pars>>stop))stop=pressure-1;pars.clear();pars>>lateTarget>>lateThreshold;}
 bool ntsc=string(argv[3])=="NTSC-U";int price=ntsc?200:300,maxbundles=ntsc?4:3;vector<Phase> phases;ifstream in(argv[1]);int u,w,k;
 while(in>>u>>w>>k){Phase p{u,w,{},nullptr,0};for(int j=0,x;j<k;j++){in>>x;p.pickups.push_back(x);}string tail;getline(in,tail);istringstream extra(tail);int atfarm=0;if(extra>>atfarm)p.entryfarm=atfarm;int available=1;if(extra>>available)p.canfarm=available;phases.push_back(p);}
 const uint16_t *postpolicy=nullptr;size_t postlength=0;if(practical&&argc>11){int fd=open(argv[11],O_RDONLY);if(fd<0)throw runtime_error("missing post policy");postlength=lseek(fd,0,SEEK_END);postpolicy=(uint16_t*)mmap(nullptr,postlength,PROT_READ,MAP_PRIVATE,fd,0);close(fd);}
 if(!practical)for(int j=0;j<(int)phases.size();j++){string file=policy_prefix+"_phase"+to_string(j)+".policy";int fd=open(file.c_str(),O_RDONLY);if(fd<0)throw runtime_error("missing "+file);auto &p=phases[j];p.length=lseek(fd,0,SEEK_END);p.policy=(uint16_t*)mmap(nullptr,p.length,PROT_READ,MAP_PRIVATE,fd,0);close(fd);if(p.policy==MAP_FAILED)throw runtime_error("mmap");}
 for(int j=0;j<(int)phases.size();j++)if(phases[j].entryfarm){if(practical||observable)throw runtime_error("Farm-entry adaptation not supplied for practical preset");int fd=open((policy_prefix+"_phase"+to_string(j)+".entry").c_str(),O_RDONLY);if(fd<0)throw runtime_error("Missing entry policy");size_t len=lseek(fd,0,SEEK_END);phases[j].entrypolicy=(uint16_t*)mmap(nullptr,len,PROT_READ,MAP_PRIVATE,fd,0);close(fd);}
 int inputs[101][101];for(int limit=1;limit<=100;limit++){fill(inputs[limit],inputs[limit]+101,999);inputs[limit][1]=0;vector<int> q{1};for(size_t i=0;i<q.size();i++)for(int delta:{-10,-1,1,10}){int y=clamp(q[i]+delta,1,limit);if(inputs[limit][y]==999){inputs[limit][y]=inputs[limit][q[i]]+1;q.push_back(y);}}}
const uint16_t*alternate=nullptr;size_t alternate_length=0;if(!alternate_prefix.empty()){string file=alternate_prefix+"_phase6.policy";int fd=open(file.c_str(),O_RDONLY);if(fd<0)throw runtime_error("alternate missing");alternate_length=lseek(fd,0,SEEK_END);alternate=(uint16_t*)mmap(nullptr,alternate_length,PROT_READ,MAP_PRIVATE,fd,0);close(fd);}
const uint16_t*endcap=nullptr;size_t endcap_length=0;if(!endcap_prefix.empty()){string file=endcap_prefix+"_phase7.policy";int fd=open(file.c_str(),O_RDONLY);if(fd<0)throw runtime_error("endcap missing");endcap_length=lseek(fd,0,SEEK_END);endcap=(uint16_t*)mmap(nullptr,endcap_length,PROT_READ,MAP_PRIVATE,fd,0);close(fd);}
 vector<uint32_t> initial_states;if(argc>13){ifstream initial(argv[13]);uint32_t state;while(initial>>state)initial_states.push_back(state);if(initial_states.size()<(size_t)runs)throw runtime_error("insufficient supplied initial states");}mt19937_64 random(seed);uniform_real_distribution<double> uniform(0,1);vector<Stats> samples;vector<array<double,8>> phase_stats(phases.size());
 for(int run=0;run<runs;run++){Stats z;int f=0,s=0,r=0;uint32_t state=(uint32_t)random();if(!state)state=1;if(!initial_states.empty())state=initial_states[run];
  auto draw=[&](){state*=3;state=(state>>13)|(state<<19);return state>>1;};
  for(int j=0;j<(int)phases.size()&&f<136;j++){auto &p=phases[j];int lookupj=(player||rules)&&(j==6||j==7)?(f<80?6:7):j;bool visit=false;
   for(int g:p.pickups){int keep=min(g,999-s);z.received+=g;z.retained+=keep;z.lost+=g-keep;s+=keep;}
   if(p.entryfarm){int a=p.entrypolicy[(size_t)f*N+s*NR+ri(r)];if(a){int q=(a-101)%maxbundles+1,n=(a-101)/maxbundles;if(n&&!p.canfarm)throw runtime_error("Farm unavailable before Mole Mitts");z.time+=25+15*q+1200./rate*n;z.trips++;z.farm_start_trips++;if(!n){z.shop_only_trips++;z.farm_start_funded_trips++;}z.farm+=n;int keep=min(p.w,r+20*n)-r;r+=keep;z.farmrupees+=keep;for(int i=0;i<q;i++){if(r<price||s+30>999)throw runtime_error("Illegal farm-entry buy");r-=price;s+=30;z.purchased+=30;}}}
   phase_stats[j][0]+=f;phase_stats[j][1]+=s;double before_time=z.time,before_pulls=z.pulls,before_used=z.used;if(rules){threshold=rulethreshold;stop=j<8?reserves[lookupj]:-1;pressure=stop+1;earlytarget=100;lateTarget=0;}bool active=s>=pressure;for(int actioncount=0;;actioncount++){if(actioncount>100000)throw runtime_error("improper simulation");size_t ix=(size_t)f*N+s*NR+ri(r);int a;
    if(practical&&p.u==136&&postpolicy){if((ix+1)*2>postlength)throw runtime_error("post lookup bounds");a=postpolicy[ix];}
    else if(practical){int b=max(1,100*(p.u-f)/p.u);if(f>=p.u||(p.u<136&&(!active||s<=stop)))a=0;else{int target=rules&&lookupj==6?(b>windthreshold?1:100):rules?(b>earlycutoff?1:100):(j>=6&&lateTarget>0)?(b>lateThreshold?1:lateTarget):earlytarget;int wager=p.u<136?max(1,target-b+1):(b>threshold?1:101-b);if(s>=wager)a=wager;else if(p.u<136)a=0;else{int q=min({maxbundles,p.w/price,(999-s)/30});if(!q)throw runtime_error("practical cannot buy");int n=max(0,(q*price-r+19)/20);a=101+(q-1)+maxbundles*n;}}}
    else if(middle&&!halfcap&&j==5){int b=max(1,100*(p.u-f)/p.u);a=f>=p.u||s<=700?0:min(101-b,s-700);}
    else{const uint16_t*selected=phases[lookupj].policy;size_t selected_length=phases[lookupj].length;int shown=max(1,100*(p.u-f)/p.u);if(lookupj==6&&alternate&&shown==max(1,100*(130-f)/130)&&shown!=max(1,100*(123-f)/123)){selected=alternate;selected_length=alternate_length;}if(lookupj==7&&endcap){selected=endcap;selected_length=endcap_length;}size_t selected_index=ix;if(middle&&!halfmiddle&&lookupj==6&&selected!=alternate)selected_index=(size_t)f*N+max(0,s-100)*NR+ri(r);if(middle&&lookupj==7)selected_index=(size_t)f*N+max(0,s-150)*NR+ri(r);if((selected_index+1)*2>selected_length){if(observable)a=0;else throw runtime_error("policy outside pool");}else a=selected[selected_index];if(observable){if(f>=p.u)a=0;else if(a>0&&a<=100)a=min(a,101-max(1,100*(p.u-f)/p.u));}}if(a==0){if(j+1==(int)phases.size())throw runtime_error("advance at final");break;}
    if(a<=100){if(a>s||f>=p.u)throw runtime_error("illegal pull");if(!visit&&j+1<(int)phases.size())z.earlyvisits++;visit=true;int b=max(1,100*(p.u-f)/p.u),floor=f<50?15:f<80?12:f<110?9:6,percent=max(floor,b+a-1);if(a>101-b)throw runtime_error("wager above bound");
     z.time+=base+(ntsc?inputs[min(s,101-b)][a]:a-1)/entry;s-=a;z.used+=a;z.pulls++;
     bool success;if(rngmode=="iid")success=uniform(random)<percent/100.;else{uint32_t x;do{x=draw()&127;}while(x>=100);success=x<(uint32_t)percent;draw();if(rngmode=="prng-gap")for(int gap=0;gap<1200;gap++)draw();}
     if(success){f++;if(f==136)break;}else{z.duplicates++;int keep=min(5,p.w-r);r+=keep;z.refund+=keep;z.refundlost+=5-keep;}
    }else{int q=(a-101)%maxbundles+1,n=(a-101)/maxbundles;if(n&&!p.canfarm)throw runtime_error("Farm unavailable before Mole Mitts");z.time+=(n?45:20)+15*q+1200./rate*n;z.trips++;if(!n)z.shop_only_trips++;z.farm+=n;for(int i=0;i<n;i++){int keep=min(20,p.w-r);r+=keep;z.farmrupees+=keep;}for(int i=0;i<q;i++){if(r<price||s+30>999)throw runtime_error("illegal purchase");r-=price;s+=30;z.purchased+=30;}}
   }
   phase_stats[j][2]+=f;phase_stats[j][3]+=s;phase_stats[j][4]+=z.time-before_time;phase_stats[j][5]+=z.pulls-before_pulls;phase_stats[j][6]+=z.used-before_used;phase_stats[j][7]+=visit;
  }
  if(f!=136)throw runtime_error("incomplete");z.endS=s;z.endR=r;samples.push_back(z);
 }
 if(argc>12){ofstream raw(argv[12]);raw<<setprecision(15);for(auto &z:samples)raw<<z.time<<"\n";}ofstream phaseout(string(argv[4])+".phases.csv");phaseout<<"phase,start_owned,start_shells,end_owned,end_shells,seconds,pulls,shells_used,visit_probability\n";for(size_t j=0;j<phases.size();j++){phaseout<<j;for(double v:phase_stats[j])phaseout<<","<<v/runs;phaseout<<"\n";}
 auto metric=[&](double Stats::*m){double v=0;for(auto &z:samples)v+=z.*m;return v/runs;};double mean=metric(&Stats::time),var=0;vector<double> times;for(auto &z:samples){var+=(z.time-mean)*(z.time-mean);times.push_back(z.time);}sort(times.begin(),times.end());double sd=sqrt(var/(runs-1)),ci=1.959963984540054*sd/sqrt(runs);
 ofstream out(argv[4]);out<<setprecision(15)<<"{\n\"runs\":"<<runs<<",\"seed\":"<<seed<<",\"rng_model\":\""<<rngmode<<"\",\"mean_seconds\":"<<mean<<",\"ci95_mean_low\":"<<mean-ci<<",\"ci95_mean_high\":"<<mean+ci<<",\"median_seconds\":"<<times[runs/2]<<",\"p90_seconds\":"<<times[(int)(.9*runs)]<<",\"p95_seconds\":"<<times[(int)(.95*runs)]<<",\"sd_seconds\":"<<sd;
 #define METRIC(field) out<<",\n\"" #field "\":"<<metric(&Stats::field)
 METRIC(pulls);METRIC(duplicates);METRIC(used);METRIC(received);METRIC(retained);METRIC(lost);METRIC(refund);METRIC(refundlost);METRIC(farm);METRIC(farmrupees);METRIC(purchased);METRIC(trips);METRIC(farm_start_trips);METRIC(farm_start_funded_trips);METRIC(shop_only_trips);METRIC(earlyvisits);METRIC(endS);METRIC(endR);out<<"\n}\n";
 }catch(exception &e){cerr<<e.what()<<"\n";return 1;}}
