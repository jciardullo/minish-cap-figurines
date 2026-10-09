// Independent exact forward occupancy evaluation; no Bellman optimization.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <queue>
#include <string>
#include <sstream>
#include <vector>
using namespace std;
constexpr int NR=400,N=400000;
int cash(int i){return 5*(i/2)+(i%2?4:0);}int ri(int r){return 2*(r/5)+(r%5==4);}
struct Phase{int u,w;vector<int> g;bool entryfarm=false,canfarm=true;};
int main(int argc,char**argv){try{
 if(argc<5)throw runtime_error("evaluate_exact ROUTE PREFIX REGION OUTPUT [base] [farmrate] [entryrate]");string policy_prefix=argv[2];bool halfcap=policy_prefix.rfind("halfcap:",0)==0;bool halfmiddle=halfcap||policy_prefix.rfind("halfmid:",0)==0;bool middle=halfmiddle||policy_prefix.rfind("mid:",0)==0;bool observable=middle||policy_prefix.rfind("observable:",0)==0;if(observable)policy_prefix=policy_prefix.substr(halfmiddle?8:middle?4:11);string alternate_prefix;auto divider=policy_prefix.find('|');if(divider!=string::npos){alternate_prefix=policy_prefix.substr(divider+1);policy_prefix.resize(divider);}string endcap_prefix;auto capdivider=alternate_prefix.find('|');if(capdivider!=string::npos){endcap_prefix=alternate_prefix.substr(capdivider+1);alternate_prefix.resize(capdivider);}bool rules=string(argv[2]).rfind("rules:",0)==0;int reserves[8]={999,999,600,150,750,750,0,850};int rulethreshold=9,windthreshold=30,earlycutoff=100;if(rules){string spec=string(argv[2]).substr(6);replace(spec.begin(),spec.end(),':',' ');istringstream pars(spec);pars>>rulethreshold>>reserves[2]>>reserves[3]>>reserves[4]>>reserves[5]>>reserves[7];pars>>windthreshold>>earlycutoff;}bool practical=rules||string(argv[2]).rfind("@",0)==0;int threshold=27,pressure=900,earlytarget=100,stop=-1,lateTarget=-1,lateThreshold=100;if(practical&&!rules){string spec=string(argv[2]).substr(1);replace(spec.begin(),spec.end(),':',' ');istringstream pars(spec);pars>>threshold>>pressure>>earlytarget;if(!(pars>>stop))stop=pressure-1;pars.clear();pars>>lateTarget>>lateThreshold;}bool ntsc=string(argv[3])=="NTSC-U";int price=ntsc?200:300,maxbundles=ntsc?4:3;double base=argc>5?stod(argv[5]):20,rate=argc>6?stod(argv[6]):300,entry=argc>7?stod(argv[7]):15;
 ifstream postpolicy;if(practical&&argc>8){postpolicy.open(argv[8],ios::binary);if(!postpolicy)throw runtime_error("post lookup open");}ifstream alternate;if(!alternate_prefix.empty()){alternate.open(alternate_prefix+"_phase6.policy",ios::binary);if(!alternate)throw runtime_error("alternate missing");}ifstream endcap;if(!endcap_prefix.empty()){endcap.open(endcap_prefix+"_phase7.policy",ios::binary);if(!endcap)throw runtime_error("endcap missing");}vector<Phase> phases;ifstream in(argv[1]);int u,w,k;while(in>>u>>w>>k){Phase p{u,w,{}};for(int i=0,x;i<k;i++){in>>x;p.g.push_back(x);}string tail;getline(in,tail);istringstream extra(tail);int atfarm=0;if(extra>>atfarm)p.entryfarm=atfarm;int available=1;if(extra>>available)p.canfarm=available;phases.push_back(p);}
 int inputs[101][101];for(int l=1;l<=100;l++){fill(inputs[l],inputs[l]+101,999);inputs[l][1]=0;vector<int> q{1};for(size_t j=0;j<q.size();j++)for(int delta:{-10,-1,1,10}){int y=clamp(q[j]+delta,1,l);if(inputs[l][y]==999){inputs[l][y]=inputs[l][q[j]]+1;q.push_back(y);}}}
 vector<double> incoming((size_t)137*N),following(incoming.size()),flow(N),weight(N);vector<int> to(N),indegree(N),order;vector<uint16_t> actions(N);
 double observable_entry_mismatch=0,shop_only_trips=0,farm_start_trips=0,farm_start_funded_trips=0; double time=0,pulls=0,dupes=0,used=0,received=0,retained=0,lost=0,refund=0,refundlost=0,farm=0,farmrupees=0,purchased=0,trips=0,endS=0,endR=0,complete=0;int start=0;for(int g:phases[0].g){int keep=min(g,999-start);received+=g;retained+=keep;lost+=g-keep;start+=keep;}incoming[start*NR]=1;
 for(int phase=0;phase<(int)phases.size();phase++){auto p=phases[phase];if(rules){threshold=rulethreshold;stop=phase<8?reserves[phase]:-1;pressure=stop+1;earlytarget=100;lateTarget=0;}if((observable||rules)&&(phase==6||phase==7))for(int f=0;f<137;f++)if((phase==6&&f>=80)||(phase==7&&f<80))for(int i=0;i<N;i++)observable_entry_mismatch+=incoming[(size_t)f*N+i];ifstream policy(policy_prefix+"_phase"+to_string(phase)+".policy",ios::binary);fill(following.begin(),following.end(),0);
 if(p.entryfarm){if(practical||observable)throw runtime_error("Farm-entry adaptation not supplied for practical preset");ifstream ent(policy_prefix+"_phase"+to_string(phase)+".entry",ios::binary);if(!ent)throw runtime_error("Missing farm-entry policy");for(int f=0;f<=min(135,p.u);f++){ent.read((char*)actions.data(),2*N);if(!ent)throw runtime_error("Entry policy truncated");for(int s=0;s<1000;s++)for(int r=0;r<NR;r++){double z=incoming[(int64_t)f*N+s*NR+r];if(!z)continue;int a=actions[s*NR+r],ss=s,rr=cash(r);if(a){if(a<=100)throw runtime_error("Illegal entry pull");int q=(a-101)%maxbundles+1,n=(a-101)/maxbundles;if(n&&!p.canfarm)throw runtime_error("Farm unavailable before Mole Mitts");int keep=min(p.w,rr+20*n)-rr;rr+=keep;rr-=q*price;ss+=30*q;if(rr<0||ss>999)throw runtime_error("Illegal entry purchase");time+=z*(25+15*q+1200./rate*n);trips+=z;farm_start_trips+=z;if(!n){shop_only_trips+=z;farm_start_funded_trips+=z;}farm+=z*n;farmrupees+=z*keep;purchased+=z*30*q;}following[(int64_t)f*N+ss*NR+ri(rr)]+=z;}}swap(incoming,following);fill(following.begin(),following.end(),0);}
 if(practical&&p.u<136){
 for(int f=0;f<=min(135,p.u);f++)for(int s=0;s<pressure;s++)for(int r=0;r<NR;r++){
  size_t ix=(size_t)f*N+s*NR+r;double z=incoming[ix];if(!z)continue;int ss=s;
  for(int g:phases[phase+1].g){int keep=min(g,999-ss);received+=z*g;retained+=z*keep;lost+=z*(g-keep);ss+=keep;}
  following[(size_t)f*N+ss*NR+r]+=z;incoming[ix]=0;
 }
 }
for(int f=0;f<=min(135,p.u);f++){
  double mass=0;for(int i=0;i<N;i++)mass+=incoming[(size_t)f*N+i];if(!mass)continue;
  if(practical&&p.u==136&&postpolicy.is_open()){postpolicy.seekg((size_t)f*N*2);postpolicy.read((char*)actions.data(),2*N);if(!postpolicy)throw runtime_error("post lookup read");}
 else if(practical){int b=max(1,100*(p.u-f)/p.u);for(int s=0;s<1000;s++)for(int r=0;r<NR;r++){
 int a=0;if(cash(r)<=p.w&&f<p.u&&(p.u==136||s>stop)){int target=rules&&phase==6?(b>windthreshold?1:100):rules?(b>earlycutoff?1:100):(phase>=6&&lateTarget>0)?(b>lateThreshold?1:lateTarget):earlytarget;int wager=p.u<136?max(1,target-b+1):(b>threshold?1:101-b);if(s>=wager)a=wager;else if(p.u==136){int q=min({maxbundles,p.w/price,(999-s)/30});int n=max(0,(q*price-cash(r)+19)/20);a=101+(q-1)+maxbundles*n;}}
 actions[s*NR+r]=a;}}
 else{int shown=max(1,100*(p.u-f)/p.u);bool usealternate=phase==6&&alternate.is_open()&&shown==max(1,100*(130-f)/130)&&shown!=max(1,100*(123-f)/123);ifstream &selected=(phase==7&&endcap.is_open())?endcap:usealternate?alternate:policy;selected.seekg((size_t)f*N*2);selected.read((char*)actions.data(),2*N);if(!selected){if(observable){fill(actions.begin(),actions.end(),0);selected.clear();}else throw runtime_error("policy read at phase "+to_string(phase)+" owned "+to_string(f));}
 if(middle){vector<uint16_t> original=actions;if(phase==5&&!halfcap){for(int s=0;s<1000;s++)for(int r=0;r<NR;r++)actions[s*NR+r]=f>=p.u||s<=700?0:min(101-max(1,100*(p.u-f)/p.u),s-700);}else if((phase==6&&!usealternate)||phase==7){int reserve=phase==6?(halfmiddle?0:100):150;for(int s=0;s<1000;s++)for(int r=0;r<NR;r++)actions[s*NR+r]=original[max(0,s-reserve)*NR+r];}}
 if(observable)for(auto &a:actions){if(f>=p.u)a=0;else if(a>0&&a<=100)a=min((int)a,101-max(1,100*(p.u-f)/p.u));}}copy(incoming.begin()+(size_t)f*N,incoming.begin()+(size_t)(f+1)*N,flow.begin());fill(indegree.begin(),indegree.end(),0);order.clear();
  int b=max(1,100*(p.u-f)/p.u),floor=f<50?15:f<80?12:f<110?9:6;
  for(int s=0;s<1000;s++)for(int r=0;r<NR;r++){int i=s*NR+r,a=actions[i];weight[i]=0;to[i]=i;if(cash(r)>p.w)continue;
   if(a>0&&a<=100){if(a>s||f>=p.u)throw runtime_error("illegal pull");weight[i]=1-max(floor,b+a-1)/100.;to[i]=(s-a)*NR+ri(min(p.w,cash(r)+5));}
   else if(a>100){int q=(a-101)%maxbundles+1,n=(a-101)/maxbundles;int rr=min(p.w,cash(r)+20*n)-price*q;if(rr<0||s+30*q>999)throw runtime_error("illegal buy");weight[i]=1;to[i]=(s+30*q)*NR+ri(rr);}
   if(weight[i])indegree[to[i]]++;
  }
  for(int i=0;i<N;i++)if(!indegree[i])order.push_back(i);
  for(size_t j=0;j<order.size();j++){int i=order[j];if(weight[i]){flow[to[i]]+=weight[i]*flow[i];if(!--indegree[to[i]])order.push_back(to[i]);}}
  for(int root=0;root<N;root++)if(indegree[root]){vector<int> cycle;int i=root;do{cycle.push_back(i);indegree[i]=0;i=to[i];}while(i!=root);double x=0,prod=1;for(int node:cycle){int dest=to[node];x=flow[dest]+weight[node]*x;prod*=weight[node];}if(prod>=1)throw runtime_error("improper cycle");flow[root]=x/(1-prod);for(size_t j=0;j+1<cycle.size();j++){int node=cycle[j];flow[to[node]]+=weight[node]*flow[node];}}
  for(int s=0;s<1000;s++)for(int r=0;r<NR;r++){int i=s*NR+r,a=actions[i];double z=flow[i];if(!z)continue;int rr=cash(r);
   if(a==0){if(phase+1==(int)phases.size())throw runtime_error("final advance");int ss=s;for(int g:phases[phase+1].g){int keep=min(g,999-ss);received+=z*g;retained+=z*keep;lost+=z*(g-keep);ss+=keep;}following[(size_t)f*N+ss*NR+r]+=z;}
   else if(a<=100){double chance=max(floor,b+a-1)/100.;time+=z*(base+(ntsc?inputs[min(s,101-b)][a]:a-1)/entry);pulls+=z;dupes+=z*(1-chance);used+=z*a;int keep=min(5,p.w-rr);refund+=z*(1-chance)*keep;refundlost+=z*(1-chance)*(5-keep);if(f==135){complete+=z*chance;endS+=z*chance*(s-a);endR+=z*chance*rr;}else incoming[(size_t)(f+1)*N+(s-a)*NR+r]+=z*chance;}
   else{int q=(a-101)%maxbundles+1,n=(a-101)/maxbundles;if(n&&!p.canfarm)throw runtime_error("Farm unavailable before Mole Mitts");time+=z*((n?45:20)+15*q+1200./rate*n);trips+=z;if(!n)shop_only_trips+=z;farm+=z*n;farmrupees+=z*(min(p.w,rr+20*n)-rr);purchased+=z*30*q;}
  }
 }
 swap(incoming,following);
 }
 if(abs(complete-1)>1e-8)throw runtime_error("completion probability");if(abs(retained+purchased-used-endS)>1e-7||abs(refund+farmrupees-purchased/30*price-endR)>1e-7)throw runtime_error("conservation");
 ofstream out(argv[4]);out<<setprecision(15)<<"{\"expected_seconds\":"<<time<<",\"completion_probability\":"<<complete;
 #define M(x) out<<",\"" #x "\":"<<x
 M(farm_start_trips);M(farm_start_funded_trips);M(shop_only_trips);M(observable_entry_mismatch);M(pulls);M(dupes);M(used);M(received);M(retained);M(lost);M(refund);M(refundlost);M(farm);M(farmrupees);M(purchased);M(trips);M(endS);M(endR);out<<"}\n";
 }catch(exception&e){cerr<<e.what()<<"\n";return 1;}}
