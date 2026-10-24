// Execute emitted XS plus serialized native selection/audio triggers. This is
// an engine model; DE selection UI and multiplayer delivery still need live QA.
#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
using string = std::string;
int seconds = 0;
std::map<int, int> variables;
std::vector<std::vector<int>> arrays;
std::map<int, std::set<int>> selected;
int selectors[9] = {0,6,8,4,7,1,5,3,2};
int post[9][25] = {};
struct Sound { int time, recipient; string name; };
struct Chat { int time, recipient; string text; };
std::vector<Sound> sounds;
std::vector<Chat> chats;
int xsGetGameTime() { return seconds; }
int xsTriggerVariable(int id) { return variables[id]; }
void xsSetTriggerVariable(int id, int value) { variables[id] = value; }
int xsArrayCreateInt(int n, int value, const char*) {
    arrays.emplace_back(n, value); return arrays.size()-1;
}
int xsArrayGetInt(int a, int i) { return arrays.at(a).at(i); }
void xsArraySetInt(int a, int i, int value) { arrays.at(a).at(i) = value; }
#include "ram-signals.h"
struct Check { int kind,a,b,inverted; };
struct Effect { int kind,a,b; string text; };
struct Trigger {
    int id; bool loop, enabled; int activated;
    std::vector<Check> checks; std::vector<Effect> effects;
};
std::vector<Trigger> graph;
std::map<int, size_t> indices;
void activate(int id) {
    auto& t = graph.at(indices.at(id)); t.enabled = true; t.activated = seconds;
}
#include "ram-signal-calls.h"
bool ready(const Trigger& t) {
    for(auto& c:t.checks) {
        bool ok=false;
        if(c.kind==0) ok=seconds-t.activated>=c.a;
        if(c.kind==1) ok=variables[c.a]==c.b;
        if(c.kind==2) ok=selected[c.a].count(c.b)>0;
        if(c.kind==3) ok=checkScript(c.a);
        if(c.inverted) ok=!ok;
        if(!ok) return false;
    }
    return true;
}
void fire(const Trigger& t) {
    for(auto& e:t.effects) {
        if(e.kind==0) variables[e.a]=e.b;
        if(e.kind==1) variables[e.a]=variables[e.b];
        if(e.kind==2) callScript(e.a);
        if(e.kind==3) activate(e.a);
        if(e.kind==4) sounds.push_back({seconds,e.a,e.text});
        if(e.kind==5) chats.push_back({seconds,e.a,e.text});
    }
}
void makeGraph() {
    #include "ram-signals-native.h"
    for (size_t i=0; i<graph.size(); i++) indices[graph[i].id] = i;
}
void reset() {
    variables.clear(); arrays.clear(); selected.clear(); sounds.clear(); chats.clear();
    graph.clear(); indices.clear(); seconds=0; gRamSignalLast=-1;
    for(int c=1;c<=8;c++) {
        variables[32+c-1]=1; variables[40+c-1]=selectors[c]; variables[121+c-1]=1;
    }
    makeGraph();
}
void advance(int count=1) {
    for(int i=0;i<count;i++) {
        seconds++; ramSignalHousekeeping();
        for(auto& t:graph) {
            if(!t.enabled || !ready(t)) continue;
            fire(t);
            if(t.loop) t.activated=seconds;
            else t.enabled=false;
        }
    }
}
void select(int sender, int event) {
    assert(post[sender][event]>0);
    selected[selectors[sender]]={post[sender][event]};
}
int team(int c) { return c<=4?1:2; }
string expectedName(int event) {
    int target=event<=8?event:event<=16?event-8:event-16;
    return "ram_team_" + string(event<=8?"help":event<=16?"attack":"feed")+
           "_p"+std::to_string(target)+"_v2";
}
void checkDelivery(int event, const std::set<int>& excluded={}) {
    int target=event<=8?event:event<=16?event-8:event-16;
    int audience=event>8&&event<=16?3-team(target):team(target);
    std::set<int> expected, actual, texts;
    for(int c=1;c<=8;c++) if(team(c)==audience&&!excluded.count(c)) expected.insert(selectors[c]);
    assert(sounds.size()==expected.size() && chats.size()==expected.size());
    for(auto& s:sounds) { assert(s.name==expectedName(event)); actual.insert(s.recipient); }
    for(auto& c:chats) { assert(c.text.rfind("[TEAM] ",0)==0); texts.insert(c.recipient); }
    assert(actual==expected && texts==expected);
}
void everyPostIsPrivate() {
    // All 64 inputs, including high colors, with native selectors independent
    // of displayed colors. Replaying one input never broadcasts to opponents.
    for(int c=1;c<=8;c++) for(int e=1;e<=24;e++) if(post[c][e]) {
        reset(); select(c,e); advance(25); checkDelivery(e);
        assert(variables[188]==0 && variables[215+c-1]==0);
    }
}
void pressReleaseAndCooldown() {
    reset(); select(1,1); advance(40); checkDelivery(1); // Held beyond cooldown.
    selected[selectors[1]].clear(); advance(); select(1,1); advance(20);
    assert(sounds.size()==8 && chats.size()==8);
    reset(); select(1,1); advance(); select(1,13); advance(25);
    checkDelivery(1); // Switching during cooldown is rejected, not delayed.
    selected[selectors[1]].clear(); advance(); select(1,13); advance(20);
    assert(sounds.size()==8 && sounds.back().name==expectedName(13));
    reset(); select(1,1); advance(13); select(1,14); advance(20);
    assert(sounds.size()==8 && sounds.back().name==expectedName(14)); // Direct switch.
    reset(); selected[selectors[1]]={post[1][1],post[1][13],post[1][19]};
    advance(40); assert(sounds.size()==4); // Multi-selection cannot flood the queue.
}
void wrongOwnerAndSparseSlots() {
    reset(); selected[selectors[5]]={post[1][1]}; advance(25); assert(sounds.empty());
    reset(); variables[33]=0; variables[122]=0; variables[37]=0; variables[126]=0;
    select(1,1); advance(25); checkDelivery(1,{2});
    reset(); variables[34]=0; // Defeated but occupied teammate can still hear.
    select(1,1); advance(25); checkDelivery(1);
    reset(); variables[34]=0; select(3,3); advance(25); assert(sounds.empty());
    reset(); variables[37]=0; select(1,14); advance(25); assert(sounds.empty());
    // Invalid targets and eliminated senders are also removed from pending queues.
    reset(); variables[188]=1; select(1,13); advance(); assert(variables[215]==13);
    variables[36]=0; advance(); assert(variables[215]==0); variables[188]=0;
    advance(25); assert(sounds.empty());
    for(int c=-1;c<=10;c++) for(int e=-1;e<=26;e++) {
        if(c>=1&&c<=8&&e>=1&&e<=24) continue;
        assert(!ramSignalAllowed(c,e));
    }
}
void fairSharedQueue() {
    reset(); variables[188]=1; variables[232]=4;
    for(int c=1;c<=8;c++) select(c,c);
    advance(); variables[188]=0; advance(200);
    assert(sounds.size()==32);
    std::vector<string> order;
    for(auto& s:sounds) if(order.empty()||order.back()!=s.name) order.push_back(s.name);
    assert(order.size()==8);
    for(int i=0;i<8;i++) assert(order[i]==expectedName((i+4)%8+1));
    reset();
    // Eight Backups, eight center rewards and a center capture contend with
    // all eight team requests. Speech must remain serialized and arrive once.
    for(int c=1;c<=8;c++) {
        variables[207+c-1]=1; variables[189+c-1]=c; select(c,c);
    }
    variables[205]=1;
    advance(500);
    std::map<std::pair<int,string>,std::set<int>> moments;
    for(auto& s:sounds) moments[{s.time,s.name}].insert(s.recipient);
    assert(moments.size()==25);
    std::map<string,double> durations;
    #include "ram-voice-durations.h"
    int previous=-100; double duration=0;
    int index=0;
    for(auto& entry:moments) {
        auto [time,name]=entry.first;
        assert(time-previous>=duration*2+1);
        if(index>=8&&index<16) assert(name.rfind("ram_team_",0)==0);
        previous=time; duration=durations.at(name);
        index++;
    }
    assert(variables[188]==0);
    for(int c=1;c<=8;c++) assert(variables[215+c-1]==0 && variables[207+c-1]==3);
}
int main() {
    everyPostIsPrivate(); pressReleaseAndCooldown(); wrongOwnerAndSparseSlots(); fairSharedQueue();
    std::cout<<"RAM team signal contracts passed\n";
}
