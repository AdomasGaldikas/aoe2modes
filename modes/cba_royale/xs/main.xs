// Last Caravan. Durations use nominal real seconds; only the shared game clock is read.
// Color -> actual XS owner is learned from surviving starting references, never slot order.
const int ACTIVE = 1;
const int RECOVERABLE = 2;
const int STRANDED = 3;
const int RESIGNED = 4;
int gOwners = -1;
int gOccupied = -1;
int gState = -1;
int gWagons = -1;
int gCastles = -1;
int gHeroes = -1;
int gWrecks = -1;
int gLastWagon = -1;
int gLastHp = -1;
int gQuiet = -1;
int gRescued = -1;
int gLostAt = -1;
int gRescueSince = -1;
int gHeroDue = -1;
int gNextWave = -1;
int gNextCamp = -1;
int gKills = -1;
int gRawKills = -1;
int gRawDeaths = -1;
int gDeaths = -1;
int gRank = -1;
int gObjectiveXp = -1;
int gBuilderDelivered = -1;
int gCastlePaid = -1;
int gUnits = -1;
int gMainCaps = -1;
int gIntervals = -1;
int gBaseHp = -1;
int gBaseAttack = -1;
int gRankHealth = -1;
int gAttackClass = -1;
int gBuildings = -1;
int gCivUnits = -1;
int gCivCaps = -1;
int gCivIntervals = -1;
int gRankKills = -1;
int gRankFloors = -1;
int gBuilderKills = -1;
int gChestTimes = -1;
int gStormDeadlines = -1;
int gStormRadii = -1;
int gStormDamagePercent = -1;
int gFinals = -1;
int gOutposts = -1;
int gZones = -1;
int gPostTeam = -1;
int gPostCandidate = -1;
int gPostSince = -1;
int gPostDue = -1;
int gPostXp = -1;
int gMarkers = -1;
int gSurvey = -1;
int gWorld = -1;
int gOrder = -1;
bool gReady = false;
bool gMatchStarted = false;
bool gProtectionReleased = false;
bool gEvacuated = false;
int gStart = 0;
int gLastTick = -1;
int gWinner = 0; // 0 unresolved; 1/2 winning team; 3 exact draw.
int gStage = 0;
int gAnnounced = -1;
int gLastMarkers = -100;
int gChestIndex = 0;
int gChestRef = -1;
int gChestSince = -1;
int gChestCandidate = 0;
int gChestExpires = -1;
int gCaptures = -1;
float gRadius = 112.0;
vector gCenter = vector(120, 120, -1);
vector gFinal = vector(120, 120, -1);
vector gChestPoint = vector(-1, -1, -1);

int royaleTeam(int color = 0) {
    if (color <= 4) return (1);
    return (2);
}

bool royaleExists(int reference = -1, int owner = -1) {
    if (reference < 0 || xsDoesUnitExist(reference) == false) return (false);
    return (xsGetUnitHitpoints(reference) > 0 && xsGetUnitOwner(reference) == owner);
}

float royaleDistance(vector a = vector(0, 0, -1), vector b = vector(0, 0, -1)) {
    float dx = xsVectorGetX(a) - xsVectorGetX(b);
    float dy = xsVectorGetY(a) - xsVectorGetY(b);
    return (dx * dx + dy * dy);
}

bool royaleSafe(vector point = vector(-1, -1, -1)) {
    return (gRadius > 0 && royaleDistance(point, gCenter) <= gRadius * gRadius);
}

// A garrisoned object's map position is the carrier's position. Follow nested carriers.
vector royalePosition(int reference = -1) {
    int container = reference;
    for (depth = 0; < 8) {
        int parent = xsCeilToInt(xsGetUnitProperty(container, 5, -1));
        if (parent < 0 || parent == container || xsDoesUnitExist(parent) == false) break;
        container = parent;
    }
    return (xsGetUnitPosition(container));
}

bool royaleCombat(int reference = -1) {
    int type = xsGetUnitObjectId(reference);
    if (type == ${WAGON} || type == ${BUILDER}) return (false);
    return (xsGetUnitProperty(reference, 10004, -1) == 70);
}

float royaleCost(int owner = -1, int unit = -1) {
    float cost = 0.0 - xsGetObjectAttribute(owner, unit, cPopulation);
    if (cost < 0) return (1.0);
    return (cost);
}

// Read live object costs: transformations and per-unit changes can differ from
// the original master definition used when deciding whether a birth may proceed.
float royaleUnitCost(int reference = -1) {
    float cost = 0.0 - xsGetUnitAttribute(reference, cPopulation);
    if (cost < 0) return (1.0);
    return (cost);
}

// Which population pool: 0 all combat, 1 primary, 2 counters, 3 object count, 4 builders.
float royalePopulation(int color = 0, int pool = 0) {
    int owner = xsArrayGetInt(gOwners, color);
    gSurvey = xsGetPlayerUnitIds(owner, -1, gSurvey);
    float result = 0;
    for (index = 0; < xsArrayGetSize(gSurvey)) {
        int reference = xsArrayGetInt(gSurvey, index);
        if (royaleExists(reference, owner) == false) continue;
        int type = xsGetUnitObjectId(reference);
        if (pool == 4) { if (type == ${BUILDER}) result++; continue; }
        if (royaleCombat(reference) == false) continue;
        bool support = type == ${PIKE} || type == ${SKIRM} || type == ${CAV};
        if (pool == 1 && (support || type == ${HERO})) continue;
        if (pool == 2 && support == false) continue;
        if (pool == 3) result++;
        else result = result + royaleUnitCost(reference);
    }
    return (result);
}

bool royaleOwner(int color = 0, int selector = 0) {
    if (gReady == false) return (false);
    return (xsArrayGetInt(gOccupied, color) == 1
        && xsArrayGetInt(gOwners, color) == xsGetWorldPlayerId(selector));
}

bool royaleResult(int color = 0, int selector = 0) {
    if (royaleOwner(color, selector) == false || gWinner == 0) return (false);
    if (xsGetPlayerInGame(xsArrayGetInt(gOwners, color)) == false) return (false);
    return (gWinner == 3 || gWinner == royaleTeam(color));
}

void royaleAbsorb() {
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 0) continue;
        int owner = xsArrayGetInt(gOwners, color);
        xsArraySetInt(gRawKills, color, xsCeilToInt(xsPlayerAttribute(owner, cAttributeKills)));
        xsArraySetInt(gRawDeaths, color, xsCeilToInt(xsPlayerAttribute(owner, cAttributeKilledByOthers)));
    }
}

void royaleCredit() {
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 0) continue;
        int owner = xsArrayGetInt(gOwners, color);
        int kills = xsCeilToInt(xsPlayerAttribute(owner, cAttributeKills));
        int deaths = xsCeilToInt(xsPlayerAttribute(owner, cAttributeKilledByOthers));
        int delta = kills - xsArrayGetInt(gRawKills, color);
        if (delta > 0) xsArraySetInt(gKills, color, xsArrayGetInt(gKills, color) + delta);
        delta = deaths - xsArrayGetInt(gRawDeaths, color);
        if (delta > 0) xsArraySetInt(gDeaths, color, xsArrayGetInt(gDeaths, color) + delta);
    }
    royaleAbsorb();
}

void royaleSupply(int color = 0, int wood = 0, int stone = 0) {
    int owner = xsArrayGetInt(gOwners, color);
    float amount = xsPlayerAttribute(owner, cAttributeWood) + wood;
    if (amount > ${WOOD_CAP}) amount = ${WOOD_CAP};
    xsSetPlayerAttribute(owner, cAttributeWood, amount);
    amount = xsPlayerAttribute(owner, cAttributeStone) + stone;
    if (amount > ${STONE_CAP}) amount = ${STONE_CAP};
    xsSetPlayerAttribute(owner, cAttributeStone, amount);
}

void royaleTeamSupply(int team = 0, int wood = 0, int stone = 0, bool renown = false) {
    int count = 0;
    for (color = 1; <= 8) {
        if (royaleTeam(color) == team && xsArrayGetInt(gOccupied, color) == 1
            && xsGetPlayerInGame(xsArrayGetInt(gOwners, color))) count++;
    }
    if (count == 0) return;
    int slot = 0;
    for (color = 1; <= 8) {
        if (royaleTeam(color) != team || xsArrayGetInt(gOccupied, color) == 0
            || xsGetPlayerInGame(xsArrayGetInt(gOwners, color)) == false) continue;
        int extraWood = 0;
        int extraStone = 0;
        if (slot < wood % count) extraWood = 1;
        if (slot < stone % count) extraStone = 1;
        royaleSupply(color, wood / count + extraWood, stone / count + extraStone);
        if (renown) {
            int points = xsArrayGetInt(gObjectiveXp, color) + ${OBJECTIVE_RENOWN};
            if (points > ${OBJECTIVE_RENOWN_CAP}) points = ${OBJECTIVE_RENOWN_CAP};
            xsArraySetInt(gObjectiveXp, color, points);
        }
        slot++;
    }
}

// These updates modify unit definitions and therefore also future births.
void royaleAttribute(int owner = -1, int type = -1, int attribute = 0, float value = 0.0) {
    xsEffectAmount(cSetAttribute, type, attribute, value, owner);
}

void royaleArmor(int owner = -1, int type = -1, int melee = 0, int pierce = 0) {
    float packed = 256 * cDamageClassMelee + melee;
    royaleAttribute(owner, type, cArmor, packed);
    packed = 256 * cDamageClassPierce + pierce;
    royaleAttribute(owner, type, cArmor, packed);
}

void royaleProtected(int reference = -1, bool attackable = false) {
    if (xsDoesUnitExist(reference) == false) return;
    xsSetUnitProperty(reference, 7, 0.0, 0);
    float flag = 0.0;
    if (attackable) flag = 1.0;
    xsSetUnitProperty(reference, 9, flag, 0);
    xsSetUnitProperty(reference, 8, flag, 0);
}

void royaleDecoration(int type = -1) {
    royaleAttribute(0, type, cLineOfSight, 0.0);
    royaleAttribute(0, type, cFogFlag, 1.0);
    royaleAttribute(0, type, cObstructionType, 0.0);
    royaleAttribute(0, type, 3, 0.0);
    royaleAttribute(0, type, 4, 0.0);
    royaleAttribute(0, type, cPopulation, 0.0);
}

int royaleProp(int type = -1, vector point = vector(-1, -1, -1)) {
    int reference = xsCreateUnit(type, 0, point, false, false, false);
    if (reference >= 0) {
        royaleProtected(reference, false);
        xsSetUnitProperty(reference, 10, 0.0, 0);
        xsSetUnitProperty(reference, 6, 0.0, 0); // Never captured by proximity.
    }
    return (reference);
}

bool royaleLand(vector point = vector(-1, -1, -1)) {
    float x = xsVectorGetX(point);
    float y = xsVectorGetY(point);
    if (x < 4 || x >= 236 || y < 4 || y >= 236) return (false);
    for (ix = 0; < 2) {
        for (iy = 0; < 2) {
            int cx = 100 + ix * 40;
            int cy = 100 + iy * 40;
            int left = cx - 4;
            int right = cx + 4;
            int top = cy - 4;
            int bottom = cy + 4;
            if (x >= left && x < right && y >= top && y < bottom) return (false);
        }
    }
    return (true);
}

void royaleOrder(int reference = -1, vector point = vector(-1, -1, -1)) {
    xsArraySetInt(gOrder, 0, reference);
    xsTaskUnits(gOrder, 1, point, -1, false, false, false, 0);
}

int royaleBirth(int color = 0, int type = -1, vector pad = vector(-1, -1, -1), int pool = 1) {
    int owner = xsArrayGetInt(gOwners, color);
    if (owner < 1 || xsArrayGetInt(gState, color) == RESIGNED || gWinner != 0) return (-1);
    if (pool != 4) {
        float cost = royaleCost(owner, type);
        // Keep arithmetic separate from DE's compound logical conditions.
        float nextCombat = royalePopulation(color, 0) + cost;
        if (nextCombat > ${COMBAT_CAP}) return (-1);
        if (royalePopulation(color, 3) >= ${OBJECT_CAP}) return (-1);
        if (pool == 1) {
            float nextMain = royalePopulation(color, 1) + cost;
            if (nextMain > xsArrayGetInt(gMainCaps, color)) return (-1);
        }
        if (pool == 2) {
            float nextSupport = royalePopulation(color, 2) + cost;
            if (nextSupport > ${SUPPORT_CAP}) return (-1);
        }
    }
    int reference = -1;
    for (attempt = 0; < 32) {
        int ring = 2 + attempt / 8 * 2;
        int direction = attempt % 8;
        int dx = 0;
        int dy = 0;
        if (direction == 0 || direction == 1 || direction == 7) dx = ring;
        if (direction == 3 || direction == 4 || direction == 5) dx = 0 - ring;
        if (direction == 1 || direction == 2 || direction == 3) dy = ring;
        if (direction == 5 || direction == 6 || direction == 7) dy = 0 - ring;
        vector point = xsVectorSet(xsVectorGetX(pad) + dx, xsVectorGetY(pad) + dy, -1);
        if (royaleLand(point) == false || royaleSafe(point) == false) continue;
        reference = xsCreateUnit(type, owner, point, false, false, true);
        if (royaleExists(reference, owner)) {
            if (pool != 4) {
                vector destination = xsVectorSet(xsVectorGetX(point) + dx / ring * 2,
                    xsVectorGetY(point) + dy / ring * 2, -1);
                if (royaleLand(destination) && royaleSafe(destination)) royaleOrder(reference, destination);
            }
            break;
        }
    }
    return (reference);
}

// Reject entire paths that become stranded by the four-tile lattice. The final
// landmark and the fair first centre are selected once, so rejection cannot bias them.
bool royalePath(bool greedy = false) {
    vector previous = vector(120, 120, -1);
    int oldRadius = 112;
    for (stage = 0; < 9) {
        int radius = xsArrayGetInt(gStormRadii, stage);
        int radiusSquared = radius * radius;
        vector chosen = xsArrayGetVector(gZones, 0);
        if (stage > 0) {
            int candidates = 0;
            float nearest = 1000000.0;
            for (gx = 1; < 60) {
                for (gy = 1; < 60) {
                    vector point = xsVectorSet(gx * 4, gy * 4, -1);
                    if (royaleDistance(point, previous) > (oldRadius - radius) * (oldRadius - radius)) continue;
                    float distance = royaleDistance(point, gFinal);
                    if (distance > radiusSquared || royaleLand(point) == false) continue;
                    candidates++;
                    if (greedy) {
                        if (distance < nearest) { nearest = distance; chosen = point; }
                    }
                    else if (xsGetRandomNumberMax(candidates) == 0) chosen = point;
                }
            }
            if (candidates == 0) return (false);
        }
        xsArraySetVector(gZones, stage, chosen);
        previous = chosen;
        oldRadius = radius;
    }
    return (true);
}

void royaleZones() {
    gFinal = xsArrayGetVector(gFinals, xsGetRandomNumberMax(9));
    xsArraySetVector(gZones, 0, xsVectorSet(120, 108 + xsGetRandomNumberMax(3) * 12, -1));
    for (attempt = 0; < 32) { if (royalePath(false)) return; }
    // Bounded work even for an adversarial random stream. Greedy movement reaches
    // the final landmark while the earlier circles still have ample slack.
    bool valid = royalePath(true);
}

void royaleStorm(int now = 0) {
    int previousStage = gStage;
    gStage = 0;
    for (stage = 0; < 9) {
        if (now >= xsArrayGetInt(gStormDeadlines, stage)) gStage++;
    }
    if (gStage != previousStage) gLastMarkers = -100;
    if (gStage >= 9) { gCenter = gFinal; gRadius = 0; return; }
    gCenter = vector(120, 120, -1);
    gRadius = 112;
    if (gStage > 0) {
        gCenter = xsArrayGetVector(gZones, gStage - 1);
        gRadius = xsArrayGetInt(gStormRadii, gStage - 1);
    }
    int deadline = xsArrayGetInt(gStormDeadlines, gStage);
    int warning = deadline - ${STORM_WARNING};
    if (gStage > 0 && warning < xsArrayGetInt(gStormDeadlines, gStage - 1))
        warning = xsArrayGetInt(gStormDeadlines, gStage - 1);
    if (now >= warning && gAnnounced < gStage) {
        vector target = xsArrayGetVector(gZones, gStage);
        xsChatData("[Caravan] Next safe circle: " + xsVectorGetX(target) + "," + xsVectorGetY(target)
            + ". Fire advances in " + (deadline - ${STORM_CLOSURE} - now) + "s.");
        if (gStage == 6) xsChatData("[Caravan] FINAL PHASE. Wagon losses are now permanent.");
        gAnnounced = gStage;
        gLastMarkers = -100;
    }
    if (now >= deadline - ${STORM_CLOSURE}) {
        float progress = (1.0 * now - deadline + ${STORM_CLOSURE}) / (1.0 * ${STORM_CLOSURE});
        vector next = xsArrayGetVector(gZones, gStage);
        gCenter = xsVectorSet(xsVectorGetX(gCenter) * (1.0 - progress) + xsVectorGetX(next) * progress,
            xsVectorGetY(gCenter) * (1.0 - progress) + xsVectorGetY(next) * progress, -1);
        gRadius = gRadius * (1.0 - progress) + progress * xsArrayGetInt(gStormRadii, gStage);
    }
}

void royaleMarkers(int now = 0) {
    if (now - gLastMarkers < ${MARKER_INTERVAL}) return;
    bool moving = false;
    if (gStage < 9) moving = now >= xsArrayGetInt(gStormDeadlines, gStage) - ${STORM_CLOSURE};
    if (gLastMarkers >= 0 && moving == false) return;
    gLastMarkers = now;
    for (slot = 0; < ${MARKER_LIMIT}) {
        int old = xsArrayGetInt(gMarkers, slot);
        if (old >= 0 && xsDoesUnitExist(old)) xsRemoveUnit(old);
        xsArraySetInt(gMarkers, slot, -1);
    }
    for (ring = 0; < 2) {
        vector center = gCenter;
        float radius = gRadius;
        int type = ${FIRE};
        if (ring == 1) {
            if (gStage >= 9 || gAnnounced < gStage) continue;
            center = xsArrayGetVector(gZones, gStage);
            radius = xsArrayGetInt(gStormRadii, gStage);
            type = ${WARNING};
        }
        if (radius <= 0) continue;
        for (sample = 0; < 128) {
            float angle = 6.283185307 * sample / 128.0;
            vector point = xsVectorSet(xsVectorGetX(center) + radius * cos(angle),
                xsVectorGetY(center) + radius * sin(angle), -1);
            xsArraySetInt(gMarkers, ring * 128 + sample, royaleProp(type, point));
        }
    }
}

void royaleLose(int color = 0, int now = 0) {
    if (xsArrayGetInt(gState, color) != ACTIVE) return;
    xsArraySetInt(gHeroDue, color, now + ${SUPPORT_HERO_RESPAWN});
    xsArraySetInt(gLostAt, color, now);
    xsArraySetInt(gRescueSince, color, -1);
    int state = STRANDED;
    if (now < ${RESCUE_CUTOFF} && xsArrayGetInt(gRescued, color) == 0) state = RECOVERABLE;
    xsArraySetInt(gState, color, state);
    if (state == RECOVERABLE) {
        int wreck = royaleProp(${WRECK}, xsArrayGetVector(gLastWagon, color));
        xsArraySetInt(gWrecks, color, wreck);
        xsChatData("[Caravan] P" + color + " wagon down! Escort a teammate Hero to the wreck within 60s.");
    }
    else xsChatData("[Caravan] P" + color + " lost production permanently. Their army and Hero can still help.");
}

float royaleNearby(int team = 0, vector point = vector(-1, -1, -1), int radius = 0) {
    float population = 0;
    for (color = 1; <= 8) {
        if (royaleTeam(color) != team || xsArrayGetInt(gOccupied, color) == 0
            || xsArrayGetInt(gState, color) == RESIGNED) continue;
        int owner = xsArrayGetInt(gOwners, color);
        gSurvey = xsGetPlayerUnitIds(owner, -1, gSurvey);
        for (index = 0; < xsArrayGetSize(gSurvey)) {
            int reference = xsArrayGetInt(gSurvey, index);
            if (royaleExists(reference, owner) == false || royaleCombat(reference) == false) continue;
            if (xsGetUnitProperty(reference, 5, -1) >= 0) continue;
            if (royaleDistance(royalePosition(reference), point) <= radius * radius)
                population = population + royaleUnitCost(reference);
        }
    }
    return (population);
}

void royaleRescue(int color = 0, int now = 0) {
    if (xsArrayGetInt(gState, color) != RECOVERABLE) return;
    int rescueAge = now - xsArrayGetInt(gLostAt, color);
    if (now >= ${RESCUE_CUTOFF} || rescueAge >= ${RESCUE_WINDOW}) {
        xsArraySetInt(gState, color, STRANDED);
        int expiredWreck = xsArrayGetInt(gWrecks, color);
        if (expiredWreck >= 0 && xsDoesUnitExist(expiredWreck)) xsRemoveUnit(expiredWreck);
        xsArraySetInt(gWrecks, color, -1);
        xsChatData("[Caravan] P" + color + " rescue window expired.");
        return;
    }
    vector point = xsArrayGetVector(gLastWagon, color);
    int rescueRadiusSquared = ${RESCUE_RADIUS} * ${RESCUE_RADIUS};
    bool escort = false;
    for (ally = 1; <= 8) {
        if (ally == color || royaleTeam(ally) != royaleTeam(color)
            || xsArrayGetInt(gOccupied, ally) == 0 || xsArrayGetInt(gState, ally) == RESIGNED) continue;
        int hero = xsArrayGetInt(gHeroes, ally);
        if (royaleExists(hero, xsArrayGetInt(gOwners, ally))
            && xsGetUnitProperty(hero, 5, -1) < 0
            && royaleDistance(royalePosition(hero), point) <= rescueRadiusSquared) escort = true;
    }
    if (royaleSafe(point) == false || escort == false
        || royaleNearby(3 - royaleTeam(color), point, ${RESCUE_ENEMY_RADIUS}) > 0) {
        xsArraySetInt(gRescueSince, color, -1);
        return;
    }
    int since = xsArrayGetInt(gRescueSince, color);
    if (since < 0) { xsArraySetInt(gRescueSince, color, now); return; }
    if (now - since < ${RESCUE_CHANNEL}) return;
    int owner = xsArrayGetInt(gOwners, color);
    int wagon = xsCreateUnit(${WAGON}, owner, point, false, false, true);
    if (royaleExists(wagon, owner) == false) return; // Retry; no ticket consumed by collision.
    royaleProtected(wagon, now >= ${WAGON_PROTECTION});
    xsSetUnitName(wagon, "Command Wagon - rescued");
    xsSetUnitHitpoints(wagon, 0.5 * ${WAGON_HP});
    xsArraySetInt(gWagons, color, wagon);
    xsArraySetInt(gLastHp, color, ${WAGON_HP} / 2);
    xsArraySetInt(gQuiet, color, 0);
    xsArraySetInt(gState, color, ACTIVE);
    xsArraySetInt(gRescued, color, 1);
    xsArraySetInt(gNextWave, color, now + xsArrayGetInt(gIntervals, color));
    int wreck = xsArrayGetInt(gWrecks, color);
    if (wreck >= 0 && xsDoesUnitExist(wreck)) xsRemoveUnit(wreck);
    xsArraySetInt(gWrecks, color, -1);
    xsChatData("[Caravan] P" + color + " wagon RESCUED. Cover its retreat!");
}

// Snapshot every team before declaring an outcome; no color gets a processing advantage.
void royaleOutcome(bool deadline = false) {
    if (gWinner != 0) return;
    int first = 0;
    int second = 0;
    float firstHp = 0;
    float secondHp = 0;
    float firstPop = 0;
    float secondPop = 0;
    int firstKills = 0;
    int secondKills = 0;
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 0 || xsArrayGetInt(gState, color) == RESIGNED) continue;
        int reference = xsArrayGetInt(gWagons, color);
        int live = 0;
        float hp = 0;
        if (xsArrayGetInt(gState, color) == ACTIVE && royaleExists(reference, xsArrayGetInt(gOwners, color))) {
            live = 1;
            hp = xsGetUnitHitpoints(reference) / ${WAGON_HP};
        }
        float population = royalePopulation(color, 0);
        int kills = xsArrayGetInt(gKills, color);
        if (royaleTeam(color) == 1) {
            first = first + live; firstHp = firstHp + hp;
            firstPop = firstPop + population; firstKills = firstKills + kills;
        }
        else {
            second = second + live; secondHp = secondHp + hp;
            secondPop = secondPop + population; secondKills = secondKills + kills;
        }
    }
    if (first > 0 && second > 0) gMatchStarted = true;
    if (deadline == false && (gMatchStarted == false || (first > 0 && second > 0))) return;
    gWinner = 3;
    if (first != second) { if (first > second) gWinner = 1; else gWinner = 2; }
    else if (firstHp != secondHp) { if (firstHp > secondHp) gWinner = 1; else gWinner = 2; }
    else if (firstPop != secondPop) { if (firstPop > secondPop) gWinner = 1; else gWinner = 2; }
    else if (firstKills != secondKills) { if (firstKills > secondKills) gWinner = 1; else gWinner = 2; }
    if (gWinner == 3) xsChatData("[Caravan] DRAW - both caravans share scenario victory.");
    else xsChatData("[Caravan] TEAM " + gWinner + " WINS THE LAST FIRE!");
    for (team = 1; <= 2) {
        int teamKills = 0;
        int teamRescues = 0;
        int teamCaptures = 0;
        for (color = 1; <= 8) {
            if (royaleTeam(color) != team || xsArrayGetInt(gOccupied, color) == 0) continue;
            teamKills = teamKills + xsArrayGetInt(gKills, color);
            teamRescues = teamRescues + xsArrayGetInt(gRescued, color);
            if (xsArrayGetInt(gCaptures, color) > teamCaptures) teamCaptures = xsArrayGetInt(gCaptures, color);
        }
        xsChatData("[Caravan] Team " + team + ": kills " + teamKills + ", rescues " + teamRescues
            + ", objective captures " + teamCaptures + ".");
    }
}

void royaleLosses(int now = 0) {
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 0) continue;
        int owner = xsArrayGetInt(gOwners, color);
        if (xsGetPlayerInGame(owner) == false) {
            if (xsArrayGetInt(gState, color) != RESIGNED) {
                xsArraySetInt(gState, color, RESIGNED);
                gWorld = xsGetPlayerUnitIds(owner, -1, gWorld);
                for (index = 0; < xsArrayGetSize(gWorld)) xsRemoveUnit(xsArrayGetInt(gWorld, index));
                int wreck = xsArrayGetInt(gWrecks, color);
                if (wreck >= 0 && xsDoesUnitExist(wreck)) xsRemoveUnit(wreck);
            }
            continue;
        }
        int wagon = xsArrayGetInt(gWagons, color);
        if (xsArrayGetInt(gState, color) == ACTIVE) {
            if (xsDoesUnitExist(wagon) && xsGetUnitOwner(wagon) == owner)
                xsArraySetVector(gLastWagon, color, royalePosition(wagon));
            if (royaleExists(wagon, owner) == false) royaleLose(color, now);
        }
        if (gEvacuated == false && now < ${CASTLE_EVACUATION}
            && xsArrayGetInt(gCastlePaid, color) == 0
            && royaleExists(xsArrayGetInt(gCastles, color), owner) == false) {
            xsArraySetInt(gCastlePaid, color, 1);
            royaleTeamSupply(3 - royaleTeam(color), ${CACHE_WOOD}, ${CACHE_STONE}, false);
        }
    }
    // A last-wagon loss is resolved before any rescue can resurrect a wiped team.
    royaleOutcome(false);
    if (gWinner != 0) return;
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 1) royaleRescue(color, now);
    }
}

void royalePromote(int color = 0, int now = 0) {
    int rank = 0;
    int renown = xsArrayGetInt(gKills, color) + xsArrayGetInt(gObjectiveXp, color);
    for (level = 0; < 3) {
        if (renown >= xsArrayGetInt(gRankKills, level) || now >= xsArrayGetInt(gRankFloors, level)) rank = level + 1;
    }
    if (rank <= xsArrayGetInt(gRank, color)) return;
    int owner = xsArrayGetInt(gOwners, color);
    int unit = xsArrayGetInt(gUnits, color);
    float oldMaximum = xsGetObjectAttribute(owner, unit, cHitpoints);
    float newMaximum = xsArrayGetFloat(gBaseHp, color) * (1.0 + 0.01 * rank * ${RANK_HP_PERCENT});
    // Save individual HP ratios before modifying the shared definition.
    gWorld = xsGetPlayerUnitIds(owner, unit, gWorld);
    int health = gRankHealth;
    for (index = 0; < xsArrayGetSize(gWorld))
        xsArraySetFloat(health, index, xsGetUnitHitpoints(xsArrayGetInt(gWorld, index)) / oldMaximum);
    royaleAttribute(owner, unit, cHitpoints, newMaximum);
    int attackClass = xsArrayGetInt(gAttackClass, color);
    float attack = 256.0 * attackClass + xsArrayGetFloat(gBaseAttack, color) + rank * ${RANK_ATTACK};
    royaleAttribute(owner, unit, cAttack, attack);
    for (index = 0; < xsArrayGetSize(gWorld))
        xsSetUnitHitpoints(xsArrayGetInt(gWorld, index), xsArrayGetFloat(health, index) * newMaximum);
    int hero = xsArrayGetInt(gHeroes, color);
    float ratio = 1;
    if (royaleExists(hero, owner)) ratio = xsGetUnitHitpoints(hero) / xsGetUnitAttribute(hero, cHitpoints);
    newMaximum = ${HERO_HP} + rank * ${HERO_RANK_HP};
    royaleAttribute(owner, ${HERO}, cHitpoints, newMaximum);
    attack = cDamageClassMelee * 256 + ${HERO_ATTACK} + rank * ${HERO_RANK_ATTACK};
    royaleAttribute(owner, ${HERO}, cAttack, attack);
    if (royaleExists(hero, owner)) xsSetUnitHitpoints(hero, ratio * newMaximum);
    xsArraySetInt(gRank, color, rank);
    xsChatData("[Caravan] P" + color + " promoted to rank " + rank + ".");
}

int royaleBuildPool(int type = -1) {
    if (type == ${TOWER}) return (0);
    if (type == ${WALL}) return (1);
    if (type == ${GATE} || type == ${GATE_SW} || type == ${GATE_NW}
        || type == ${GATE_EW} || type == ${GATE_NS}) return (2);
    if (type == ${BARRACKS} || type == ${RANGE} || type == ${STABLE}) return (3);
    return (-1);
}

void royaleBuildings(int color = 0) {
    int owner = xsArrayGetInt(gOwners, color);
    gWorld = xsGetPlayerUnitIds(owner, -1, gWorld);
    for (index = 0; < xsArrayGetSize(gWorld)) {
        int reference = xsArrayGetInt(gWorld, index);
        if (royaleExists(reference, owner) == false || reference == xsArrayGetInt(gCastles, color)) continue;
        if (xsGetUnitProperty(reference, 10004, -1) != 80) continue;
        int type = xsGetUnitObjectId(reference);
        int pool = royaleBuildPool(type);
        bool known = false;
        int free = -1;
        int count = 0;
        for (slot = 0; < 16) {
            int old = xsArrayGetInt(gBuildings, color * 16 + slot);
            if (old == reference) known = true;
            if (royaleExists(old, owner) == false) { if (free < 0) free = slot; continue; }
            if (royaleBuildPool(xsGetUnitObjectId(old)) == pool) count++;
        }
        if (known) continue; // Existing legal structures stay when the wagon moves away.
        int limit = 1;
        if (pool == 0) limit = ${TOWER_LIMIT};
        if (pool == 1) limit = ${WALL_LIMIT};
        if (pool == 2) limit = ${GATE_LIMIT};
        vector point = royalePosition(reference);
        bool valid = pool >= 0 && free >= 0 && count < limit && xsArrayGetInt(gState, color) == ACTIVE;
        if (valid) valid = royaleSafe(point) && royaleDistance(point, xsArrayGetVector(gLastWagon, color))
            <= ${BUILD_RADIUS} * ${BUILD_RADIUS};
        float clearance = 3.0 + ${FINAL_CLEAR_RADIUS}; // Includes the largest allowed footprint.
        for (site = 0; < 9) {
            if (royaleDistance(point, xsArrayGetVector(gFinals, site))
                < clearance * clearance) valid = false;
        }
        if (valid) xsArraySetInt(gBuildings, color * 16 + free, reference);
        else {
            int wood = xsCeilToInt(xsGetObjectAttribute(owner, type, cWoodCost));
            int stone = xsCeilToInt(xsGetObjectAttribute(owner, type, cStoneCost));
            xsRemoveUnit(reference);
            royaleSupply(color, wood, stone);
        }
    }
}

void royaleProduction(int color = 0, int now = 0) {
    int owner = xsArrayGetInt(gOwners, color);
    int state = xsArrayGetInt(gState, color);
    if (state == RESIGNED) return;
    royaleBuildings(color);
    royalePromote(color, now);
    int hero = xsArrayGetInt(gHeroes, color);
    if (royaleExists(hero, owner)) xsArraySetInt(gHeroDue, color, -1);
    else {
        int due = xsArrayGetInt(gHeroDue, color);
        int delay = ${HERO_RESPAWN};
        if (state != ACTIVE) delay = ${SUPPORT_HERO_RESPAWN};
        if (due < 0) xsArraySetInt(gHeroDue, color, now + delay);
        else if (now >= due) {
            vector heroPad = vector(-1, -1, -1);
            float nearest = 1000000;
            for (ally = 1; <= 8) {
                if (royaleTeam(ally) != royaleTeam(color) || xsArrayGetInt(gState, ally) != ACTIVE) continue;
                if (state == ACTIVE && ally != color) continue;
                vector point = xsArrayGetVector(gLastWagon, ally);
                float distance = royaleDistance(point, xsArrayGetVector(gLastWagon, color));
                if (distance < nearest) { nearest = distance; heroPad = point; }
            }
            if (nearest < 1000000) {
                hero = royaleBirth(color, ${HERO}, heroPad, 0);
                if (royaleExists(hero, owner)) {
                    royaleProtected(hero, true);
                    xsArraySetInt(gHeroes, color, hero);
                    xsArraySetInt(gHeroDue, color, -1);
                }
            }
        }
    }
    if (state != ACTIVE) return;
    vector pad = xsArrayGetVector(gLastWagon, color);
    int entitled = 0;
    for (level = 0; < 4) { if (xsArrayGetInt(gKills, color) >= xsArrayGetInt(gBuilderKills, level)) entitled++; }
    if (entitled > xsArrayGetInt(gBuilderDelivered, color) && royalePopulation(color, 4) < ${BUILDER_LIMIT}) {
        int builder = royaleBirth(color, ${BUILDER}, pad, 4);
        if (royaleExists(builder, owner)) {
            xsArraySetInt(gBuilderDelivered, color, xsArrayGetInt(gBuilderDelivered, color) + 1);
            royaleSupply(color, ${BUILDER_WOOD}, ${BUILDER_STONE});
            xsChatData("[Caravan] P" + color + " earned a builder and field supplies.");
        }
    }
    if (now >= xsArrayGetInt(gNextWave, color)) {
        int born = 0;
        for (birth = 0; < ${ARMY_BATCH}) {
            if (royaleBirth(color, xsArrayGetInt(gUnits, color), pad, 1) >= 0) born++;
        }
        int retry = xsArrayGetInt(gIntervals, color);
        if (born == 0) retry = 1;
        xsArraySetInt(gNextWave, color, now + retry);
    }
    if (now >= xsArrayGetInt(gNextCamp, color)) {
        bool campFound = false;
        for (slot = 0; < 16) {
            int camp = xsArrayGetInt(gBuildings, color * 16 + slot);
            if (royaleExists(camp, owner) == false) continue;
            int type = xsGetUnitObjectId(camp);
            if (royaleBuildPool(type) != 3) continue;
            if (xsGetUnitBuildPoints(camp) < xsGetUnitAttribute(camp, cTrainTime)) continue;
            if (royaleSafe(royalePosition(camp)) == false) continue;
            int unit = ${PIKE};
            if (type == ${RANGE}) unit = ${SKIRM};
            if (type == ${STABLE}) unit = ${CAV};
            for (birth = 0; < ${CAMP_BATCH}) royaleBirth(color, unit, royalePosition(camp), 2);
            campFound = true;
        }
        if (campFound) xsArraySetInt(gNextCamp, color, now + ${CAMP_INTERVAL});
    }
    int wagon = xsArrayGetInt(gWagons, color);
    int hp = xsCeilToInt(xsGetUnitHitpoints(wagon));
    int quiet = xsArrayGetInt(gQuiet, color) + 1;
    if (hp < xsArrayGetInt(gLastHp, color) || royaleSafe(pad) == false) quiet = 0;
    if (quiet >= ${WAGON_QUIET}) {
        float healed = hp + ${WAGON_REGEN};
        if (healed > ${WAGON_HP}) healed = ${WAGON_HP};
        xsSetUnitHitpoints(wagon, healed);
        hp = xsCeilToInt(healed);
        quiet = ${WAGON_QUIET};
    }
    xsArraySetInt(gQuiet, color, quiet);
    xsArraySetInt(gLastHp, color, hp);
}

int royaleControl(vector point = vector(-1, -1, -1)) {
    if (royaleSafe(point) == false) return (0);
    float first = royaleNearby(1, point, ${OBJECTIVE_RADIUS});
    float second = royaleNearby(2, point, ${OBJECTIVE_RADIUS});
    if (first >= ${OBJECTIVE_POPULATION} && second == 0) return (1);
    if (second >= ${OBJECTIVE_POPULATION} && first == 0) return (2);
    return (0);
}

void royaleCaptureCount(int team = 0) {
    for (color = 1; <= 8) {
        if (royaleTeam(color) == team && xsArrayGetInt(gOccupied, color) == 1)
            xsArraySetInt(gCaptures, color, xsArrayGetInt(gCaptures, color) + 1);
    }
}

void royaleObjectives(int now = 0) {
    for (post = 0; < 6) {
        int team = royaleControl(xsArrayGetVector(gOutposts, post));
        int held = xsArrayGetInt(gPostTeam, post);
        if (team == 0) { xsArraySetInt(gPostSince, post, -1); xsArraySetInt(gPostDue, post, now + ${OUTPOST_INTERVAL}); continue; }
        if (team != held) {
            int since = xsArrayGetInt(gPostSince, post);
            if (xsArrayGetInt(gPostCandidate, post) != team || since < 0) {
                xsArraySetInt(gPostCandidate, post, team); xsArraySetInt(gPostSince, post, now); continue;
            }
            if (now - since < ${OUTPOST_CAPTURE}) continue;
            xsArraySetInt(gPostTeam, post, team);
            xsArraySetInt(gPostDue, post, now + ${OUTPOST_INTERVAL});
            if (xsArrayGetInt(gPostXp, post * 3 + team) == 0) {
                xsArraySetInt(gPostXp, post * 3 + team, 1);
                royaleTeamSupply(team, 0, 0, true);
            }
            royaleCaptureCount(team);
            xsChatData("[Caravan] Team " + team + " captured outpost " + (post + 1) + ".");
        }
        else {
            xsArraySetInt(gPostSince, post, -1);
            if (now >= xsArrayGetInt(gPostDue, post)) {
                royaleTeamSupply(team, ${OUTPOST_WOOD}, ${OUTPOST_STONE}, false);
                xsArraySetInt(gPostDue, post, now + ${OUTPOST_INTERVAL});
            }
        }
    }
    if (gChestRef >= 0 && now >= gChestExpires) {
        if (xsDoesUnitExist(gChestRef)) xsRemoveUnit(gChestRef);
        gChestRef = -1;
    }
    if (gChestIndex < 7 && now >= xsArrayGetInt(gChestTimes, gChestIndex)) {
        if (gChestRef >= 0 && xsDoesUnitExist(gChestRef)) xsRemoveUnit(gChestRef);
        int count = 0;
        for (site = 0; < 9) {
            vector point = xsArrayGetVector(gFinals, site);
            if (royaleSafe(point)) { count++; if (xsGetRandomNumberMax(count) == 0) gChestPoint = point; }
        }
        gChestRef = royaleProp(${CHEST}, gChestPoint);
        gChestExpires = now + ${CHEST_LIFETIME};
        gChestSince = -1;
        gChestCandidate = 0;
        gChestIndex++;
        xsChatData("[Caravan] WAR CHEST at " + xsVectorGetX(gChestPoint) + "," + xsVectorGetY(gChestPoint) + " for 90s.");
    }
    if (gChestRef >= 0) {
        int chestTeam = royaleControl(gChestPoint);
        if (chestTeam == 0) { gChestSince = -1; return; }
        if (chestTeam != gChestCandidate || gChestSince < 0) { gChestCandidate = chestTeam; gChestSince = now; return; }
        if (now - gChestSince >= ${CHEST_CAPTURE}) {
            royaleTeamSupply(chestTeam, ${CACHE_WOOD}, ${CACHE_STONE}, true);
            royaleCaptureCount(chestTeam);
            xsRemoveUnit(gChestRef); gChestRef = -1;
            xsChatData("[Caravan] Team " + chestTeam + " secured the war chest!");
        }
    }
}

void royaleHazard(int now = 0) {
    int damageStage = gStage - 1;
    if (gStage < 9) {
        int closureStart = xsArrayGetInt(gStormDeadlines, gStage) - ${STORM_CLOSURE};
        if (now >= closureStart) damageStage = gStage;
    }
    if (damageStage < 0) return;
    float percent = 0.01 * xsArrayGetInt(gStormDamagePercent, damageStage);
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 0 || xsArrayGetInt(gState, color) == RESIGNED) continue;
        int owner = xsArrayGetInt(gOwners, color);
        gWorld = xsGetPlayerUnitIds(owner, -1, gWorld);
        for (index = 0; < xsArrayGetSize(gWorld)) {
            int reference = xsArrayGetInt(gWorld, index);
            if (royaleExists(reference, owner) == false || royaleSafe(royalePosition(reference))) continue;
            float hp = xsGetUnitHitpoints(reference) - xsGetUnitAttribute(reference, cHitpoints) * percent;
            if (hp < 0) hp = 0;
            xsSetUnitHitpoints(reference, hp);
        }
    }
}

void royaleHud(int now = 0) {
    int first = 0;
    int second = 0;
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 0) continue;
        int state = xsArrayGetInt(gState, color);
        if (state == ACTIVE) { if (royaleTeam(color) == 1) first++; else second++; }
        int owner = xsArrayGetInt(gOwners, color);
        int base = ${HUD_BASE} + (color - 1) * ${HUD_STRIDE};
        xsSetTriggerVariable(base, state);
        xsSetTriggerVariable(base + 1, xsArrayGetInt(gKills, color));
        xsSetTriggerVariable(base + 2, xsArrayGetInt(gDeaths, color));
        xsSetTriggerVariable(base + 3, xsArrayGetInt(gRank, color));
        xsSetTriggerVariable(base + 4, xsArrayGetInt(gKills, color) + xsArrayGetInt(gObjectiveXp, color));
        int owed = 0;
        for (level = 0; < 4) { if (xsArrayGetInt(gKills, color) >= xsArrayGetInt(gBuilderKills, level)) owed++; }
        xsSetTriggerVariable(base + 5, owed - xsArrayGetInt(gBuilderDelivered, color));
        xsSetTriggerVariable(base + 6, xsCeilToInt(xsPlayerAttribute(owner, cAttributeWood)));
        xsSetTriggerVariable(base + 7, xsCeilToInt(xsPlayerAttribute(owner, cAttributeStone)));
        xsSetTriggerVariable(base + 8, xsArrayGetInt(gRescued, color));
    }
    xsSetTriggerVariable(0, first);
    xsSetTriggerVariable(1, second);
    int storm = 0;
    if (gStage < 9) storm = xsArrayGetInt(gStormDeadlines, gStage) - now;
    xsSetTriggerVariable(2, storm);
    int remaining = ${RESCUE_CUTOFF} - now;
    if (remaining < 0) remaining = 0;
    xsSetTriggerVariable(3, remaining);
    remaining = ${DEADLINE} - now;
    if (remaining < 0) remaining = 0;
    xsSetTriggerVariable(4, remaining);
    xsSetTriggerVariable(5, gStage);
}

void royaleSetupColor(int color = 0) {
    int owner = xsArrayGetInt(gOwners, color);
    int civilization = xsGetPlayerCivilization(owner);
    int unit = ${CHAMPION};
    int cap = 70;
    int interval = 9;
    if (civilization > 0 && civilization < ${CIV_COUNT}) {
        unit = xsArrayGetInt(gCivUnits, civilization);
        cap = xsArrayGetInt(gCivCaps, civilization);
        interval = xsArrayGetInt(gCivIntervals, civilization);
    }
    else xsChatData("[Caravan] P" + color + " civilization is unmapped: Champion fallback 70 pop / 9s.");
    xsArraySetInt(gUnits, color, unit);
    xsArraySetInt(gMainCaps, color, cap);
    xsArraySetInt(gIntervals, color, interval);
    xsArraySetInt(gNextWave, color, interval);
    xsArraySetFloat(gBaseHp, color, xsGetObjectAttribute(owner, unit, cHitpoints));
    int attackClass = cDamageClassMelee;
    if (xsGetObjectAttribute(owner, unit, cAttack, cDamageClassPierce) > 0) attackClass = cDamageClassPierce;
    xsArraySetInt(gAttackClass, color, attackClass);
    xsArraySetFloat(gBaseAttack, color, xsGetObjectAttribute(owner, unit, cAttack, attackClass));
    royaleAttribute(owner, ${WAGON}, cHitpoints, ${WAGON_HP}.0);
    royaleAttribute(owner, ${WAGON}, cMovementSpeed, ${WAGON_SPEED});
    royaleAttribute(owner, ${WAGON}, cLineOfSight, 8.0);
    royaleAttribute(owner, ${WAGON}, cGarrisonCapacity, 0.0);
    royaleAttribute(owner, ${WAGON}, cConversionChanceMod, 0.0);
    royaleAttribute(owner, ${WAGON}, cHeroStatus, 2.0); // Conversion immunity without native hero regeneration.
    royaleAttribute(owner, ${WAGON}, 109, 0.0);
    royaleAttribute(owner, ${WAGON}, 120, 0.0);
    royaleAttribute(owner, ${WAGON}, 13, 0.0); // No economic work.
    royaleAttribute(owner, ${WAGON}, 14, 0.0); // No cargo.
    royaleAttribute(owner, ${WAGON}, 30, 0.0); // Cannot enter garrisons.
    royaleAttribute(owner, ${WAGON}, cAttack, 1024.0);
    royaleAttribute(owner, ${WAGON}, cAttack, 768.0);
    royaleArmor(owner, ${WAGON}, 2, 4);
    royaleAttribute(owner, ${HERO}, cHitpoints, ${HERO_HP}.0);
    float heroAttack = cDamageClassMelee * 256 + ${HERO_ATTACK};
    royaleAttribute(owner, ${HERO}, cAttack, heroAttack);
    royaleAttribute(owner, ${HERO}, cMovementSpeed, ${HERO_SPEED});
    royaleAttribute(owner, ${HERO}, cHeroStatus, 1.0);
    royaleAttribute(owner, ${HERO}, 30, 0.0);
    royaleArmor(owner, ${HERO}, 2, 2);
    royaleAttribute(owner, ${CASTLE}, cGarrisonCapacity, 0.0);
    royaleAttribute(owner, ${TOWER}, cGarrisonCapacity, 0.0);
    int wagon = xsArrayGetInt(gWagons, color);
    int hero = xsArrayGetInt(gHeroes, color);
    royaleProtected(wagon, false);
    xsSetUnitProperty(wagon, 10, 1.0, 0);
    royaleProtected(hero, true);
    royaleProtected(xsArrayGetInt(gCastles, color), true);
    xsSetUnitName(wagon, "Command Wagon - your army and team life");
    xsSetUnitName(hero, "Caravan Hero - escort allied wrecks to rescue");
    xsSetUnitHitpoints(wagon, ${WAGON_HP});
    xsSetUnitHitpoints(hero, ${HERO_HP});
    xsArraySetInt(gLastHp, color, ${WAGON_HP});
    xsArraySetVector(gLastWagon, color, royalePosition(wagon));
    xsSetPlayerAttribute(owner, 4, 200.0);
    xsSetPlayerAttribute(owner, 203, 1.0); // explored map, enemy LOS is still fogged.
    for (building = 0; < 10) {
        int type = ${TOWER};
        float wood = ${TOWER_WOOD};
        float stone = ${TOWER_STONE};
        if (building == 1) { type = ${WALL}; wood = ${WALL_WOOD}; stone = 0; }
        if (building == 2) { type = ${GATE}; wood = ${GATE_WOOD}; stone = 0; }
        if (building == 3) { type = ${BARRACKS}; wood = ${CAMP_WOOD}; stone = 0; }
        if (building == 4) { type = ${RANGE}; wood = ${CAMP_WOOD}; stone = 0; }
        if (building == 5) { type = ${STABLE}; wood = ${CAMP_WOOD}; stone = 0; }
        if (building >= 6) {
            type = ${GATE_SW}; wood = ${GATE_WOOD}; stone = 0;
            if (building == 7) type = ${GATE_NW};
            if (building == 8) type = ${GATE_EW};
            if (building == 9) type = ${GATE_NS};
        }
        xsEffectAmount(cEnableObject, type, 0, 1, owner);
        royaleAttribute(owner, type, cFoodCost, 0.0);
        royaleAttribute(owner, type, cWoodCost, wood);
        royaleAttribute(owner, type, cStoneCost, stone);
        royaleAttribute(owner, type, 105, 0.0); // gold cost
        royaleAttribute(owner, type, cGarrisonCapacity, 0.0);
    }
    for (birth = 0; < 8) royaleBirth(color, unit, xsArrayGetVector(gLastWagon, color), 1);
}

void royaleResolve() {
    for (color = 1; <= 8) {
        int reference = xsArrayGetInt(gWagons, color);
        if (reference < 0 || xsDoesUnitExist(reference) == false || xsGetUnitHitpoints(reference) <= 0) continue;
        int owner = xsGetUnitOwner(reference);
        if (owner < 1 || xsGetPlayerInGame(owner) == false) continue;
        // The same live owner must own all three anchors. Closed slots cannot borrow Gaia anchors.
        if (royaleExists(xsArrayGetInt(gCastles, color), owner) == false
            || royaleExists(xsArrayGetInt(gHeroes, color), owner) == false) continue;
        xsArraySetInt(gOwners, color, owner);
        xsArraySetInt(gOccupied, color, 1);
        xsArraySetInt(gState, color, ACTIVE);
    }
    gReady = true;
    gStart = 0; // The enforced deadline is exactly 70:00 on the game clock.
    royaleZones();
    royaleDecoration(${FIRE}); royaleDecoration(${WARNING}); royaleDecoration(${WRECK});
    royaleDecoration(${OUTPOST}); royaleDecoration(${CHEST});
    gWorld = xsGetPlayerUnitIds(0, ${OUTPOST}, gWorld);
    for (index = 0; < xsArrayGetSize(gWorld)) {
        int outpostRef = xsArrayGetInt(gWorld, index);
        royaleProtected(outpostRef, false); xsSetUnitProperty(outpostRef, 10, 0.0, 0);
    }
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 0) continue;
        royaleSetupColor(color);
        int mask = 0;
        for (ally = 1; <= 8) {
            if (royaleTeam(ally) == royaleTeam(color) && xsArrayGetInt(gOccupied, ally) == 1) {
                int bit = 1;
                for (power = 0; < xsArrayGetInt(gOwners, ally)) bit = bit * 2;
                mask = mask + bit;
            }
        }
        int visionOwner = xsArrayGetInt(gOwners, color);
        xsSetPlayerAttribute(visionOwner, 285, bitCastToFloat(mask));
        xsSetPlayerAttribute(visionOwner, 286, bitCastToFloat(mask));
    }
    royaleAbsorb();
    xsChatData("[Caravan] Protect your wagon. Enter the marked safe circle. Destroy every enemy wagon.");
    xsChatData("[Caravan] HOST: Faster 2x + Lock Speed. Finale at 70:00 game time (~35 active real minutes).");
}

void main() {
    ${ALLOCATIONS}
    ${INITIALIZERS}
}

void royaleTick() {
    if (gReady == false) {
        if (xsGetGameTime() < ${LOBBY_SETTLE_GAME_SECONDS}) return;
        royaleResolve();
    }
    if (gWinner != 0) return;
    int now = (xsGetGameTime() - gStart) / ${SPEED_FACTOR};
    if (now <= gLastTick) return;
    gLastTick = now;
    royaleCredit();
    // Deadline uses the pre-final-hazard snapshot; all result declarations use this latch.
    if (now >= ${DEADLINE}) {
        royaleOutcome(true);
        gStage = 9; gRadius = 0; gCenter = gFinal;
        gLastMarkers = -100; royaleMarkers(now); royaleHud(now); return;
    }
    royaleStorm(now);
    if (now >= ${WAGON_PROTECTION} && gProtectionReleased == false) {
        gProtectionReleased = true;
        for (color = 1; <= 8) {
            if (xsArrayGetInt(gOccupied, color) == 1) royaleProtected(xsArrayGetInt(gWagons, color), true);
        }
    }
    royaleLosses(now);
    if (gWinner != 0) { royaleHud(now); return; }
    if (now >= ${CASTLE_EVACUATION} && gEvacuated == false) {
        gEvacuated = true;
        for (color = 1; <= 8) {
            int reference = xsArrayGetInt(gCastles, color);
            if (xsDoesUnitExist(reference)) xsRemoveUnit(reference);
        }
        xsChatData("[Caravan] Castles evacuated. Your command wagon is now your only base.");
    }
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 1) { royaleSupply(color, 0, 0); royaleProduction(color, now); }
    }
    royaleObjectives(now);
    royaleHazard(now);
    royaleAbsorb();
    // Observe storm losses now, not one tick later; never process a new rescue after a wipe.
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 1 && xsArrayGetInt(gState, color) == ACTIVE
            && royaleExists(xsArrayGetInt(gWagons, color), xsArrayGetInt(gOwners, color)) == false)
            royaleLose(color, now);
    }
    royaleOutcome(false);
    royaleMarkers(now);
    royaleHud(now);
}

rule royaleHeartbeat
active
minInterval 1
{
    royaleTick();
}
