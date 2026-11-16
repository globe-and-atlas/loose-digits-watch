#include <pebble.h>
#include "motion.h"
#include "config.h"
static Window *s_window;static Layer *s_layer;static AppTimer *s_timer;
static LDKnock s_knock;
static int s_trigger=0;
static uint32_t s_background=0xFFFFAA,s_foreground=0x000000,s_accent=0xFF5500;
static LDGesture s_gesture;static bool s_motion=true,s_active=false,s_focus=true;
static int s_date=0,s_direction=1;static uint32_t s_start,s_elapsed;
static char s_digits[5],s_period[3],s_detail[16];
#if LD_FIXTURE
static int s_hour=10,s_minute=42,s_format=2,s_frame=-1;
#endif
static const uint8_t DIGITS[10][7]={
 {14,17,19,21,25,17,14},{4,12,4,4,4,4,14},{14,17,1,2,4,8,31},
 {30,1,1,14,1,1,30},{2,6,10,18,31,2,2},{31,16,16,30,1,1,30},
 {14,16,16,30,17,17,14},{31,1,2,4,8,8,8},{14,17,17,14,17,17,14},
 {14,17,17,15,1,1,14}};
static uint32_t now_ms(void){time_t s;uint16_t ms;time_ms(&s,&ms);return (uint32_t)s*1000+ms;}
static void refresh(void){
 time_t now=time(NULL);struct tm *value=localtime(&now);if(!value)return;
 struct tm local=*value;bool use24=clock_is_24h_style();
#if LD_FIXTURE
 local.tm_hour=s_hour;local.tm_min=s_minute;local.tm_year=126;local.tm_mon=10;local.tm_mday=7;use24=s_format==2;
#endif
 ld_format_time(local.tm_hour,local.tm_min,use24,s_digits,s_period);s_detail[0]=0;
 if(s_date)strftime(s_detail,sizeof(s_detail),s_date==1?"%Y-%m-%d":s_date==2?"%m/%d/%Y":"%d/%m/%Y",&local);
}
static void stop_motion(void){if(s_timer){app_timer_cancel(s_timer);s_timer=NULL;}s_active=false;s_elapsed=0;refresh();if(s_layer)layer_mark_dirty(s_layer);}
static void animate(void *context){
 (void)context;s_timer=NULL;s_elapsed=now_ms()-s_start;
 if(s_elapsed>=LD_DURATION){stop_motion();return;}
 layer_mark_dirty(s_layer);s_timer=app_timer_register(50,animate,NULL);if(!s_timer)stop_motion();
}
static void start_motion(int direction){
 if(!s_motion||s_active||!s_focus)return;
 s_direction=direction;s_start=now_ms();s_elapsed=0;s_active=true;
 s_timer=app_timer_register(50,animate,NULL);if(!s_timer)stop_motion();
}
static void sample(AccelData *samples,uint32_t count){
#if LD_FIXTURE
 static int last_x=9999;static bool last_focus=false;
 if(count&&(samples[0].x!=last_x||s_focus!=last_focus)){APP_LOG(APP_LOG_LEVEL_INFO,"LD x=%d z=%d vib=%d focus=%d motion=%d busy=%d",samples[0].x,samples[0].z,samples[0].did_vibrate,s_focus,s_motion,s_active);last_x=samples[0].x;last_focus=s_focus;}
#endif
 for(uint32_t i=0;i<count;i++){
  AccelData a=samples[i];bool fire=false;
  if(s_trigger==2)fire=ld_sample(&s_gesture,a.x,a.z,a.did_vibrate,s_motion&&s_focus,s_active,now_ms());
  else fire=ld_knock_sample(&s_knock,a.x,a.y,a.z,a.did_vibrate,s_motion&&s_focus,s_active,s_trigger==1,(uint32_t)a.timestamp);
#if LD_FIXTURE
  if(a.y>900||fire)APP_LOG(APP_LOG_LEVEL_INFO,"LD knock y=%d time=%lu fire=%d mode=%d",a.y,(unsigned long)a.timestamp,fire,s_trigger);
#endif
  if(fire)start_motion(a.x<0?-1:1);
 }
}
// Inverse-map the whole glyph so rotation never creates seams between its cells.
static void draw_digit(GContext *ctx,char digit,LDPose p,int cell){
 if(digit<'0'||digit>'9')return;
 const uint8_t *bits=DIGITS[digit-'0'];
 if(!p.angle){
  for(int row=0;row<7;row++)for(int col=0;col<5;col++)if(bits[row]&(1<<(4-col)))
   graphics_fill_rect(ctx,GRect(p.x+col*cell-5*cell/2,p.y+row*cell-7*cell/2,cell,cell),0,GCornerNone);
  return;
 }
 int32_t angle=p.angle*TRIG_MAX_ANGLE/360,co=cos_lookup(angle),si=sin_lookup(angle);
 int radius=cell*5;
 for(int dy=-radius;dy<=radius;dy++){
  int run=-radius-1;
  for(int dx=-radius;dx<=radius+1;dx++){
   int x=(dx*co+dy*si)/TRIG_MAX_RATIO+5*cell/2;
   int y=(-dx*si+dy*co)/TRIG_MAX_RATIO+7*cell/2;
   bool ink=dx<=radius&&x>=0&&x<5*cell&&y>=0&&y<7*cell&&(bits[y/cell]&(1<<(4-x/cell)));
   if(ink&&run==-radius-1)run=dx;
   if(!ink&&run!=-radius-1){graphics_fill_rect(ctx,GRect(p.x+run,p.y+dy,dx-run,1),0,GCornerNone);run=-radius-1;}
  }
 }
}
static void update(Layer *layer,GContext *ctx){
 GRect b=layer_get_bounds(layer);int w=b.size.w,h=b.size.h,cell=(w-24)/26;
 GColor bg=GColorFromHEX(s_background),fg=GColorFromHEX(s_foreground),accent=GColorFromHEX(s_accent);
 // Keep the clock readable if requested colors quantize to the same palette entry.
 if(fg.argb==bg.argb)fg=ld_background_is_light(bg.r,bg.g,bg.b)?GColorBlack:GColorWhite;
 if(accent.argb==bg.argb)accent=fg;
 graphics_context_set_fill_color(ctx,bg);graphics_fill_rect(ctx,b,0,GCornerNone);
 graphics_context_set_fill_color(ctx,fg);uint32_t elapsed=s_active?s_elapsed:LD_DURATION;
#if LD_FIXTURE
 if(s_frame>=0)elapsed=s_frame;
#endif
 int shift=s_digits[0]==' '?3*cell:0;
 for(int i=0;i<4;i++){LDPose pose=ld_pose(i,w,h,elapsed,s_direction);pose.x-=shift;draw_digit(ctx,s_digits[i],pose,cell);}
 LDPose a=ld_pose(1,w,h,elapsed,s_direction),z=ld_pose(2,w,h,elapsed,s_direction);
 int cx=(a.x+z.x)/2-shift,cy=(a.y+z.y)/2;graphics_context_set_fill_color(ctx,accent);
 graphics_fill_rect(ctx,GRect(cx-cell/3,cy-cell,cell*2/3,cell*2/3),0,GCornerNone);
 graphics_fill_rect(ctx,GRect(cx-cell/3,cy+cell/2,cell*2/3,cell*2/3),0,GCornerNone);
 graphics_context_set_text_color(ctx,fg);
 if(s_period[0])graphics_draw_text(ctx,s_period,fonts_get_system_font(FONT_KEY_GOTHIC_18_BOLD),GRect(0,h*23/100,w,22),GTextOverflowModeTrailingEllipsis,GTextAlignmentCenter,NULL);
 if(s_detail[0])graphics_draw_text(ctx,s_detail,fonts_get_system_font(FONT_KEY_GOTHIC_18_BOLD),GRect(0,h*82/100,w,23),GTextOverflowModeTrailingEllipsis,GTextAlignmentCenter,NULL);
}
static void tick(struct tm *tm,TimeUnits units){(void)tm;(void)units;refresh();layer_mark_dirty(s_layer);}
static void subscribe_motion(void){accel_data_service_unsubscribe();s_gesture=(LDGesture){0};s_knock=(LDKnock){0};if(s_motion&&s_focus){accel_data_service_subscribe(5,sample);accel_service_set_sampling_rate(ACCEL_SAMPLING_50HZ);}}
static void focus(bool focused){s_focus=focused;if(!focused)stop_motion();subscribe_motion();}
static void inbox(DictionaryIterator *iter,void *context){
 (void)context;Tuple *t;
 if((t=dict_find(iter,MESSAGE_KEY_Motion))&&(t->type==TUPLE_INT||t->type==TUPLE_UINT)&&t->value->int32>=0&&t->value->int32<=1){s_motion=t->value->int32;persist_write_int(1,s_motion);stop_motion();subscribe_motion();}
 if((t=dict_find(iter,MESSAGE_KEY_DateFormat))&&(t->type==TUPLE_INT||t->type==TUPLE_UINT)&&t->value->int32>=0&&t->value->int32<=3){s_date=t->value->int32;persist_write_int(2,s_date);}
 if((t=dict_find(iter,MESSAGE_KEY_Trigger))&&(t->type==TUPLE_INT||t->type==TUPLE_UINT)&&t->value->int32>=0&&t->value->int32<=2){s_trigger=t->value->int32;persist_write_int(3,s_trigger);stop_motion();subscribe_motion();}
 const uint32_t keys[]={MESSAGE_KEY_Background,MESSAGE_KEY_Foreground,MESSAGE_KEY_Accent};
 uint32_t *colors[]={&s_background,&s_foreground,&s_accent};
 for(int i=0;i<3;i++)if((t=dict_find(iter,keys[i]))&&(t->type==TUPLE_INT||t->type==TUPLE_UINT)&&t->value->int32>=0&&t->value->int32<=0xFFFFFF){*colors[i]=t->value->int32;persist_write_int(4+i,*colors[i]);}
#if LD_FIXTURE
 if((t=dict_find(iter,11000)))s_hour=t->value->int32;
 if((t=dict_find(iter,11001)))s_minute=t->value->int32;
 if((t=dict_find(iter,11002)))s_format=t->value->int32;
 if((t=dict_find(iter,11003)))s_frame=t->value->int32;
 if((t=dict_find(iter,11004)))s_direction=t->value->int32<0?-1:1;
 if((t=dict_find(iter,11005))){s_frame=-1;start_motion(1);}
#endif
 refresh();layer_mark_dirty(s_layer);
}
static void load(Window *window){s_layer=layer_create(layer_get_bounds(window_get_root_layer(window)));layer_set_update_proc(s_layer,update);layer_add_child(window_get_root_layer(window),s_layer);refresh();}
static void unload(Window *window){(void)window;layer_destroy(s_layer);s_layer=NULL;}
static void init(void){
 if(persist_exists(1))s_motion=persist_read_int(1)!=0;
 if(persist_exists(2)){int v=persist_read_int(2);s_date=v>=0&&v<=3?v:0;}
 if(persist_exists(3)){int v=persist_read_int(3);s_trigger=v>=0&&v<=2?v:0;}
 uint32_t *colors[]={&s_background,&s_foreground,&s_accent};
 for(int i=0;i<3;i++)if(persist_exists(4+i)){int v=persist_read_int(4+i);if(v>=0&&v<=0xFFFFFF)*colors[i]=v;}
 s_window=window_create();window_set_window_handlers(s_window,(WindowHandlers){.load=load,.unload=unload});window_stack_push(s_window,true);
 tick_timer_service_subscribe(MINUTE_UNIT,tick);app_message_register_inbox_received(inbox);app_message_open(256,256);app_focus_service_subscribe(focus);subscribe_motion();
}
static void deinit(void){stop_motion();accel_data_service_unsubscribe();app_focus_service_unsubscribe();tick_timer_service_unsubscribe();app_message_deregister_callbacks();window_destroy(s_window);}
int main(void){init();app_event_loop();deinit();}
