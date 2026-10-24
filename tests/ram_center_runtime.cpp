// Run the serialized RAM XS against independent engine state. This verifies
// deterministic contracts, not DE pathfinding, rendering or rule scheduling.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <iostream>
#include <map>
#include <string>
#include <vector>
struct Vec { float x,y,z; Vec(float x=0,float y=0,float z=0):x(x),y(y),z(z){} };
struct Object { int owner,type,kind,category; float hp; Vec position; int carrier=-1; int hero=0; };
std::map<int,Object> objects;
std::vector<std::vector<int>> arrays;
std::map<int,int> variables;
std::map<int,float> kills;
std::map<int,float> room;
struct Notice { int recipient,amount; float killsAfterAward; };
std::vector<Notice> notices;
int localPlayer=0;
std::vector<int> births,orders;
std::vector<int> ramMoves;
std::map<int,std::string> names;
std::map<std::pair<int,int>,float> properties;
using string=std::string;
int owners[9]={0,7,3,6,1,8,2,5,4};
int selectors[9]={0,6,8,4,7,1,5,3,2};
int nativeToWorld(int n){for(int c=1;c<=8;c++)if(selectors[c]==n)return owners[c];return 0;}
bool connected[9]={false,true,true,true,true,true,true,true,true};
int seconds=0,nextRef=200000,gCbaUnitByCiv=-1;
bool obstructed=false;
const int cHeroStatus=40,cAttributeKills=20,cSetUnitAttribute=10;
int xsArrayCreateInt(int n,int v,const char*){arrays.emplace_back(n,v);return arrays.size()-1;}
int xsArrayGetInt(int a,int n){return arrays.at(a).at(n);}
void xsArraySetInt(int a,int n,int v){arrays.at(a).at(n)=v;}
int xsArrayGetSize(int a){return arrays.at(a).size();}
int xsTriggerVariable(int v){return variables[v];}
int xsUnsyncGetLocalPlayerId(){return localPlayer;}
void xsChatData(const string& message,int amount){
    assert(message=="<YELLOW>Team center control: +%d kills!");
    notices.push_back(Notice{localPlayer,amount,kills[localPlayer]});
}
void xsSetTriggerVariable(int v,int n){variables[v]=n;}
int cbaWorldPlayerForColor(int c){int o=variables[137+c-1]-1000;return o>=1&&o<=8?o:0;}
bool xsDoesUnitExist(int r){return objects.count(r)&&objects.at(r).hp>0;}
int xsGetUnitOwner(int r){return objects.at(r).owner;}
float xsGetUnitHitpoints(int r){return objects.at(r).hp;}
int xsGetUnitObjectId(int r){return objects.at(r).type;}
int xsGetUnitClass(int r){return objects.at(r).kind;}
Vec xsGetUnitPosition(int r){return objects.at(r).position;}
Vec xsVectorSet(float x,float y,float z){return Vec(x,y,z);}
bool xsSetUnitPosition(int r,Vec position,bool collision){
    assert(!collision&&objects.at(r).owner==0);
    objects.at(r).position=position;ramMoves.push_back(r);return true;
}
float xsVectorGetX(Vec v){return v.x;}
float xsVectorGetY(Vec v){return v.y;}
float xsGetUnitProperty(int r,int p,int){
    if(p==5)return objects.at(r).carrier;
    if(p==10004)return objects.at(r).category;
    return properties[{r,p}];
}
bool xsSetUnitProperty(int r,int p,float value,int){properties[{r,p}]=value;return true;}
float xsGetUnitAttribute(int r,int a,int=-1){
    if(a==cHeroStatus)return objects.at(r).hero;
    assert(a==129);return properties[{r,a}];
}
void xsEffectAmount(int effect,int r,int attribute,float amount,int owner){
    assert(effect==cSetUnitAttribute&&attribute==129&&owner==0&&objects.at(r).owner==0);
    properties[{r,attribute}]=amount;
}
bool xsGetPlayerInGame(int o){return connected[o];}
int xsGetPlayerCivilization(int o){return o;}
int xsGetGameTime(){return seconds;}
int xsFloorToInt(float f){return std::floor(f);}
int xsCeilToInt(float f){return std::ceil(f);}
float xsAbs(float f){return std::abs(f);}
float xsMin(float a,float b){return std::min(a,b);}
float xsMax(float a,float b){return std::max(a,b);}
float xsPlayerAttribute(int o,int a){assert(a==cAttributeKills);return kills[o];}
int xsGetPlayerUnitIds(int o,int type,int a){
    arrays.at(a).clear();
    for(auto [r,u]:objects)if(u.owner==o&&(type<0||u.type==type))arrays.at(a).push_back(r);
    return a;
}
bool xsSetUnitOwner(int r,int o,bool flash){assert(!flash);objects.at(r).owner=o;return true;}
bool xsSetUnitName(int r,const string& s){names[r]=s;return true;}
bool xsRemoveUnit(int r){objects.at(r).hp=0;return true;}
bool cbaHasPopulationRoom(int o,int,int count){assert(count==1);return room[o]>=1;}
int xsCreateUnit(int t,int o,Vec p,bool,bool,bool collision){
    if(collision&&obstructed)return -1;
    int r=nextRef++;objects[r]=Object{o,t,930,70,100,p};
    if(o>0){assert(collision&&room[o]>=1);room[o]-=1;births.push_back(r);}
    return r;
}
void cbaOrderArmyBirth(int c,int slot,int r){assert(objects.at(r).owner==owners[c]);assert(slot>=0&&slot<4);orders.push_back(r);}
#include "ram-center.h"
#include "ram-native.h"
void reset(){
    objects.clear();arrays.clear();variables.clear();room.clear();kills.clear();births.clear();orders.clear();names.clear();
    properties.clear();
    notices.clear();ramMoves.clear();localPlayer=0;
    seconds=0;nextRef=200000;obstructed=false;
    gRamPresence=-1;gRamSurvey=-1;gRamLast=-1;gRamBalance=0;gRamOwner=0;gRamPayoutClock=0;
    gRamVoiceState=4;
    gCbaUnitByCiv=xsArrayCreateInt(9,4,"army");
    variables[56]=1;
    for(int c=1;c<=8;c++){
        variables[137+c-1]=1000+owners[c];variables[32+c-1]=1;variables[40+c-1]=selectors[c];
        connected[owners[c]]=true;room[owners[c]]=200;kills[owners[c]]=0;
    }
    #include "ram-initial.h"
}
int combat(int c,int kind=906,Vec p=Vec(72,72,-1),bool hero=false){
    int r=nextRef++;objects[r]=Object{owners[c],4,kind,70,100,p,-1,int(hero)};return r;
}
void advance(int count){for(int i=0;i<count;i++){seconds++;ramCenterTick();nativeCenterRewards();}}
int credit(int c){return variables[153+c-1];}
void teamwideSnapshotPayouts(){
    reset();combat(1);advance(179);
    for(int c=1;c<=8;c++)assert(credit(c)==0&&kills[owners[c]]==0);
    assert(variables[178]==100&&variables[169]==0&&variables[170]==1);
    assert(variables[171]==25&&variables[172]==0&&births.size()==4);
    advance(1);assert(gRamPayoutClock==0&&variables[170]==180&&notices.size()==4);
    for(int c=1;c<=4;c++){
        assert(credit(c)==25&&kills[owners[c]]==25);
        assert(notices[c-1].recipient==owners[c]&&notices[c-1].amount==25);
        assert(notices[c-1].killsAfterAward==25);
        assert(variables[189+selectors[c]-1]==25);
    }
    for(int c=5;c<=8;c++)assert(credit(c)==0&&kills[owners[c]]==0);
    // Backline teammates get kills, while the existing unit bonus is for holders.
    for(int r:births)assert(objects[r].owner==owners[1]);
    assert(orders==births&&variables[197]==1&&variables[198]==0);
    assert(objects[cRamTeamOneFlag].owner==0&&objects[cRamTeamTwoFlag].owner==0);
    assert(properties[std::make_pair(cRamTeamOneFlag,13)]==0);
    assert(properties[std::make_pair(cRamTeamTwoFlag,13)]==8);
    assert(names[cRamTeamOneFlag].find("100% | +25 kills per teammate")!=string::npos);
    advance(180);assert(notices.size()==8&&births.size()==8);
    for(int c=1;c<=4;c++)assert(credit(c)==50&&kills[owners[c]]==50);
    int value=credit(1),clock=gRamPayoutClock;ramCenterTick();
    assert(credit(1)==value&&gRamPayoutClock==clock); // No duplicate same-second tick.

    // The selected design is a snapshot, not accumulated or averaged control.
    reset();combat(1);combat(5);advance(179); // Entire window was neutral.
    gRamBalance=cRamControlScale*42/100;advance(1); // Contest reduces this to 125/300.
    assert(variables[178]==70&&variables[169]==30&&variables[175]==10);
    for(int c=1;c<=4;c++)assert(kills[owners[c]]==10);
    for(int c=5;c<=8;c++)assert(kills[owners[c]]==0);
    reset();combat(1);advance(179);gRamBalance=0;combat(5);advance(1);
    assert(notices.empty()); // Strong earlier control cannot pay at 50/50.
}
void payoutScale(){
    reset();
    // Explicit user examples, for either team. Minority and empty teams get zero.
    int lead[]={0,10,20,40,50,60,80,100};
    int amount[]={0,2,5,10,12,15,20,25};
    for(int i=0;i<8;i++){
        gRamBalance=cRamControlScale*lead[i]/100;
        assert(ramIncomeFor(1,1)==amount[i]&&ramIncomeFor(2,1)==0);
        assert(ramIncomeFor(1,0)==0);
        gRamBalance=0-gRamBalance;
        assert(ramIncomeFor(2,1)==amount[i]&&ramIncomeFor(1,1)==0);
        assert(ramIncomeFor(2,0)==0);
    }
}
void contestedEqualization(){
    reset();combat(1);advance(180);combat(8,925,Vec(72,72,-1),true);
    for(int i=0;i<100;i++)combat(1); // A huge army cannot overpower a contested point.
    int count=births.size();advance(60);
    assert(gRamBalance==cRamControlScale*80/100);
    assert(variables[178]==90&&variables[169]==10&&variables[171]==20);
    assert(variables[177]==3&&variables[205]==3);
    advance(120);assert(variables[178]==70&&variables[169]==30);
    for(int c=1;c<=4;c++)assert(credit(c)==35&&kills[owners[c]]==35);
    for(int c=5;c<=8;c++)assert(credit(c)==0);
    assert(births.size()==count);
    advance(120);assert(gRamBalance==0&&gRamOwner==0);
    assert(variables[178]==50&&variables[169]==50&&variables[171]==0&&variables[172]==0);
    advance(360); // Neutral contest stays neutral indefinitely, without minimum rewards.
    for(int c=1;c<=4;c++)assert(credit(c)==35);
    for(int c=5;c<=8;c++)assert(credit(c)==0);
    // Team 2 gains control only after Team 1 actually leaves.
    for(auto& [r,u]:objects)if(u.owner==owners[1]&&u.kind==906)u.hp=0;
    advance(60);assert(gRamBalance==0-cRamControlScale&&variables[172]==25);
    advance(120);for(int c=5;c<=8;c++)assert(credit(c)==25&&kills[owners[c]]==25);

    // Symmetric approach to neutral from the other side, with no crossing.
    reset();combat(8);advance(60);combat(1);
    advance(299);assert(gRamBalance==-1);advance(1);assert(gRamBalance==0);
    advance(50);assert(gRamBalance==0);
    // Reversing full enemy control takes two capture intervals.
    reset();int holder=combat(1);advance(60);objects[holder].hp=0;combat(5);
    advance(60);assert(gRamBalance==0&&variables[171]==0&&variables[172]==0);
    advance(60);assert(gRamBalance==0-cRamControlScale&&variables[172]==25);
}
void filteringAndIdentity(){
    reset();
    for(int c=1;c<=8;c++){
        combat(c,904);combat(c,959);combat(c,930);combat(c,938); // Villager, King, flag, bird.
        int a=combat(c);objects[a].hp=0;
        int b=combat(c);objects[b].carrier=99;
        int d=combat(c);objects[d].category=80;
    }
    advance(180);assert(gRamBalance==0&&births.empty()&&notices.empty());
    int r=combat(8);advance(59);assert(gRamBalance>0-cRamControlScale);
    assert(variables[205]==0); // Merely leading is not a full-capture voice event.
    advance(1);assert(gRamBalance==0-cRamControlScale&&variables[168]==1&&variables[205]==2);
    assert(ramPresenceFor(8)==1&&ramPresenceFor(4)==0);
    objects[r].position=Vec(64.9,72,-1);assert(ramPresenceFor(8)==0);
    objects[r].position=Vec(65,78.99,-1);assert(ramPresenceFor(8)==1);
    objects[r].position=Vec(79,72,-1);assert(ramPresenceFor(8)==0);
    objects[r].position=Vec(72,72,-1);
    objects[r].owner=owners[1];assert(ramPresenceFor(8)==0&&ramPresenceFor(1)==1);
    variables[32]=0;assert(ramPresenceFor(1)==0);
    variables[32]=1;variables[137]=0;assert(ramPresenceFor(1)==0);
    variables[137]=1000+owners[1];connected[owners[1]]=false;assert(ramPresenceFor(1)==0);
    reset();variables[33]=0;connected[owners[3]]=false;variables[140]=0;
    combat(1);advance(180);assert(credit(1)==25&&notices.size()==1);
    for(int c=2;c<=8;c++)assert(credit(c)==0);
    // A defeat between queueing and native delivery blocks the actual kill effect.
    reset();variables[33]=0;variables[181]=25;nativeCenterRewards();
    assert(kills[owners[2]]==0&&notices.empty());advance(1);assert(variables[181]==0);
}
void boundedDeliveryAndReset(){
    reset();combat(1);room[owners[1]]=0;advance(500);
    assert(births.empty()&&xsArrayGetInt(gRamPending,1)==4&&variables[197]==0);
    room[owners[1]]=2;advance(1);assert(births.size()==2&&xsArrayGetInt(gRamPending,1)==2);
    assert(variables[197]==1);variables[197]=0;
    room[owners[1]]=20;obstructed=true;advance(20);assert(births.size()==2);
    obstructed=false;advance(1);assert(births.size()==4&&xsArrayGetInt(gRamPending,1)==0);
    assert(variables[197]==0); // The rest of a partial packet cannot repeat its voice.
    advance(119);assert(births.size()==4);advance(1);assert(births.size()==8);
    xsArraySetInt(gRamPending,1,4);combat(5);advance(1);assert(births.size()==8);
    advance(299);assert(gRamBalance==0&&xsArrayGetInt(gRamPending,1)==0);
    // Empty control decays slowly, pays nothing, and never produces armies.
    reset();int r=combat(1);advance(180);objects[r].position=Vec(0,0,-1);
    advance(1);assert(variables[171]==0&&variables[172]==0);
    advance(299);assert(gRamBalance==0&&gRamOwner==0&&variables[205]==4);
    assert(births.size()==4&&credit(1)==25&&xsArrayGetInt(gRamPending,1)==0);
    int clock=gRamPayoutClock;seconds+=1000;ramCenterTick();
    assert(gRamPayoutClock==clock+1); // A gap is one observation, never fabricated ownership.
}
void payoutNotifications(){
    reset();
    // Native selectors and XS/local player ids are independently shuffled.
    // Every recipient sees their own actual award, including uneven amounts.
    for(int color=1;color<=8;color++)variables[180+color-1]=color;
    nativeCenterRewards();assert(notices.size()==8);
    for(int color=1;color<=8;color++){
        const auto& notice=notices[color-1];
        assert(notice.recipient==owners[color]&&notice.amount==color);
        assert(notice.killsAfterAward==color&&variables[180+color-1]==0);
    }
    nativeCenterRewards();assert(notices.size()==8);
    localPlayer=owners[1];ramAnnounceCenterKills(1);ramAnnounceCenterKills(0);
    ramAnnounceCenterKills(9);assert(notices.size()==8);
}
void physicalControlMeter(){
    reset();
    const int reference=cRamCenterRam;
    const size_t initialObjects=objects.size();
    auto at=[&](float x){
        Vec p=objects.at(reference).position;
        assert(std::abs(p.x-x)<0.0001f&&std::abs(p.y-cRamCenterRamY)<0.0001f);
        assert(objects.at(reference).owner==0&&objects.at(reference).hp>0);
    };
    // Placed once at neutral. Gaia never supplies presence or player kill credit.
    at(cRamCenterRamMidX);advance(1);at(cRamCenterRamMidX);
    assert(variables[173]==0&&variables[174]==0&&births.empty());
    for(int c=1;c<=8;c++)assert(credit(c)==0);
    combat(1);advance(30);
    at(cRamCenterRamMidX-cRamCenterRamHalfTravel/2);
    advance(30);at(cRamCenterRamMidX-cRamCenterRamHalfTravel);
    assert(objects.size()==initialObjects+1&&ramMoves.size()==61);
    for(int r:ramMoves)assert(r==reference);
    // Contest moves gradually toward the middle on the existing 300s clock.
    combat(5);advance(150);at(cRamCenterRamMidX-cRamCenterRamHalfTravel/2);
    advance(150);at(cRamCenterRamMidX);
    advance(60);at(cRamCenterRamMidX);
    // Team2 reaches the other existing flag after Team1 leaves.
    for(auto& [r,u]:objects)if(u.owner==owners[1]&&u.kind==906)u.hp=0;
    advance(60);at(cRamCenterRamMidX+cRamCenterRamHalfTravel);
    assert(std::abs(objects.at(reference).position.x-objects.at(cRamTeamTwoFlag).position.x)<0.0001f);
    // Rendering bounds remain safe even for a corrupted/restored out-of-range value.
    gRamBalance=cRamControlScale*2;ramMoveCenterRam();
    at(cRamCenterRamMidX-cRamCenterRamHalfTravel);
    gRamBalance=0-cRamControlScale*2;ramMoveCenterRam();
    at(cRamCenterRamMidX+cRamCenterRamHalfTravel);
    // Exact reference and engine flags survive continued execution after a save.
    reset();combat(1);advance(20);
    auto savedObjects=objects;
    int savedBalance=gRamBalance,savedLast=gRamLast,savedClock=gRamPayoutClock;
    advance(10);
    objects=savedObjects;gRamBalance=savedBalance;gRamLast=savedLast;
    gRamPayoutClock=savedClock;seconds=savedLast;
    size_t count=ramMoves.size();ramCenterTick();
    assert(ramMoves.size()==count&&gRamBalance==savedBalance&&gRamPayoutClock==savedClock);
    advance(1);
    at(cRamCenterRamMidX-cRamCenterRamHalfTravel*21/60);
    assert(ramMoves.back()==reference);
    // Explicit native properties prevent capture/deletion/targeting/selection.
    objects.at(reference).owner=owners[7];
    for(int property=6;property<=10;property++)properties[{reference,property}]=1;
    ramProtectCenterRam();assert(objects.at(reference).owner==0);
    assert(properties[std::make_pair(reference,129)]==1.0f);
    for(int property=6;property<=10;property++)assert(properties[std::make_pair(reference,property)]==0);
    assert(properties[std::make_pair(reference,11)]==3);
    // Missing reference is never replaced or silently counted as a reinforcement.
    objects.erase(reference);count=objects.size();int next=nextRef;
    ramMoveCenterRam();assert(objects.size()==count&&nextRef==next);
}
int main(){teamwideSnapshotPayouts();payoutScale();contestedEqualization();filteringAndIdentity();boundedDeliveryAndReset();
    payoutNotifications();physicalControlMeter();
    std::cout<<"RAM center contracts passed\n";}
