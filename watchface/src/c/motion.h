#pragma once
#include <stdint.h>
#include <stdbool.h>
#define LD_DURATION 3000
#define LD_COOLDOWN 5000
typedef struct { bool armed, cooling; uint8_t neutral, rolled; uint32_t cooldown_until; } LDGesture;
typedef struct { int16_t x,y,angle; } LDPose;
bool ld_sample(LDGesture *g,int x,int z,bool vibrated,bool enabled,bool busy,uint32_t now);
LDPose ld_pose(int index,int width,int height,uint32_t elapsed,int direction);
void ld_format_time(int hour,int minute,bool use24,char digits[5],char period[3]);

// Axis-independent case knocks: suppress rebound; pair deliberate impacts.
typedef struct {bool initialized,pending,seen_impact,cooling;int x,y,z;uint32_t impact_at,cooldown_until;} LDKnock;
bool ld_knock_sample(LDKnock *g,int x,int y,int z,bool vibrated,bool enabled,bool busy,bool single,uint32_t now);

bool ld_background_is_light(int r,int g,int b);
