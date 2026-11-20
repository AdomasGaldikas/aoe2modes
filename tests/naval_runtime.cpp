// Execute the serialized XS and native defeat effects with engine API mocks.
#include <cassert>
#include <cmath>
#include <cstring>
#include <map>
#include <vector>
#include <algorithm>
struct Vec {
    double x,y,z;
    Vec(double a=0,double b=0,double c=0):x(a),y(b),z(c) {}
};
#include "naval-map.h"
struct Object { int owner,type; float hp; Vec point; float buildpoints=35; };
std::map<int,Object> objects;
std::vector<std::vector<int>> ints;
std::vector<std::vector<Vec>> vectors;
std::map<std::pair<int,int>,int> attributes,vision;
std::map<int,int> variables;
std::map<std::pair<int,int>,bool> available;
std::vector<int> births,orders;
std::map<int,Vec> clearanceOrders;
std::vector<std::pair<int,int>> deferredOrders;
std::vector<Vec> attemptedPoints;
int owners[9]={0,7,0,0,0,2,0,0,0};
int selectors[9]={-1,2,-1,-1,-1,7,-1,-1,-1};
int seconds=0,nextRef=900000;
bool createFails=false,inGame[9]={false,false,true,false,false,false,false,true,false};
int blockedDock=-1;
const int cAttributeKills=20,cAttributeKilledByOthers=154,cAttributeRazings=43;
const int cAttributeMilitaryPopulation=40,cAttributeTotalValueOfKills=170;
const int cAttributeValueKilledByOthers=152,cAttributeTotalValueOfRazings=172,cHitpoints=0;
const int cAttributeWood=1,cAttributeStone=2,cEnableObject=2,cTrainTime=101;
int xsArrayCreateInt(int n,int value,const char*) {
    ints.push_back(std::vector<int>(n,value));return ints.size()-1;
}
int xsArrayCreateVector(int n,Vec value,const char*) {
    vectors.push_back(std::vector<Vec>(n,value));return vectors.size()-1;
}
int xsArrayGetInt(int a,int i){return ints.at(a).at(i);}
void xsArraySetInt(int a,int i,int v){ints.at(a).at(i)=v;}
int xsArrayGetSize(int a){return ints.at(a).size();}
Vec xsArrayGetVector(int a,int i){return vectors.at(a).at(i);}
void xsArraySetVector(int a,int i,Vec v){vectors.at(a).at(i)=v;}
bool xsDoesUnitExist(int ref){return objects.count(ref)&&objects.at(ref).hp>0;}
int xsGetUnitOwner(int ref){return objects.at(ref).owner;}
float xsGetUnitHitpoints(int ref){return objects.at(ref).hp;}
Vec xsGetUnitPosition(int ref){return objects.at(ref).point;}
double xsVectorGetX(Vec v){return v.x;}
double xsVectorGetY(Vec v){return v.y;}
Vec xsVectorSet(double x,double y,double z){return Vec(x,y,z);}
bool xsGetPlayerInGame(int owner){return owner>0&&owner<=8&&inGame[owner];}
int xsGetWorldPlayerId(int selector){return selectors[selector];}
int xsCeilToInt(double v){return std::ceil(v);}
// Real API contract: these are seconds; only xsGetWorldTime is milliseconds.
int xsGetTime(){return seconds-1;}
int xsGetGameTime(){return seconds;}
float bitCastToFloat(int bits){float v;std::memcpy(&v,&bits,4);return v;}
void xsSetPlayerAttribute(int owner,int attr,float value){
    if(attr==285||attr==286){int bits;std::memcpy(&bits,&value,4);vision[{owner,attr}]=bits;}
    else attributes[{owner,attr}]=value;
}
float xsGetUnitAttribute(int,int attr){return attr==cTrainTime?35:100;}
float xsGetUnitBuildPoints(int ref){return objects.at(ref).buildpoints;}
int xsGetPlayerUnitIds(int owner,int type,int array){
    ints.at(array).clear();
    for(auto [ref,u]:objects)if(u.owner==owner&&u.type==type&&u.hp>0)ints.at(array).push_back(ref);
    return array;
}
bool xsRemoveUnit(int ref){if(!xsDoesUnitExist(ref))return false;objects.at(ref).hp=0;return true;}
void xsEffectAmount(int command,int type,int unused,int value,int owner){
    assert(command==cEnableObject&&unused==0);available[{owner,type}]=value;
}
float xsSetUnitHitpoints(int ref,float hp){objects.at(ref).hp=hp;return hp;}
void xsChatData(const char*){}
void xsSetTriggerVariable(int id,int value){variables[id]=value;}
bool isShip(Object u){return u.type!=12&&u.type!=45&&u.type!=234&&u.type!=79&&u.type!=87&&u.type!=83&&u.type!=4;}
int xsPlayerAttribute(int owner,int attr){
    if(attr==cAttributeMilitaryPopulation){
        int count=0;for(auto [ref,u]:objects)if(u.owner==owner&&u.hp>0&&(isShip(u)||u.type==4))count++;
        return count;
    }
    return attributes[{owner,attr}];
}
int xsCreateUnit(int type,int owner,Vec point,bool,bool,bool collision){
    assert(collision);attemptedPoints.push_back(point);if(createFails)return -1;
    if(isShip(Object{owner,type,100,point}))assert(waterAt(point));
    for(auto [ref,u]:objects)if(u.hp>0&&u.type==45
        && std::abs(u.point.x-point.x)<2&&std::abs(u.point.y-point.y)<2)return -1;
    if(blockedDock>=0){
        Vec p=objects.at(blockedDock).point;
        double dx=p.x-point.x,dy=p.y-point.y;
        if(dx*dx+dy*dy<=16)return -1;
    }
    int ref=nextRef++;objects[ref]=Object{owner,type,100,point};births.push_back(ref);return ref;
}
void xsTaskUnits(int array,int action,Vec destination,int object,bool queued,bool formation,bool,int){
    int ref=xsArrayGetInt(array,0);
    assert(!formation&&object==-1&&waterAt(destination));
    if(action==1){
        assert(!queued);
        Vec birth=objects.at(ref).point;
        double dx=birth.x-destination.x,dy=birth.y-destination.y;
        assert(dx*dx+dy*dy>0&&dx*dx+dy*dy<=36);
        clearanceOrders[ref]=destination;
    }else{
        assert(action==17&&queued);
        assert(!orders.empty()&&orders.back()==ref&&clearanceOrders.count(ref));
        assert(destination.x==72.5&&destination.y==72.5);
    }
    orders.push_back(ref);
    deferredOrders.push_back({array,ref});
}
void nativeRemove(int selector){
    for(auto& [ref,u]:objects)if(u.owner==xsGetWorldPlayerId(selector))u.hp=0;
}
void nativeDefeat(int selector){inGame[xsGetWorldPlayerId(selector)]=false;}
#include "naval-runtime.h"
#include "naval-effects.h"
int port(int c,int s){return xsArrayGetInt(gPorts,c*4+s);}
int ship(int c,int s){return xsArrayGetInt(gShips,c*FLEET_CAP+s);}
void flushOrders(){
    for(auto [array,expected]:deferredOrders)assert(xsArrayGetInt(array,0)==expected);
    deferredOrders.clear();
}
void tick(int t){flushOrders();seconds=t;navalTick();flushOrders();}
void seed(){
    #include "naval-initial.h"
}
void reset(){
    objects.clear();ints.clear();vectors.clear();births.clear();orders.clear();attributes.clear();vision.clear();
    available.clear();variables.clear();deferredOrders.clear();clearanceOrders.clear();
    attemptedPoints.clear();blockedDock=-1;createFails=false;
    gReady=false;gMatchStarted=false;gWinner=0;gWinSince=-1;gLastTick=-1;
}
void fresh(){
    reset();
    for(int c=0;c<9;c++){owners[c]=0;selectors[c]=-1;inGame[c]=false;}
    owners[1]=7;owners[5]=2;selectors[1]=2;selectors[5]=7;inGame[2]=inGame[7]=true;
    seed();navalMain();
}
int born(int owner,int type=-1){
    return std::count_if(births.begin(),births.end(),[=](int ref){
        return objects.at(ref).owner==owner&&(type<0||objects.at(ref).type==type);
    });
}
int main(){
    fresh();assert(!navalClosed1()&&!navalOccupied1()&&!navalDefeat1W5());
    assert(!navalBirth(1,539,0,false));
    tick(0);tick(2);assert(!gReady&&births.empty());tick(3);
    assert(gReady&&gMatchStarted&&gWinner==0&&births.empty()&&orders.empty());
    assert(xsArrayGetInt(gOwners,1)==7&&xsArrayGetInt(gOwners,5)==2);
    assert(navalOccupied1()&&navalOccupied5()&&!navalOccupied8());
    assert(navalClosed8()&&!navalClosed1());
    assert(vision.at({7,285})==(1<<7)&&vision.at({2,286})==(1<<2));
    assert(isShip(objects.at(ship(1,0)))&&!navalBirth(1,250,0,true));
    // No ordinary opening fleet. All regular and siege births obey the same 15s clock.
    for(int t=4;t<18;t++)tick(t);assert(births.empty());tick(18);
    assert(born(7)==4&&born(2)==4&&orders.size()==16);
    for(int r:births){
        bool near=false;int c=objects.at(r).owner==7?1:5;
        for(int p=0;p<4;p++){
            Vec dock=objects.at(port(c,p)).point,boat=objects.at(r).point;
            double dx=dock.x-boat.x,dy=dock.y-boat.y;
            near=near||std::abs(dx*dx+dy*dy-9)<0.0001;
        }
        assert(near); // Actual own producer, not a fixed remote pad.
    }
    auto count=births.size();tick(18);tick(17);assert(births.size()==count);
    births.clear();orders.clear();objects.at(port(1,0)).hp=0;
    for(int t=19;t<33;t++)tick(t);assert(births.empty());tick(33);
    assert(navalPorts(1)==3&&born(7)==3&&born(2)==4&&orders.size()==14);
    assert(std::none_of(orders.begin(),orders.end(),[](int r){return r<900000;}));
    // Ordinary tiers, real K/D/R and fractional slow healing with no stacked ports.
    attributes[{7,cAttributeKills}]=20;attributes[{7,cAttributeKilledByOthers}]=5;attributes[{7,22}]=99;
    int repairShip=ship(1,1);objects.at(repairShip).hp=50.5;tick(34);
    assert(navalRank(1)==1&&variables.at(1)==20&&variables.at(2)==5&&variables.at(4)==1);
    assert(attributes.at({7,170})==2000&&attributes.at({7,152})==500&&attributes.at({7,22})==0);
    assert(objects.at(repairShip).hp==51.5);tick(34);assert(objects.at(repairShip).hp==51.5);
    for(int t=35;t<=43;t++)tick(t);assert(objects.at(repairShip).hp==60.5);
    objects.at(repairShip).hp=99.5;tick(44);assert(objects.at(repairShip).hp==100);
    objects.at(repairShip).hp=50;objects.at(repairShip).point=Vec(72.5,72.5,-1);
    tick(45);assert(objects.at(repairShip).hp==50);
    births.clear();for(int t=46;t<=48;t++)tick(t);
    assert(born(7)==3&&born(7,21)>0); // New rank changes the wave, never creates bonus ships.

    // A large siege bank never drains one ship per heartbeat or increases wave size.
    fresh();tick(3);attributes[{7,cAttributeRazings}]=20;
    for(int t=4;t<18;t++)tick(t);
    assert(births.empty()&&xsArrayGetInt(gPendingCannons,1)==20);
    tick(18);assert(born(7)==4&&born(7,420)==1&&xsArrayGetInt(gPendingCannons,1)==19);
    births.clear();for(int t=19;t<33;t++)tick(t);assert(births.empty());tick(33);
    assert(born(7)==4&&born(7,420)==1&&xsArrayGetInt(gPendingCannons,1)==18);
    births.clear();createFails=true;tick(48);
    assert(births.empty()&&xsArrayGetInt(gPendingCannons,1)==18);
    createFails=false;tick(49);assert(births.empty());tick(63);
    assert(born(7)==4&&born(7,420)==1&&xsArrayGetInt(gPendingCannons,1)==17);

    // Hero death cooldown, current-tier return, cap/placement retry and manual control.
    fresh();tick(3);int hero=ship(1,0);objects.at(hero).hp=0;tick(4);
    assert(xsArrayGetInt(gNextFlagship,1)==34);
    attributes[{7,cAttributeKills}]=120;
    for(int t=5;t<=33;t++)tick(t);assert(xsArrayGetInt(gFlagship,1)==hero);
    createFails=true;tick(34);assert(xsArrayGetInt(gFlagship,1)==hero);
    createFails=false;int capShip=-1;
    while(xsPlayerAttribute(7,cAttributeMilitaryPopulation)<FLEET_CAP){
        capShip=nextRef++;objects[capShip]=Object{7,539,100,Vec(72,72,-1)};
    }
    tick(35);assert(xsArrayGetInt(gFlagship,1)==hero&&xsArrayGetInt(gNextFlagship,1)==34);
    objects.at(capShip).hp=0;orders.clear();tick(36);int replacement=xsArrayGetInt(gFlagship,1);
    assert(replacement!=hero&&objects.at(replacement).type==844&&orders.empty());
    Vec berth=xsArrayGetVector(gHeroPads,1),actual=objects.at(replacement).point;
    assert(berth.x==actual.x&&berth.y==actual.y&&!navalBirth(1,844,0,true));
    assert(xsArrayGetInt(gNextFlagship,1)==0);

    // Practice: two actual XS owners on one team share vision but do not win automatically.
    fresh();owners[5]=0;owners[3]=4;inGame[2]=false;inGame[4]=true;
    seed();tick(3);tick(18);
    assert(!gMatchStarted&&gWinner==0&&born(7)==4&&born(4)==4);
    assert(vision.at({7,285})==((1<<7)|(1<<4))&&vision.at({4,286})==((1<<7)|(1<<4)));
    inGame[7]=false;tick(19);assert(navalDefeat1W5()&&gWinner==0);

    // Grey/P7 sparse identity: native cleanup uses selector2 (XS4), not color7.
    fresh();owners[5]=0;owners[7]=4;inGame[2]=false;inGame[4]=true;selectors[2]=4;
    seed();tick(3);tick(18);assert(gMatchStarted);
    for(int p=0;p<4;p++)objects.at(port(7,p)).hp=0;tick(19);
    assert(xsPlayerAttribute(4,cAttributeMilitaryPopulation)>0&&navalDefeat7W2()&&!navalDefeat7W7());
    replayNativeDefeat(7);assert(xsArrayGetInt(gCleaned,7)==1&&!inGame[4]);
    for(auto [r,u]:objects)if(u.owner==4)assert(u.hp==0);
    tick(20);tick(25);assert(gWinner==1&&navalWin1W5());

    // Builders retry placement and grant supplies once at real kill milestones.
    fresh();tick(3);attributes[{7,cAttributeKills}]=29;tick(4);
    assert(xsArrayGetInt(gBuilders,1)==0);attributes[{7,cAttributeKills}]=30;createFails=true;tick(5);
    assert(xsArrayGetInt(gBuilders,1)==0&&xsPlayerAttribute(7,cAttributeWood)==0);
    createFails=false;births.clear();orders.clear();tick(6);
    assert(xsArrayGetInt(gBuilders,1)==1&&born(7,83)==1&&orders.empty());
    assert(attributes.at({7,cAttributeWood})==400&&attributes.at({7,cAttributeStone})==150);
    attributes[{7,cAttributeKills}]=120;for(int t=7;t<=9;t++)tick(t);tick(10);
    assert(xsArrayGetInt(gBuilders,1)==4&&variables.at(6)==4&&attributes.at({7,cAttributeWood})==1600);
    int misplaced=nextRef++;objects[misplaced]=Object{7,45,100,Vec(54.5,32.5,-1),5};
    navalConstruction(1);assert(!xsDoesUnitExist(misplaced)&&navalPorts(1)==4);
    int extra=nextRef++;objects[extra]=Object{7,45,100,Vec(46.5,24.5,-1),5};
    navalConstruction(1);assert(navalPorts(1)==4);
    objects.at(extra).buildpoints=35;navalConstruction(1);births.clear();navalWave(1);
    assert(navalPorts(1)==5&&born(7)==5);
    int extra2=nextRef++;objects[extra2]=Object{7,45,100,Vec(63.5,24.5,-1),35};
    navalConstruction(1);assert(navalPorts(1)==6&&!available.at({7,45}));
    int overflow=nextRef++;objects[overflow]=Object{7,45,100,Vec(46.5,29.5,-1),5};
    int wood=attributes.at({7,cAttributeWood});navalConstruction(1);
    assert(!xsDoesUnitExist(overflow)&&attributes.at({7,cAttributeWood})==wood+300);
    for(int i=0;i<5;i++)objects[nextRef++]=Object{7,79,100,Vec(10,48,-1),5};
    for(int i=0;i<2;i++)objects[nextRef++]=Object{7,87,100,Vec(8,48,-1),5};
    for(int i=0;i<13;i++)objects[nextRef++]=Object{7,4,100,Vec(34,48,-1)};
    navalConstruction(1);int towers=0,archers=0,ranges=0;
    for(auto [r,u]:objects)if(u.owner==7&&u.hp>0){towers+=u.type==79;archers+=u.type==4;ranges+=u.type==87;}
    assert(towers==4&&ranges==1&&archers==12&&!available.at({7,79})&&!available.at({7,87})&&!available.at({7,4}));
    for(int p=0;p<4;p++)objects.at(port(1,p)).hp=0;
    int healed=ship(1,1);objects.at(healed).hp=50;objects.at(healed).point=Vec(50.5,24.5,-1);
    tick(11);assert(xsArrayGetInt(gAlive,1)==1&&navalPorts(1)==2&&objects.at(healed).hp==51);
    objects.at(extra).hp=0;tick(12);assert(xsArrayGetInt(gAlive,1)==1);
    objects.at(extra2).hp=0;tick(13);assert(navalDefeat1W5());
    objects.at(extra).hp=100;tick(14);assert(xsArrayGetInt(gAlive,1)==0);
    replayNativeDefeat(1);for(auto [r,u]:objects)if(u.owner==7)assert(u.hp==0);
    fresh();tick(3);int foundation=nextRef++;
    objects[foundation]=Object{7,45,100,Vec(46.5,24.5,-1),34};
    for(int p=0;p<4;p++)objects.at(port(1,p)).hp=0;tick(4);
    assert(xsArrayGetInt(gAlive,1)==0&&navalPorts(1)==0&&!navalBirth(1,539,0,false));

    // Center rewards are exact even with duplicate heartbeat callbacks.
    fresh();tick(3);objects.at(ship(1,0)).point=Vec(72,72,-1);createFails=true;
    for(int t=4;t<=93;t++){tick(t);tick(t);}
    assert(xsArrayGetInt(gHold,1)==90&&xsArrayGetInt(gPrestige,1)==45);
    assert(xsArrayGetInt(gPendingCannons,1)==2); // Timed75 and uninterrupted center90.
    tick(94);assert(xsArrayGetInt(gPendingCannons,1)==2);
    objects.at(ship(5,0)).point=Vec(72,72,-1);tick(95);assert(xsArrayGetInt(gHold,1)==0);

    // All eight sectors, including Blue and Green, have dock-near births and central orders.
    reset();for(int c=1;c<=8;c++){owners[c]=c;inGame[c]=true;selectors[c]=c;}
    seed();navalMain();tick(3);assert(births.empty()&&orders.empty());
    for(int c=1;c<=8;c++){
        Vec local(24.5,46.5,-1),world=navalWorld(c,local),roundtrip=navalLocal(c,world);
        assert(roundtrip.x==local.x&&roundtrip.y==local.y);
        for(int p=0;p<4;p++){
            int r=port(c,p);Vec dock=objects.at(r).point;assert(navalBirth(c,539,p,false));
            Vec launch=objects.at(births.back()).point;double dx=launch.x-dock.x,dy=launch.y-dock.y;
            assert(std::abs(dx*dx+dy*dy-9)<0.0001);
            Vec clear=clearanceOrders.at(births.back());
            assert(std::abs(clear.x-(dock.x+2*dx))<0.0001);
            assert(std::abs(clear.y-(dock.y+2*dy))<0.0001);
        }
        int r=port(c,0);objects.at(r).point=world;assert(navalBirth(c,539,0,false));
        Vec northClear=navalLocal(c,clearanceOrders.at(births.back()));
        assert(northClear.x==27.5&&northClear.y==49.5);
        int extra=nextRef++;objects[extra]=Object{c,45,3000,navalWorld(c,Vec(24.5,63.5,-1)),35};
        navalConstruction(c);assert(navalPorts(c)==5&&navalBirth(c,539,4,false));
        Vec launch=objects.at(births.back()).point;
        double dx=launch.x-objects.at(extra).point.x,dy=launch.y-objects.at(extra).point.y;
        assert(dx*dx+dy*dy<=16);
        Vec southClear=navalLocal(c,clearanceOrders.at(births.back()));
        assert(southClear.x==27.5&&southClear.y==60.5);
        blockedDock=r;attemptedPoints.clear();auto count=births.size();
        assert(!navalBirth(c,539,0,false)&&births.size()==count&&!attemptedPoints.empty());
        for(Vec point:attemptedPoints){dx=point.x-world.x;dy=point.y-world.y;assert(dx*dx+dy*dy<=16);}
        blockedDock=-1;objects.at(r).hp=0;attemptedPoints.clear();
        assert(!navalBirth(c,539,0,false)&&attemptedPoints.empty());
        int hero=xsArrayGetInt(gFlagship,c);objects.at(hero).hp=0;orders.clear();
        assert(navalBirth(c,250,1,true)&&orders.empty()&&!navalBirth(c,250,1,true));
        Vec berth=xsArrayGetVector(gHeroPads,c),actual=objects.at(births.back()).point;
        assert(berth.x==actual.x&&berth.y==actual.y);
    }
}
