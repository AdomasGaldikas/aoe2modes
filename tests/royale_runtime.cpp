// Tests actual serialized XS bodies. Engine behavior here is a deliberately bounded mock.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstring>
#include <iostream>
#include <map>
#include <random>
#include <queue>
#include <set>
#include <tuple>
#include <vector>
struct Vec { double x,y,z; Vec(double x=0,double y=0,double z=0):x(x),y(y),z(z){} };
struct Object { int owner,type; double hp; Vec point; int carrier=-1; double buildpoints=100; };
struct Array { std::vector<int> ints; std::vector<float> floats; std::vector<Vec> vectors; };
std::vector<Array> arrays;
std::map<int,Object> objects;
std::vector<int> ownerUnits[9];
std::map<std::tuple<int,int,int,int>,float> defs;
std::map<std::pair<int,int>,float> attrs;
std::map<std::pair<int,int>,float> properties;
std::map<int,int> variables;
std::map<int,float> unitCosts;
std::vector<int> orders,winners;
int owners[9]={0,7,3,6,1,8,2,5,4};
int selectors[9]={0,6,8,4,7,1,5,3,2};
bool connected[9]={false,true,true,true,true,true,true,true,true};
int seconds=0,nextRef=100000,events=0;
bool failBirth=false;
std::mt19937 rng(1);
const int cArmor=8,cAttack=9,cAttributeKilledByOthers=154,cAttributeKills=20,cAttributeStone=2;
const int cAttributeWood=1,cConversionChanceMod=113,cDamageClassMelee=4,cDamageClassPierce=3;
const int cEnableObject=2,cFogFlag=28,cFoodCost=103,cGarrisonCapacity=2,cHeroStatus=40;
const int cHitpoints=0,cLineOfSight=1,cMovementSpeed=5,cObstructionType=78,cPopulation=110;
const int cSetAttribute=0,cStoneCost=106,cTrainTime=101,cWoodCost=104;
int xsArrayCreateInt(int n,int value,const char*) {
    arrays.push_back(Array{std::vector<int>(n,value),{}, {}}); return arrays.size()-1;
}
int xsArrayCreateFloat(int n,float value,const char*) {
    arrays.push_back(Array{{},std::vector<float>(n,value), {}}); return arrays.size()-1;
}
int xsArrayCreateVector(int n,Vec value,const char*) {
    arrays.push_back(Array{{},{},std::vector<Vec>(n,value)}); return arrays.size()-1;
}
int xsArrayGetInt(int a,int i){return arrays.at(a).ints.at(i);}
void xsArraySetInt(int a,int i,int v){arrays.at(a).ints.at(i)=v;}
float xsArrayGetFloat(int a,int i){return arrays.at(a).floats.at(i);}
void xsArraySetFloat(int a,int i,float v){arrays.at(a).floats.at(i)=v;}
Vec xsArrayGetVector(int a,int i){return arrays.at(a).vectors.at(i);}
void xsArraySetVector(int a,int i,Vec v){arrays.at(a).vectors.at(i)=v;}
int xsArrayGetSize(int a){return arrays.at(a).ints.size();}
bool xsDoesUnitExist(int r){return objects.count(r)&&objects.at(r).hp>0;}
int xsGetUnitOwner(int r){return objects.at(r).owner;}
int xsGetUnitObjectId(int r){return objects.at(r).type;}
float xsGetUnitHitpoints(int r){return objects.at(r).hp;}
Vec xsGetUnitPosition(int r){return objects.at(r).point;}
float xsVectorGetX(Vec v){return v.x;}
float xsVectorGetY(Vec v){return v.y;}
Vec xsVectorSet(double x,double y,double z){return Vec(x,y,z);}
int xsCeilToInt(float v){return std::ceil(v);}
int xsGetGameTime(){return seconds;}
int xsGetRandomNumberMax(int n){assert(n>0);return std::uniform_int_distribution<int>(0,n-1)(rng);}
bool xsGetPlayerInGame(int o){return o>0&&o<9&&connected[o];}
int xsGetWorldPlayerId(int s){return selectors[s];}
int xsGetPlayerCivilization(int o){return o==8?999:o;}
float xsGetObjectAttribute(int o,int t,int a,int damage=-1){
    auto key=std::make_tuple(o,t,a,damage);
    if(defs.count(key))return defs[key];
    if(a==cHitpoints)return 100;
    if(a==cPopulation)return -1;
    if(a==cAttack)return damage==4?10:0;
    if(a==cTrainTime)return 100;
    return 0;
}
float xsGetUnitAttribute(int r,int a){
    if(a==cPopulation&&unitCosts.count(r))return unitCosts[r];
    auto u=objects.at(r);return xsGetObjectAttribute(u.owner,u.type,a);
}
float xsGetUnitBuildPoints(int r){return objects.at(r).buildpoints;}
bool isBuilding(int t){return t==789||t==793||t==797||t==801||t==82||t==79||t==72||t==792||t==87||t==12||t==101||t==70;}
float xsGetUnitProperty(int r,int p,int=-1){
    if(p==5)return objects.at(r).carrier;
    if(p==10004)return isBuilding(objects.at(r).type)?80:70;
    return properties[{r,p}];
}
bool xsSetUnitProperty(int r,int p,float value,int=-1){properties[{r,p}]=value;return true;}
bool xsSetUnitName(int,const char*){return true;}
float xsPlayerAttribute(int o,int a){return attrs[{o,a}];}
void xsSetPlayerAttribute(int o,int a,float v){attrs[{o,a}]=v;}
void xsSetTriggerVariable(int id,int v){variables[id]=v;}
float bitCastToFloat(int bits){float value;std::memcpy(&value,&bits,4);return value;}
int xsGetPlayerUnitIds(int o,int type,int a){
    arrays.at(a).ints.clear();
    for(int r:ownerUnits[o]) {
        auto u=objects.at(r);
        if(u.owner==o&&u.hp>0&&(type==-1||u.type==type))arrays.at(a).ints.push_back(r);
    }
    return a;
}
void xsEffectAmount(int command,int type,int a,float v,int o){
    if(command==cEnableObject)return;
    assert(command==cSetAttribute);
    if(a==cAttack||a==cArmor){int packed=v;defs[{o,type,a,packed/256}]=packed%256;}
    else defs[{o,type,a,-1}]=v;
}
bool xsRemoveUnit(int r){if(!xsDoesUnitExist(r))return false;objects.at(r).hp=0;return true;}
float xsSetUnitHitpoints(int r,float value){
    auto& u=objects.at(r);
    if(u.hp>0&&value<=0){attrs[{u.owner,cAttributeKilledByOthers}]++;attrs[{8,cAttributeKills}]++;}
    u.hp=value;return value;
}
int xsCreateUnit(int type,int owner,Vec point,bool,bool,bool collision){
    if(collision&&failBirth)return -1;
    int r=nextRef++;objects[r]=Object{owner,type,xsGetObjectAttribute(owner,type,cHitpoints),point};
    ownerUnits[owner].push_back(r);return r;
}
void xsTaskUnits(int a,int action,Vec,int,bool queued,bool,bool,int){
    assert(action==1&&!queued);orders.push_back(xsArrayGetInt(a,0));
}
void xsChatData(const char*){events++;}
#include "royale-runtime.h"
#include "royale-effects.h"
int wagon(int c){return xsArrayGetInt(gWagons,c);}
int hero(int c){return xsArrayGetInt(gHeroes,c);}
int owner(int c){return xsArrayGetInt(gOwners,c);}
void tick(int real){seconds=gStart+real*2;royaleTick();}
void reset(bool sparse=false){
    for(auto& refs:ownerUnits)refs.clear();
    unitCosts.clear();objects.clear();arrays.clear();defs.clear();attrs.clear();properties.clear();variables.clear();orders.clear();
    winners.clear();failBirth=false;seconds=3;nextRef=100000;events=0;rng.seed(1);
    for(int i=1;i<=8;i++)connected[owners[i]]=!sparse||i==1||i==3||i==5||i==8;
    gReady=false;gMatchStarted=false;gProtectionReleased=false;gEvacuated=false;gStart=0;gLastTick=-1;
    gWinner=0;gStage=0;gAnnounced=-1;gLastMarkers=-100;gChestIndex=0;gChestRef=-1;gChestSince=-1;
    gChestCandidate=0;gChestExpires=-1;gRadius=112;gCenter=Vec(120,120,-1);
    royaleMain();
    #include "royale-initial.h"
    for(auto [r,u]:objects)ownerUnits[u.owner].push_back(r);
    royaleResolve();royaleOutcome(false);
}
int unit(int c,int type,Vec p){return xsCreateUnit(type,owner(c),p,false,false,true);}
void position(int c,Vec p){objects[wagon(c)].point=p;xsArraySetVector(gLastWagon,c,p);}
void killCombat(int c){for(auto& [r,u]:objects)if(u.owner==owner(c)&&royaleCombat(r))u.hp=0;}
void connectedCircle(Vec center,int radius,Vec final) {
    if(radius==0)return;
    std::set<std::pair<int,int>> land,seen;
    for(int x=4;x<236;x++)for(int y=4;y<236;y++){
        Vec p(x,y,-1);
        if(royaleLand(p)&&royaleDistance(p,center)<=radius*radius)land.insert({x,y});
    }
    std::queue<std::pair<int,int>> pending;pending.push({int(final.x),int(final.y)});
    seen.insert(pending.front());
    while(!pending.empty()){
        auto [x,y]=pending.front();pending.pop();
        for(int dx=-1;dx<=1;dx++)for(int dy=-1;dy<=1;dy++){
            std::pair<int,int> p(x+dx,y+dy);
            if(land.count(p)&&!seen.count(p)){seen.insert(p);pending.push(p);}
        }
    }
    // A single tangent tile behind a pond has no collision clearance for a unit.
    // Every cell with a 3x3 land/safe neighborhood must connect to the final arena.
    for(auto [x,y]:land){
        bool usable=true;
        for(int dx=-1;dx<=1;dx++)for(int dy=-1;dy<=1;dy++)if(!land.count({x+dx,y+dy}))usable=false;
        if(usable)assert(seen.count({x,y}));
    }
}
void zonePaths(){
    reset();int counts[9]={};
    for(int seed=0;seed<2000;seed++){
        rng.seed(seed);royaleZones();int site=(int(gFinal.x)-80)/40*3+(int(gFinal.y)-80)/40;counts[site]++;
        Vec previous(120,120,-1);int oldRadius=112;
        for(int stage=0;stage<9;stage++){
            Vec p=xsArrayGetVector(gZones,stage);int radius=xsArrayGetInt(gStormRadii,stage);
            if(royaleDistance(p,previous)>pow(oldRadius-radius,2)+0.001) {
                std::cerr<<"seed "<<seed<<" stage "<<stage<<" prior "<<previous.x<<","<<previous.y
                <<" old R "<<oldRadius<<" new "<<p.x<<","<<p.y<<" radius "<<radius<<" final "<<gFinal.x<<","<<gFinal.y<<"\n";abort();}

            assert(royaleDistance(p,gFinal)<=radius*radius+0.001);assert(royaleLand(p));
            assert(p.x-radius>=4&&p.y-radius>=4&&p.x+radius<=236&&p.y+radius<=236);
            if(stage==0)assert(p.x==120&&(p.y==108||p.y==120||p.y==132));
            if(seed<32)connectedCircle(p,radius,gFinal);
            previous=p;oldRadius=radius;
        }
    }
    for(int n:counts)assert(n>150&&n<300);
    for(int site=0;site<9;site++)for(int first=0;first<3;first++){
        gFinal=xsArrayGetVector(gFinals,site);xsArraySetVector(gZones,0,Vec(120,108+first*12,-1));
        assert(royalePath(true));
    }
    royaleStorm(330);assert(gRadius==104);Vec p=xsArrayGetVector(gZones,0);
    assert(std::abs(gCenter.y-(120+p.y)/2)<0.001);
    royaleMarkers(330);int alive=0;for(auto [r,u]:objects)if(u.owner==0&&u.hp>0)alive++;
    assert(alive<=262);royaleMarkers(334);alive=0;for(auto [r,u]:objects)if(u.owner==0&&u.hp>0)alive++;
    assert(alive<=262);
    std::cout<<"2000 seeded paths passed\n";
}
void identitiesAndBirths(){
    reset(true);
    for(int c=1;c<=8;c++){
        bool occupied=c==1||c==3||c==5||c==8;assert(xsArrayGetInt(gOccupied,c)==occupied);
        for(int s=1;s<=8;s++)assert(royaleOwner(c,s)==(occupied&&selectors[s]==owners[c]));
    }
    assert(xsArrayGetInt(gUnits,5)==567); // unknown civilization fallback
    assert(royalePopulation(1,3)==9);
    int t=xsArrayGetInt(gUnits,1);xsArraySetInt(gMainCaps,1,95);killCombat(1);defs[{owner(1),t,cPopulation,-1}]=-0.5;
    for(int i=0;i<119;i++)unit(1,t,Vec(32,84,-1));
    assert(royaleBirth(1,t,Vec(32,84,-1),1)>=0);assert(royaleBirth(1,t,Vec(32,84,-1),1)<0);
    killCombat(1);defs[{owner(1),t,cPopulation,-1}]=-2;xsArraySetInt(gMainCaps,1,95);
    for(int i=0;i<47;i++)unit(1,t,Vec(32,84,-1));assert(royaleBirth(1,t,Vec(32,84,-1),1)<0);
    killCombat(1);int oldOrders=orders.size();failBirth=true;xsArraySetInt(gNextWave,1,0);royaleProduction(1,10);
    assert(xsArrayGetInt(gNextWave,1)==11);assert(orders.size()==oldOrders); // failed births cannot issue orders
    failBirth=false;royaleProduction(1,11);assert(royalePopulation(1,3)==4);
    // Transformed objects are queried anew, rather than consuming stale reference/type ledgers.
    auto r=arrays[gSurvey].ints.back();objects[r].type=567;defs[{owner(1),567,cPopulation,-1}]=-2;
    assert(royalePopulation(1,0)>=5);
    float prior=royalePopulation(1,0);unitCosts[r]=-3;
    assert(royalePopulation(1,0)==prior+1); // Same master ID, different live transformation cost.
}
void rescuesAndOutcomes(){
    reset();Vec p(60,84,-1);position(1,p);objects[hero(2)].point=p;objects[wagon(1)].hp=0;
    royaleLosses(100);assert(xsArrayGetInt(gState,1)==RECOVERABLE);royaleRescue(1,114);
    assert(xsArrayGetInt(gState,1)==RECOVERABLE);int enemy=unit(5,567,p);royaleRescue(1,115);
    assert(xsArrayGetInt(gRescueSince,1)==-1);objects[enemy].hp=0;
    royaleRescue(1,116);failBirth=true;royaleRescue(1,131);assert(xsArrayGetInt(gRescued,1)==0);
    failBirth=false;royaleRescue(1,132);assert(xsArrayGetInt(gState,1)==ACTIVE);
    assert(objects[wagon(1)].hp==750);assert(xsArrayGetInt(gRescued,1)==1);
    objects[wagon(1)].hp=0;royaleLosses(133);assert(xsArrayGetInt(gState,1)==STRANDED);
    objects[wagon(2)].hp=0;royaleLosses(140);royaleRescue(2,200);assert(xsArrayGetInt(gState,2)==STRANDED);
    objects[wagon(3)].hp=0;royaleLosses(1739);royaleRescue(3,1740);assert(xsArrayGetInt(gState,3)==STRANDED);
    reset();for(int c=1;c<=4;c++)objects[wagon(c)].hp=0;royaleLosses(100);assert(gWinner==2);
    reset();for(int c=1;c<=8;c++){objects[wagon(c)].hp=0;killCombat(c);}royaleLosses(100);
    assert(gWinner==3);nativeOutcomes();assert(winners.size()==8);
    reset();connected[owner(1)]=false;royaleLosses(100);assert(xsArrayGetInt(gState,1)==RESIGNED);
    assert(!xsDoesUnitExist(hero(1)));assert(gWinner==0);
    reset();objects[wagon(1)].hp=1499;royaleOutcome(true);assert(gWinner==2);
    objects[wagon(5)].hp=1;royaleOutcome(true);assert(gWinner==2);
    reset();unit(1,567,Vec(32,84,-1));royaleOutcome(true);assert(gWinner==1);
    reset();xsArraySetInt(gKills,1,1);royaleOutcome(true);assert(gWinner==1);
    reset();tick(2100);assert(gWinner==3&&gRadius==0);int n=nextRef;tick(2101);assert(nextRef==n);
}
void damageRanksBuildersAndConstruction(){
    reset();gStage=1;gRadius=96;gCenter=Vec(120,120,-1);int carrier=unit(1,79,Vec(10,10,-1));
    int passenger=unit(1,567,Vec(120,120,-1));objects[passenger].carrier=carrier;
    int foundation=unit(1,87,Vec(10,10,-1));objects[foundation].buildpoints=1;
    royaleHazard(400);assert(objects[passenger].hp==99);assert(objects[foundation].hp==99);
    objects[passenger].hp=0.5;royaleHazard(401);royaleAbsorb();royaleCredit();
    assert(xsArrayGetInt(gKills,5)==0&&xsArrayGetInt(gDeaths,1)==0);
    attrs[{owner(1),cAttributeKills}]+=40;royaleCredit();assert(xsArrayGetInt(gKills,1)==40);
    reset();xsArraySetInt(gKills,1,40);int t=xsArrayGetInt(gUnits,1);int r=unit(1,t,Vec(32,84,-1));objects[r].hp=50;
    royalePromote(1,0);assert(xsArrayGetInt(gRank,1)==1);assert(std::abs(objects[r].hp-52.5)<0.001);
    royalePromote(1,0);assert(std::abs(objects[r].hp-52.5)<0.001);
    killCombat(1);royalePromote(1,1680);assert(xsArrayGetInt(gRank,1)==3);
    failBirth=true;royaleProduction(1,100);assert(xsArrayGetInt(gBuilderDelivered,1)==0);
    failBirth=false;royaleProduction(1,101);assert(xsArrayGetInt(gBuilderDelivered,1)==1);
    assert(attrs[std::make_pair(owner(1),cAttributeWood)]==250);
    xsArraySetInt(gKills,1,350);royaleProduction(1,102);royaleProduction(1,103);
    assert(xsArrayGetInt(gBuilderDelivered,1)==2);assert(royalePopulation(1,4)==2);
    for(auto& [ref,u]:objects)if(u.owner==owner(1)&&u.type==83){u.hp=0;break;}
    royaleProduction(1,104);assert(xsArrayGetInt(gBuilderDelivered,1)==3);
    int bad=unit(1,79,Vec(80,80,-1));float wood=attrs[{owner(1),cAttributeWood}];
    royaleBuildings(1);assert(!xsDoesUnitExist(bad));assert(attrs[std::make_pair(owner(1),cAttributeWood)]==wood+100);
    int a=unit(1,79,Vec(34,84,-1));int b=unit(1,79,Vec(36,84,-1));int c=unit(1,79,Vec(38,84,-1));
    royaleBuildings(1);assert(xsDoesUnitExist(a)&&xsDoesUnitExist(b)&&!xsDoesUnitExist(c));
    position(1,Vec(60,84,-1));royaleBuildings(1);assert(xsDoesUnitExist(a));
    objects[a].owner=owner(2);ownerUnits[owner(2)].push_back(a);royaleBuildings(2);assert(!xsDoesUnitExist(a));
}
void objectives(){
    reset();for(int c=1;c<=8;c++)killCombat(c);Vec post(72,72,-1);
    for(int i=0;i<5;i++)unit(1,567,post);royaleObjectives(0);royaleObjectives(10);
    assert(xsArrayGetInt(gPostTeam,0)==1);assert(xsArrayGetInt(gObjectiveXp,1)==10);
    royaleObjectives(40);assert(attrs[std::make_pair(owner(1),cAttributeWood)]==15);
    int enemy=unit(5,567,post);royaleObjectives(50);royaleObjectives(100);
    assert(attrs[std::make_pair(owner(1),cAttributeWood)]==15);
    objects[enemy].hp=0;royaleObjectives(101);royaleObjectives(130);
    assert(attrs[std::make_pair(owner(1),cAttributeWood)]==30);
    for(int i=0;i<20;i++)royaleTeamSupply(1,0,0,true);assert(xsArrayGetInt(gObjectiveXp,1)==100);
    royaleTeamSupply(1,7,3,false);assert(attrs[std::make_pair(owner(1),cAttributeWood)]==32);
    for(int i=0;i<20;i++)royaleTeamSupply(1,2000,1000,false);
    assert(attrs[std::make_pair(owner(1),cAttributeWood)]==1000);
    assert(attrs[std::make_pair(owner(1),cAttributeStone)]==500);
    royaleObjectives(240);assert(gChestRef>=0);int chest=gChestRef;
    for(auto& [r,u]:objects)if(u.owner==owner(1)&&royaleCombat(r))u.point=gChestPoint;
    royaleObjectives(241);royaleObjectives(253);assert(gChestRef<0&&!xsDoesUnitExist(chest));
    int captures=xsArrayGetInt(gCaptures,1);royaleObjectives(254);assert(xsArrayGetInt(gCaptures,1)==captures);
}
void campsHeroesAndFoundationStates(){
    reset();int camp=unit(1,12,Vec(34,84,-1));objects[camp].buildpoints=1;
    royaleProduction(1,0);assert(royalePopulation(1,2)==0);
    objects[camp].buildpoints=100;royaleProduction(1,1);assert(royalePopulation(1,2)==2);
    royaleProduction(1,20);assert(royalePopulation(1,2)==2);
    royaleProduction(1,21);assert(royalePopulation(1,2)==4);
    for(int i=0;i<20;i++)unit(1,358,Vec(32,84,-1));
    assert(royaleBirth(1,358,Vec(32,84,-1),2)<0);
    int firstGate=unit(1,789,Vec(35,86,-1));int secondGate=unit(1,801,Vec(36,86,-1));
    royaleBuildings(1);assert(xsDoesUnitExist(firstGate)&&!xsDoesUnitExist(secondGate));
    objects[wagon(1)].hp=0;royaleLosses(100);
    int invalid=unit(1,79,Vec(34,84,-1));royaleProduction(1,101);assert(!xsDoesUnitExist(invalid));
    assert(royalePopulation(1,2)==24); // Existing camp stops while recoverable.
    reset();objects[hero(1)].hp=0;royaleProduction(1,100);royaleProduction(1,144);
    assert(!xsDoesUnitExist(hero(1)));royaleProduction(1,145);assert(xsDoesUnitExist(hero(1)));
    position(1,Vec(60,84,-1));position(2,Vec(64,84,-1));position(3,Vec(180,120,-1));
    objects[hero(1)].hp=0;objects[wagon(1)].hp=0;royaleLosses(1740);
    royaleProduction(1,1799);assert(!xsDoesUnitExist(hero(1)));royaleProduction(1,1800);
    assert(xsDoesUnitExist(hero(1)));assert(royaleDistance(objects[hero(1)].point,objects[wagon(2)].point)<=128);
}
void persistentStateAndLateLoad(){
    reset();auto savedRng=rng;auto savedArrays=arrays;Vec savedFinal=gFinal;
    royaleZones();auto afterArrays=arrays;Vec afterFinal=gFinal;
    rng=savedRng;arrays=savedArrays;gFinal=savedFinal;royaleZones();
    assert(gFinal.x==afterFinal.x&&gFinal.y==afterFinal.y);
    for(int i=0;i<9;i++){
        Vec a=xsArrayGetVector(gZones,i),b=afterArrays[gZones].vectors[i];assert(a.x==b.x&&a.y==b.y);
    }
    reset();
    for(int c=1;c<=8;c++){
        killCombat(c);int type=xsArrayGetInt(gUnits,c);xsArraySetInt(gMainCaps,c,95);
        for(int i=0;i<95;i++)unit(c,type,Vec(120,120,-1));
        for(int i=0;i<24;i++)unit(c,358,Vec(120,120,-1)); // Pikemen
        int h=unit(c,173,Vec(120,120,-1));xsArraySetInt(gHeroes,c,h);
    }
    for(int t=0;t<2100;t++){
        royaleStorm(t);
        for(int c=1;c<=8;c++){
            position(c,gCenter);
            for(int r:ownerUnits[owner(c)])if(objects[r].hp>0)objects[r].point=gCenter;
        }
        tick(t);assert(gWinner==0);
        for(int c=1;c<=8;c++){assert(royalePopulation(c,0)<=120);assert(royalePopulation(c,3)<=120);}
    }
    assert(gEvacuated&&gProtectionReleased);assert(gChestIndex==7);
    tick(2100);assert(gWinner==3);assert(gStage==9);
}
int main(){zonePaths();identitiesAndBirths();rescuesAndOutcomes();damageRanksBuildersAndConstruction();objectives();campsHeroesAndFoundationStates();persistentStateAndLateLoad();
    std::cout<<"ownership, production, rescue, outcomes, hazards, progression, construction, objectives passed\n";}
