#include "policy.hpp"
#include <cassert>
#include <iostream>
int main(){
 const char* files[]={"PAL_knee","NTSC-U_knee","PAL_compact","NTSC-U_compact"};
 for(int version=0;version<2;version++)for(int type=0;type<2;type++){
  std::string file="outputs/distillation/selected_policies/"+std::string(files[type*2+version])+".txt";auto p=loadpolicies(file)[0];
  int trigger=type?version?800:700:1,entry=type?20:version?60:50;
  Observable x{999,0,999,entry,false,false,false,false,bool(version)};
  x.shells=trigger;assert(beginvisit(p,x));x.chance=entry-1;assert(!beginvisit(p,x));x.chance=entry;
  if(type){x.shells=trigger-1;assert(!beginvisit(p,x));x.shells=999;}
  for(int phase=0;phase<5;phase++){
   x.fortress_done=phase>=1;x.water=phase>=2;x.wind=phase>=3;x.full=phase==4;x.shells=999;
   int cut=type?phase==0?80:phase<3?100:phase==3?version?20:15:version?9:8:phase==4?version?10:7:version?100:50;
   for(int b:{cut-1,cut,cut+1})if(b>=1&&b<=100){x.chance=b;int expected=b>cut?1:101-b;assert(choosehuman(p,x,true)==expected);}
   if(type&&!x.full){int reserve=phase==0?600:phase==1?version?100:150:phase==2?800:0;x.shells=reserve;x.chance=70;assert(choosehuman(p,x,true)==0);x.shells=reserve+1;assert(choosehuman(p,x,true)>0);}
  }
 }
 std::cout<<"Inclusive entry gates, strict wager thresholds, equality branches and reserve stops match all four frozen policy IDs.\n";
}
