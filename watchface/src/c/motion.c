#include "motion.h"
#include <stdlib.h>
bool ld_sample(LDGesture *g,int x,int z,bool vibrated,bool enabled,bool busy,uint32_t now) {
 if(!enabled||busy||vibrated){g->neutral=g->rolled=0;g->armed=false;return false;}
 if(g->cooling&&(int32_t)(now-g->cooldown_until)<0)return false;
 g->cooling=false;
 if(abs(x)<300&&abs(z)>500){if(g->neutral<3)++g->neutral;if(g->neutral>=3)g->armed=true;g->rolled=0;}
 else {g->neutral=0;if(g->armed&&abs(x)>620&&abs(z)>220){if(++g->rolled>=2){g->armed=false;g->rolled=0;g->cooldown_until=now+LD_COOLDOWN;g->cooling=true;return true;}}else g->rolled=0;}
 return false;
}
static int smooth(int q){return q*q/1000*(3000-2*q)/1000;}
LDPose ld_pose(int index,int width,int height,uint32_t elapsed,int direction){
 int cell=(width-24)/26;const int units[]={3,9,17,23};
 int sx=(width-26*cell)/2+units[index]*cell,sy=height*45/100;
 const int dx[]={23,41,59,77},dy[]={61,73,73,61},angles[]={-24,22,-17,29};
 int tx=width*dx[index]/100,ty=height*dy[index]/100;
 if(direction<0){tx=width-width*dx[3-index]/100;ty=height*dy[3-index]/100;}
 int q=0;
 if(elapsed<1200){int local=(int)elapsed-index*65;if(local>0){int v=local*1000/900;if(v>1000)v=1000;q=v*v/1000;}}
 else if(elapsed<1800)q=1000;
 else if(elapsed<LD_DURATION)q=1000-smooth((elapsed-1800)*1000/(LD_DURATION-1800));
 return (LDPose){sx+(tx-sx)*q/1000,sy+(ty-sy)*q/1000,angles[index]*direction*q/1000};
}
void ld_format_time(int hour,int minute,bool use24,char digits[5],char period[3]){
 hour=(hour%24+24)%24;minute=(minute%60+60)%60;period[0]=0;int h=hour;
 if(!use24){h=hour%12;if(!h)h=12;period[0]=hour<12?'A':'P';period[1]='M';period[2]=0;}
 digits[0]=(!use24&&h<10)?' ':('0'+h/10);digits[1]='0'+h%10;digits[2]='0'+minute/10;digits[3]='0'+minute%10;digits[4]=0;
}

bool ld_knock_sample(LDKnock *g,int x,int y,int z,bool vibrated,bool enabled,bool busy,bool single,uint32_t now){
 if(!enabled||busy||vibrated){g->initialized=false;g->pending=false;return false;}
 if(!g->initialized){g->x=x;g->y=y;g->z=z;g->initialized=true;return false;}
 int delta=abs(x-g->x);if(abs(y-g->y)>delta)delta=abs(y-g->y);if(abs(z-g->z)>delta)delta=abs(z-g->z);
 g->x=x;g->y=y;g->z=z;
 if(g->cooling&&(int32_t)(now-g->cooldown_until)<0)return false;
 g->cooling=false;
 if(g->pending&&(uint32_t)(now-g->impact_at)>650)g->pending=false;
 if(delta<700)return false;
 uint32_t gap=now-g->impact_at;
 if(g->seen_impact&&gap<120)return false;
 bool fire=single||(g->pending&&gap<=650);
 g->seen_impact=true;g->impact_at=now;g->pending=!fire;
 if(fire){g->cooling=true;g->cooldown_until=now+LD_COOLDOWN;}
 return fire;
}

bool ld_background_is_light(int r,int g,int b){return 299*r+587*g+114*b>1500;}
