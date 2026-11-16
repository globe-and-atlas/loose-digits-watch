#include "motion.h"
#include <assert.h>
#include <string.h>
#include <stdio.h>
static void neutral(LDGesture *g,uint32_t t){for(int i=0;i<3;i++)assert(!ld_sample(g,0,-1000,false,true,false,t+i*40));}
static bool roll(LDGesture *g,int x,uint32_t t){assert(!ld_sample(g,x,-600,false,true,false,t));return ld_sample(g,x,-600,false,true,false,t+40);}
static bool impulse(LDKnock *g,int axis,uint32_t time,bool single){
 int x=0,y=0,z=-1000;if(axis==0)x=1200;if(axis==1)y=1200;if(axis==2)z=200;
 return ld_knock_sample(g,x,y,z,false,true,false,single,time);
}
static void test_knocks(void){
 for(int axis=0;axis<3;axis++){
  LDKnock g={0};assert(!ld_knock_sample(&g,0,0,-1000,false,true,false,false,0));
  assert(!impulse(&g,axis,200,false));assert(!ld_knock_sample(&g,0,0,-1000,false,true,false,false,220));
  assert(impulse(&g,axis,440,false));
  assert(!ld_knock_sample(&g,0,0,-1000,false,true,false,false,460));assert(!impulse(&g,axis,650,false));
 }
 LDKnock g={0};ld_knock_sample(&g,0,0,-1000,false,true,false,false,0);
 assert(!impulse(&g,1,200,false));assert(!ld_knock_sample(&g,0,0,-1000,false,true,false,false,220));assert(!impulse(&g,1,1000,false));
 g=(LDKnock){0};ld_knock_sample(&g,0,0,-1000,false,true,false,true,0);assert(impulse(&g,1,200,true));
 g=(LDKnock){0};ld_knock_sample(&g,0,0,-1000,false,true,false,false,0);assert(!impulse(&g,0,200,false));
 assert(!ld_knock_sample(&g,0,0,-1000,true,true,false,false,400));assert(!impulse(&g,0,600,false));
 assert(!ld_knock_sample(&g,0,0,-1000,false,false,false,false,800));assert(!impulse(&g,0,1000,false));
 assert(!ld_knock_sample(&g,0,0,-1000,false,true,true,false,1200));assert(!impulse(&g,0,1400,false));
 g=(LDKnock){0};ld_knock_sample(&g,0,0,-1000,false,true,false,false,UINT32_MAX-400);
 assert(!impulse(&g,2,UINT32_MAX-200,false));assert(!ld_knock_sample(&g,0,0,-1000,false,true,false,false,UINT32_MAX-180));assert(impulse(&g,2,100,false));
 puts("PASS: axis-independent knocks, double/single modes, rebound, timeout, cooldown, disabled/busy/vibration, wraparound");
}
int main(void){
 test_knocks();
 assert(ld_background_is_light(0,3,0));assert(ld_background_is_light(3,3,0));assert(ld_background_is_light(3,3,3));assert(!ld_background_is_light(0,0,3));assert(!ld_background_is_light(0,0,0));
 LDGesture g={0};neutral(&g,3000000000U);assert(roll(&g,750,3000000200U));
 for(int i=0;i<1000;i++)assert(!ld_sample(&g,750,-600,false,true,false,3000000300U+i*40));
 neutral(&g,3000050000U);assert(roll(&g,-750,3000050200U));
 neutral(&g,3000050300U);assert(!roll(&g,750,3000050400U));
 g=(LDGesture){0};for(int i=0;i<10000;i++)assert(!ld_sample(&g,(i%7)*30,-950,false,true,false,i*40));
 neutral(&g,500000);assert(!ld_sample(&g,750,-600,true,true,false,500200));assert(!roll(&g,750,500500));
 neutral(&g,501000);assert(!ld_sample(&g,750,-600,false,false,false,501200));assert(!roll(&g,750,501500));
 neutral(&g,502000);assert(!ld_sample(&g,750,-600,false,true,true,502200));assert(!roll(&g,750,502500));
 g=(LDGesture){0};neutral(&g,UINT32_MAX-1000);assert(roll(&g,750,UINT32_MAX-800));neutral(&g,500);assert(!roll(&g,750,1000));neutral(&g,6000);assert(roll(&g,-750,6500));
 char digits[5],period[3];ld_format_time(0,0,true,digits,period);assert(!strcmp(digits,"0000")&&!strcmp(period,""));
 ld_format_time(0,9,false,digits,period);assert(!strcmp(digits,"1209")&&!strcmp(period,"AM"));
 ld_format_time(12,0,false,digits,period);assert(!strcmp(digits,"1200")&&!strcmp(period,"PM"));
 ld_format_time(23,59,false,digits,period);assert(!strcmp(digits,"1159")&&!strcmp(period,"PM"));
 ld_format_time(1,8,false,digits,period);assert(!strcmp(digits," 108"));
 for(int h=0;h<24;h++)for(int m=0;m<60;m++){ld_format_time(h,m,true,digits,period);assert(digits[0]=='0'+h/10&&digits[1]=='0'+h%10&&digits[2]=='0'+m/10&&digits[3]=='0'+m%10);}
 int ws[]={200,180,260},hs[]={228,180,260};
 for(int k=0;k<3;k++)for(int dir=-1;dir<=1;dir+=2)for(int i=0;i<4;i++){
  LDPose first=ld_pose(i,ws[k],hs[k],0,dir),last=ld_pose(i,ws[k],hs[k],LD_DURATION,dir);
  assert(first.x==last.x&&first.y==last.y&&last.angle==0);
  for(int t=0;t<=LD_DURATION;t+=10){LDPose a=ld_pose(i,ws[k],hs[k],t,dir);assert(a.x>0&&a.x<ws[k]&&a.y>0&&a.y<hs[k]);assert(a.angle>=-29&&a.angle<=29);}
 }
 puts("PASS: gesture, cooldown, disabled/vibration/busy, wraparound, 1440 times, bounded poses, exact reassembly");
}
