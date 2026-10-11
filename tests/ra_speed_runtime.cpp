// Compiles the emitted XS state machine itself, with independent engine stubs.
#include <cassert>
#include <cmath>
#include <iostream>
#include <map>
#include <string>
#include <tuple>
#include <vector>
using std::string;
constexpr int cMulAttribute = 5, cMovementSpeed = 5, cAttackReloadTime = 10, cAttackDelay = 41;
std::vector<std::vector<int>> arrays;
std::map<int, int> vars;
std::map<std::tuple<int,int,int>, float> attributes;
std::vector<string> chats;
int now = 0, calls = 0;
int owners[9] = {0,7,2,5,8,3,1,4,6};
bool inGame[9] = {false,true,true,true,true,true,true,true,true};
int xsArrayCreateInt(int size, int initial, string) {
    arrays.emplace_back(size,initial); return arrays.size()-1;
}
int xsArrayGetInt(int array, int index) {return arrays.at(array).at(index);}
void xsArraySetInt(int array, int index, int value) {arrays.at(array).at(index)=value;}
int xsTriggerVariable(int id) {return vars[id];}
void xsSetTriggerVariable(int id, int value) {vars[id]=value;}
int xsGetGameTime() {return now;}
bool xsGetPlayerInGame(int owner) {return inGame[owner];}
int cbaWorldPlayerForColor(int color) {return owners[color];}
void xsChatData(string text) {chats.push_back(text);}
void xsEffectAmount(int kind, int unit, int attr, double factor, int owner) {
    assert(kind==cMulAttribute && unit>=0 && owner>0 && owner<=8 && inGame[owner]);
    assert(attr==cMovementSpeed || attr==cAttackReloadTime || attr==cAttackDelay);
    auto key=std::make_tuple(owner,unit,attr);
    if (!attributes.count(key)) attributes[key]=(attr==5 ? 0.9 : attr==10 ? 2.4 : 0.6);
    attributes[key]*=factor; ++calls;
}
// GENERATED_RUNTIME

void clear() {
    arrays.clear(); vars.clear(); attributes.clear(); chats.clear(); calls=0; now=0;
    gRaSpeedSeenLoss=gRaSpeedUntil=gRaSpeedApplied=-1;
    cbaSpeedTick(); assert(calls==0); // Guard against an early rule before main.
    cbaSpeedInitialize(); cbaSpeedInitialize(); assert(arrays.size()==3);
    for (int owner=1;owner<=8;++owner) inGame[owner]=true;
    for (int color=1;color<=8;++color) {
        vars[120+color]=1; vars[47+color]=0;
    }
}
bool boosted(int color) {return xsArrayGetInt(gRaSpeedApplied,owners[color])==1;}
void closeSlot(int color) {vars[120+color]=0; vars[47+color]=1;}
void lose(int color) {vars[47+color]=1;}
void checkFactors(int owner, double movement, double fire) {
    bool found=false;
    for (auto &entry:attributes) if (std::get<0>(entry.first)==owner) {
        found=true;
        int attr=std::get<2>(entry.first);
        double expected=attr==5 ? 0.9*movement : (attr==10 ? 2.4 : 0.6)/fire;
        assert(std::abs(entry.second-expected)<1e-4);
    }
    assert(found);
}
int main() {
    clear(); closeSlot(2); closeSlot(4); closeSlot(6); closeSlot(7);
    now=899; lose(1); cbaSpeedTick(); assert(calls==0);
    now=900; cbaSpeedTick(); assert(calls==0); // No retroactive early loss.
    now=905; lose(5); cbaSpeedTick();
    assert(!boosted(3) && boosted(8) && vars[154]==300 && vars[153]==0); checkFactors(owners[8],2,3);
    int first=calls; for(now=906;now<1205;++now) cbaSpeedTick(); assert(calls==first);
    now=1205; cbaSpeedTick(); assert(!boosted(8) && vars[154]==0); checkFactors(owners[8],1,1);
    first=calls; now=1400; cbaSpeedTick(); assert(calls==first);

    clear(); now=900; lose(1); lose(2); cbaSpeedTick();
    assert(boosted(3) && boosted(4) && !boosted(5));
    assert(chats.size()==1); checkFactors(owners[3],2,3); checkFactors(owners[4],2,3);
    first=calls; now=1199; lose(3); cbaSpeedTick(); assert(calls==first+first/2);
    assert(xsArrayGetInt(gRaSpeedUntil,1)==1499 && boosted(4) && !boosted(3));
    checkFactors(owners[4],2,3); // Refresh never re-multiplies the survivor.
    now=1200; cbaSpeedTick(); assert(boosted(4));
    now=1499; cbaSpeedTick(); assert(!boosted(4)); checkFactors(owners[4],1,1);

    clear(); now=900; lose(1); cbaSpeedTick();
    now=1000; lose(5); cbaSpeedTick();
    now=1200; cbaSpeedTick(); assert(!boosted(2) && boosted(6));
    now=1300; cbaSpeedTick(); assert(!boosted(6));

    clear(); int oldOwner=owners[3]; owners[3]=0; now=900; lose(1); cbaSpeedTick();
    owners[3]=oldOwner; now=1199; cbaSpeedTick(); assert(boosted(3));
    now=1200; cbaSpeedTick(); assert(!boosted(3)); checkFactors(owners[3],1,1);

    clear(); now=900; lose(1); cbaSpeedTick();
    // Multiplicative civilization/tech upgrades during the boost are retained.
    for(auto &entry:attributes) if(std::get<0>(entry.first)==owners[2]) entry.second*=1.1;
    now=1200; cbaSpeedTick();
    for(auto &entry:attributes) if(std::get<0>(entry.first)==owners[2]) {
        int attr=std::get<2>(entry.first);
        double expected=(attr==5 ? 0.9 : attr==10 ? 2.4 : 0.6)*1.1;
        assert(std::abs(entry.second-expected)<1e-4);
    }

    clear(); now=900; lose(1); lose(2); lose(3); lose(4); cbaSpeedTick();
    assert(calls==0 && chats.empty()); // No survivor, no boost.
    for(int i=0;i<100;++i) {cbaSpeedSetOwner(owners[8],true); cbaSpeedSetOwner(owners[8],false);}
    checkFactors(owners[8],1,1); // Repeated cycles stay within engine float precision.
    std::cout << "Speed runtime contracts passed\n";
}
