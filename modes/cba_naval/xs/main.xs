// All combat is at sea. Color, trigger selector, and XS owner are separate domains.
const int FLEET_CAP = ${FLEET_CAP};
int gPorts = -1;
int gHeroPads = -1;
int gShips = -1;
int gOwners = -1;
int gOccupied = -1;
int gAlive = -1;
int gCleaned = -1;
int gWave = -1;
int gNextWave = -1;
int gNextFlagship = -1;
int gNextSiege = -1;
int gFlagship = -1;
int gHold = -1;
int gPrestige = -1;
int gRazings = -1;
int gPendingCannons = -1;
int gCenter = -1;
int gOrders = -1;
int gExtraPorts = -1;
int gBuilderPads = -1;
int gBuilders = -1;
int gSurvey = -1;
bool gReady = false;
bool gMatchStarted = false;
int gWinner = 0;
int gWinSince = -1;
int gLastTick = -1;

int navalTeam(int color = 0) {
    if (color <= 4) return (1);
    return (2);
}

bool navalExists(int reference = -1, int owner = -1) {
    if (reference < 0) return (false);
    if (xsDoesUnitExist(reference) == false) return (false);
    return (xsGetUnitHitpoints(reference) > 0 && xsGetUnitOwner(reference) == owner);
}

int navalPortReference(int color = 0, int port = 0) {
    if (port < 4) return (xsArrayGetInt(gPorts, color * 4 + port));
    return (xsArrayGetInt(gExtraPorts, color * ${EXTRA_PORTS} + port - 4));
}

int navalPorts(int color = 0) {
    int count = 0;
    int owner = xsArrayGetInt(gOwners, color);
    for (slot = 0; < 4 + ${EXTRA_PORTS}) {
        if (navalExists(navalPortReference(color, slot), owner)) count++;
    }
    return (count);
}

int navalRank(int color = 0) {
    int points = xsCeilToInt(xsPlayerAttribute(xsArrayGetInt(gOwners, color), cAttributeKills))
        + xsArrayGetInt(gPrestige, color);
    if (points >= ${RANK_3}) return (3);
    if (points >= ${RANK_2}) return (2);
    if (points >= ${RANK_1}) return (1);
    return (0);
}

vector navalLocal(int color = 0, vector point = vector(-1, -1, -1)) {
    float horizontal = xsVectorGetX(point);
    float vertical = xsVectorGetY(point);
    if (color == 1) return (xsVectorSet(vertical, horizontal, -1));
    if (color == 2) return (xsVectorSet(vertical, 144.0 - horizontal, -1));
    if (color == 3) return (point);
    if (color == 4) return (xsVectorSet(144.0 - horizontal, vertical, -1));
    if (color == 5) return (xsVectorSet(horizontal, 144.0 - vertical, -1));
    if (color == 6) return (xsVectorSet(144.0 - horizontal, 144.0 - vertical, -1));
    if (color == 7) return (xsVectorSet(144.0 - vertical, horizontal, -1));
    return (xsVectorSet(144.0 - vertical, 144.0 - horizontal, -1));
}

vector navalWorld(int color = 0, vector point = vector(-1, -1, -1)) {
    float horizontal = xsVectorGetX(point);
    float vertical = xsVectorGetY(point);
    if (color == 1) return (xsVectorSet(vertical, horizontal, -1));
    if (color == 2) return (xsVectorSet(144.0 - vertical, horizontal, -1));
    if (color == 3) return (point);
    if (color == 4) return (xsVectorSet(144.0 - horizontal, vertical, -1));
    if (color == 5) return (xsVectorSet(horizontal, 144.0 - vertical, -1));
    if (color == 6) return (xsVectorSet(144.0 - horizontal, 144.0 - vertical, -1));
    if (color == 7) return (xsVectorSet(vertical, 144.0 - horizontal, -1));
    return (xsVectorSet(144.0 - vertical, 144.0 - horizontal, -1));
}

void navalOrder(int color = 0, int fleetSlot = -1, int reference = -1, int producer = -1) {
    if (fleetSlot < 0 || fleetSlot >= FLEET_CAP) return;
    int owner = xsArrayGetInt(gOwners, color);
    if (navalExists(reference, owner) == false || navalExists(producer, owner) == false) return;
    vector boat = navalLocal(color, xsGetUnitPosition(reference));
    vector dock = navalLocal(color, xsGetUnitPosition(producer));
    float horizontal = xsVectorGetX(boat);
    float vertical = xsVectorGetY(boat);
    // Move into the lagoon, away from the actual launching shore. Pure MOVE
    // cannot stop to fight at the birth cell and block the next port wave.
    if (xsVectorGetX(dock) < 20.0) horizontal = horizontal + ${LAUNCH_CLEARANCE};
    else {
        if (xsVectorGetY(dock) < 54.5) vertical = vertical + ${LAUNCH_CLEARANCE};
        else vertical = vertical - ${LAUNCH_CLEARANCE};
    }
    if (horizontal < 22.5) horizontal = 22.5;
    if (horizontal > 30.5) horizontal = 30.5;
    if (vertical < 48.5) vertical = 48.5;
    if (vertical > 61.5) vertical = 61.5;
    vector clear = navalWorld(color, xsVectorSet(horizontal, vertical, -1));
    int unitIds = xsArrayGetInt(gOrders, color * FLEET_CAP + fleetSlot);
    xsArraySetInt(unitIds, 0, reference);
    // Each living birth has its own selector; no mutable shared route lookup.
    // Both commands are issued once, so later manual commands remain yours.
    xsTaskUnits(unitIds, 1, clear, -1, false, false, false, 0);
    xsTaskUnits(unitIds, 17, vector(72.5, 72.5, -1), -1, true, false, false, 0);
}


bool navalBirth(int color = 0, int unit = -1, int port = 0, bool flagship = false) {
    if (gReady == false) return (false);
    int owner = xsArrayGetInt(gOwners, color);
    if (xsArrayGetInt(gAlive, color) == 0) return (false);
    if (flagship && navalExists(xsArrayGetInt(gFlagship, color), owner)) return (false);
    int producer = navalPortReference(color, port);
    if (flagship == false && navalExists(producer, owner) == false) return (false);
    if (xsPlayerAttribute(owner, cAttributeMilitaryPopulation) >= FLEET_CAP) return (false);
    int freeSlot = -1;
    for (slot = 0; < FLEET_CAP) {
        if (navalExists(xsArrayGetInt(gShips, color * FLEET_CAP + slot), owner) == false) {
            freeSlot = slot;
            break;
        }
    }
    if (freeSlot < 0) return (false);
    int unitRef = -1;
    vector pad = xsArrayGetVector(gHeroPads, color);
    if (flagship == false) pad = xsGetUnitPosition(producer);
    vector localPad = navalLocal(color, pad);
    for (attempt = 0; < 10) {
        float dx = 3.0;
        float dy = 0.0;
        if (attempt > 0) {
            int cell = attempt - 1;
            if (cell == 4) continue;
            dx = 2.5 * (cell % 3 - 1);
            dy = 2.5 * (cell / 3 - 1);
        }
        if (flagship) {
            dx = 0.75 * (attempt % 3 - 1);
            dy = 0.75 * (attempt / 3 - 1);
            if (attempt == 0) { dx = 0.0; dy = 0.0; }
        }
        vector lagoonPoint = xsVectorSet(xsVectorGetX(localPad) + dx, xsVectorGetY(localPad) + dy, -1);
        if (xsVectorGetX(lagoonPoint) < 20 || xsVectorGetX(lagoonPoint) >= 32
            || xsVectorGetY(lagoonPoint) < 46 || xsVectorGetY(lagoonPoint) >= 64) continue;
        // All regular births stay at the producing dock's edge. No remote fallback pad.
        vector point = navalWorld(color, lagoonPoint);
        unitRef = xsCreateUnit(unit, owner, point, false, false, true);
        if (navalExists(unitRef, owner)) break;
    }
    if (navalExists(unitRef, owner) == false) return (false);
    xsArraySetInt(gShips, color * FLEET_CAP + freeSlot, unitRef);
    if (flagship) xsArraySetInt(gFlagship, color, unitRef);
    else navalOrder(color, freeSlot, unitRef, producer);
    return (true);
}

void navalWave(int color = 0) {
    int rank = navalRank(color);
    int wave = xsArrayGetInt(gWave, color);
    int ranged = ${GALLEY};
    int fire = ${FIRE_GALLEY};
    int demo = ${DEMOLITION_RAFT};
    int launchedCount = 0;
    int pending = xsArrayGetInt(gPendingCannons, color);
    bool siegeReleased = false;
    if (rank >= 1) { ranged = ${WAR_GALLEY}; fire = ${FIRE_SHIP}; demo = ${DEMOLITION_SHIP}; }
    if (rank >= 2) { ranged = ${GALLEON}; demo = ${HEAVY_DEMOLITION_SHIP}; }
    if (rank >= 3) fire = ${FAST_FIRE_SHIP};
    for (port = 0; < 4 + ${EXTRA_PORTS}) {
        if (navalExists(navalPortReference(color, port), xsArrayGetInt(gOwners, color))) {
            int phase = (wave + port) % 4;
            int unit = ranged;
            if (phase == 1) unit = fire;
            if (phase == 3) unit = demo;
            bool siege = pending > 0 && siegeReleased == false;
            if (siege) unit = ${CANNON_GALLEON};
            if (navalBirth(color, unit, port, false)) {
                launchedCount++;
                if (siege) { pending--; siegeReleased = true; }
            }
        }
    }
    xsArraySetInt(gPendingCannons, color, pending);
    if (launchedCount > 0) xsArraySetInt(gWave, color, wave + 1);
}

void navalRepair(int color = 0, int reference = -1, vector point = vector(-1, -1, -1)) {
    float hp = xsGetUnitHitpoints(reference);
    for (port = 0; < 4 + ${EXTRA_PORTS}) {
        int portRef = navalPortReference(color, port);
        if (navalExists(portRef, xsArrayGetInt(gOwners, color))) {
            vector dock = xsGetUnitPosition(portRef);
            float dx = xsVectorGetX(dock) - xsVectorGetX(point);
            float dy = xsVectorGetY(dock) - xsVectorGetY(point);
            if (dx * dx + dy * dy <= ${REPAIR_RADIUS} * ${REPAIR_RADIUS}) {
                float maximum = xsGetUnitAttribute(reference, cHitpoints);
                float repaired = hp + ${REPAIR_HP};
                if (repaired > maximum) repaired = maximum;
                if (repaired > hp) {
                    float applied = xsSetUnitHitpoints(reference, repaired);
                }
                // Nearby ports never stack healing. The heartbeat supplies one tick per second.
                break;
            }
        }
    }
}

void navalScan(int color = 0) {
    int owner = xsArrayGetInt(gOwners, color);
    int center = 0;
    for (slot = 0; < FLEET_CAP) {
        int reference = xsArrayGetInt(gShips, color * FLEET_CAP + slot);
        if (navalExists(reference, owner)) {
            vector point = xsGetUnitPosition(reference);
            navalRepair(color, reference, point);
            if (xsVectorGetX(point) >= 64 && xsVectorGetX(point) < 80
                && xsVectorGetY(point) >= 64 && xsVectorGetY(point) < 80) center++;
        }
    }
    xsArraySetInt(gCenter, color, center);
}

bool navalNeedsCleanup(int color = 0, int selector = 0) {
    if (gReady == false) return (false);
    return (xsArrayGetInt(gOccupied, color) == 1 && xsArrayGetInt(gAlive, color) == 0
        && xsArrayGetInt(gOwners, color) == xsGetWorldPlayerId(selector));
}

bool navalWins(int color = 0, int selector = 0) {
    if (gReady == false) return (false);
    return (gWinner == navalTeam(color) && xsArrayGetInt(gAlive, color) == 1
        && xsArrayGetInt(gOwners, color) == xsGetWorldPlayerId(selector));
}

void navalRefund(int owner = -1, int wood = 0, int stone = 0) {
    xsSetPlayerAttribute(owner, cAttributeWood, xsPlayerAttribute(owner, cAttributeWood) + wood);
    xsSetPlayerAttribute(owner, cAttributeStone, xsPlayerAttribute(owner, cAttributeStone) + stone);
}

void navalLimit(int owner = -1, int objectId = -1, int limit = 0, int wood = 0, int stone = 0) {
    gSurvey = xsGetPlayerUnitIds(owner, objectId, gSurvey);
    int count = xsArrayGetSize(gSurvey);
    // Include foundations and units already queued when disabling took effect.
    for (index = limit; < count) {
        if (xsRemoveUnit(xsArrayGetInt(gSurvey, index))) navalRefund(owner, wood, stone);
    }
    int available = 0;
    if (count < limit) available = 1;
    xsEffectAmount(cEnableObject, objectId, 0, available, owner);
}


void navalConstruction(int color = 0) {
    int owner = xsArrayGetInt(gOwners, color);
    for (slot = 0; < ${EXTRA_PORTS}) xsArraySetInt(gExtraPorts, color * ${EXTRA_PORTS} + slot, -1);
    gSurvey = xsGetPlayerUnitIds(owner, ${DOCK}, gSurvey);
    int extras = 0;
    int completed = 0;
    int count = xsArrayGetSize(gSurvey);
    for (index = 0; < count) {
        int reference = xsArrayGetInt(gSurvey, index);
        if (navalExists(reference, owner) == false) continue;
        bool original = false;
        for (slot = 0; < 4) {
            if (reference == xsArrayGetInt(gPorts, color * 4 + slot)) original = true;
        }
        if (original) continue;
        vector local = navalLocal(color, xsGetUnitPosition(reference));
        // Docks belong inside the lagoon, clear of the mouth and its turning room.
        if (xsVectorGetX(local) < 17 || xsVectorGetX(local) >= 30
            || xsVectorGetY(local) < 46 || xsVectorGetY(local) >= 64) {
            if (xsRemoveUnit(reference)) navalRefund(owner, ${PORT_WOOD}, 0);
            continue;
        }
        extras++;
        if (extras > ${EXTRA_PORTS}) {
            if (xsRemoveUnit(reference)) navalRefund(owner, ${PORT_WOOD}, 0);
            continue;
        }
        // A foundation has HP but is not a life, a repair point or a fleet producer.
        float required = xsGetUnitAttribute(reference, cTrainTime);
        if (required > 0 && xsGetUnitBuildPoints(reference) >= required) {
            xsArraySetInt(gExtraPorts, color * ${EXTRA_PORTS} + completed, reference);
            completed++;
        }
    }
    int available = 0;
    if (extras < ${EXTRA_PORTS}) available = 1;
    xsEffectAmount(cEnableObject, ${DOCK}, 0, available, owner);
    navalLimit(owner, ${WATCH_TOWER}, ${EXTRA_TOWERS}, ${TOWER_WOOD}, ${TOWER_STONE});
    navalLimit(owner, ${ARCHERY_RANGE}, ${ARCHERY_RANGES}, ${RANGE_WOOD}, 0);
    navalLimit(owner, ${ARCHER}, ${ARCHER_CAP}, ${ARCHER_WOOD}, 0);
}

void navalBuilders(int color = 0) {
    int owner = xsArrayGetInt(gOwners, color);
    int earned = xsArrayGetInt(gBuilders, color);
    int entitlement = xsCeilToInt(xsPlayerAttribute(owner, cAttributeKills)) / ${BUILDER_KILLS};
    if (entitlement > ${BUILDER_REWARDS}) entitlement = ${BUILDER_REWARDS};
    if (earned >= entitlement) return;
    vector pad = xsArrayGetVector(gBuilderPads, color);
    for (attempt = 0; < 6) {
        vector point = xsVectorSet(xsVectorGetX(pad) + attempt % 3 - 1,
            xsVectorGetY(pad) + attempt / 3, -1);
        int reference = xsCreateUnit(${VILLAGER}, owner, point, false, false, true);
        if (navalExists(reference, owner)) {
            xsArraySetInt(gBuilders, color, earned + 1);
            navalRefund(owner, ${BUILDER_WOOD}, ${BUILDER_STONE});
            break;
        }
    }
}

void main() {
    gPorts = xsArrayCreateInt(36, -1, "ports");
    gHeroPads = xsArrayCreateVector(9, vector(-1, -1, -1), "hero berths");
    gShips = xsArrayCreateInt(9 * FLEET_CAP, -1, "fleet references");
    gOwners = xsArrayCreateInt(9, -1, "owners");
    gOccupied = xsArrayCreateInt(9, 0, "occupied");
    gAlive = xsArrayCreateInt(9, 0, "alive");
    gCleaned = xsArrayCreateInt(9, 0, "cleaned");
    gWave = xsArrayCreateInt(9, 0, "wave");
    gNextWave = xsArrayCreateInt(9, ${LOBBY_SETTLE_SECONDS} + ${WAVE_INTERVAL}, "next wave");
    gNextFlagship = xsArrayCreateInt(9, 0, "next flagship");
    gNextSiege = xsArrayCreateInt(9, ${SIEGE_INTERVAL}, "next siege");
    gFlagship = xsArrayCreateInt(9, -1, "flagship");
    gHold = xsArrayCreateInt(9, 0, "sea hold");
    gPrestige = xsArrayCreateInt(9, 0, "prestige");
    gRazings = xsArrayCreateInt(9, 0, "razings");
    gPendingCannons = xsArrayCreateInt(9, 0, "pending cannons");
    gCenter = xsArrayCreateInt(9, 0, "center");
    // Bound memory to the tracked fleet. Each living birth has its own selector;
    // deferred engine commands cannot observe another ship overwriting it.
    gOrders = xsArrayCreateInt(9 * FLEET_CAP, -1, "birth order handles");
    for (slot = 0; < 9 * FLEET_CAP) {
        xsArraySetInt(gOrders, slot, xsArrayCreateInt(1, -1, "birth selector"));
    }
    gExtraPorts = xsArrayCreateInt(9 * ${EXTRA_PORTS}, -1, "completed extra ports");
    gBuilderPads = xsArrayCreateVector(9, vector(-1, -1, -1), "builder yards");
    gBuilders = xsArrayCreateInt(9, 0, "delivered builder rewards");
    gSurvey = xsArrayCreateInt(1, -1, "construction survey");
    ${INITIALIZERS}
}

void navalVision() {
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 0) continue;
        int owner = xsArrayGetInt(gOwners, color);
        int mask = 0;
        for (ally = 1; <= 8) {
            if (navalTeam(ally) != navalTeam(color)) continue;
            if (xsArrayGetInt(gOccupied, ally) == 0) continue;
            int allyOwner = xsArrayGetInt(gOwners, ally);
            int bit = 1;
            for (power = 0; < allyOwner) bit = bit * 2;
            mask = mask + bit;
        }
        // Bitfields use actual runtime owners, not editor colors or trigger selectors.
        xsSetPlayerAttribute(owner, 285, bitCastToFloat(mask));
        xsSetPlayerAttribute(owner, 286, bitCastToFloat(mask));
    }
}

void navalResolve() {
    for (color = 1; <= 8) {
        for (port = 0; < 4) {
            int reference = xsArrayGetInt(gPorts, color * 4 + port);
            if (xsDoesUnitExist(reference) && xsGetUnitHitpoints(reference) > 0) {
                int owner = xsGetUnitOwner(reference);
                if (owner > 0 && xsGetPlayerInGame(owner)) {
                    xsArraySetInt(gOwners, color, owner);
                    xsArraySetInt(gOccupied, color, 1);
                    xsArraySetInt(gAlive, color, 1);
                    break;
                }
            }
        }
    }
    gReady = true;
    navalVision();
    xsChatData("[Naval 0.5.1] Ships clear their dock before battle. 15s port waves; first fleet at 18s.");
}

void navalCombatScore(int owner = -1) {
    ${SCORE_NEUTRALIZE}
    xsSetPlayerAttribute(owner, cAttributeTotalValueOfKills, xsPlayerAttribute(owner, cAttributeKills) * 100);
    xsSetPlayerAttribute(owner, cAttributeValueKilledByOthers,
        xsPlayerAttribute(owner, cAttributeKilledByOthers) * 100);
    xsSetPlayerAttribute(owner, cAttributeTotalValueOfRazings, xsPlayerAttribute(owner, cAttributeRazings) * 500);
}

void navalTick() {
    int now = xsGetGameTime();
    // One economy/repair/reward tick per game second, even after duplicate callbacks.
    if (now <= gLastTick) return;
    gLastTick = now;
    if (gReady == false) {
        if (now < ${LOBBY_SETTLE_SECONDS}) return;
        navalResolve();
    }
    if (gWinner != 0) return;
    int first = 0;
    int second = 0;
    int firstCenter = 0;
    int secondCenter = 0;
    bool cleaned = true;
    int owner = -1;
    // Resolve all colors before rewards: a defeated navy cannot contest the sea.
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gOccupied, color) == 0) continue;
        owner = xsArrayGetInt(gOwners, color);
        if (xsArrayGetInt(gAlive, color) == 1) navalConstruction(color);
        int ports = navalPorts(color);
        if (ports == 0 || xsGetPlayerInGame(owner) == false) xsArraySetInt(gAlive, color, 0);
        xsSetTriggerVariable((color - 1) * ${HUD_STRIDE}, ports);
        xsSetTriggerVariable((color - 1) * ${HUD_STRIDE} + 1, xsCeilToInt(xsPlayerAttribute(owner, cAttributeKills)));
        xsSetTriggerVariable((color - 1) * ${HUD_STRIDE} + 2,
            xsCeilToInt(xsPlayerAttribute(owner, cAttributeKilledByOthers)));
        xsSetTriggerVariable((color - 1) * ${HUD_STRIDE} + 3, xsCeilToInt(xsPlayerAttribute(owner, cAttributeRazings)));
        xsSetTriggerVariable((color - 1) * ${HUD_STRIDE} + 4, navalRank(color));
        xsSetTriggerVariable((color - 1) * ${HUD_STRIDE} + 5, xsArrayGetInt(gWave, color));
        xsSetTriggerVariable((color - 1) * ${HUD_STRIDE} + 6, xsArrayGetInt(gBuilders, color));
        navalCombatScore(owner);
        if (xsArrayGetInt(gAlive, color) == 0) {
            if (xsArrayGetInt(gCleaned, color) == 0) cleaned = false;
            xsArraySetInt(gCenter, color, 0);
            continue;
        }
        navalScan(color);
        if (navalTeam(color) == 1) { first++; firstCenter = firstCenter + xsArrayGetInt(gCenter, color); }
        else { second++; secondCenter = secondCenter + xsArrayGetInt(gCenter, color); }
    }
    if (first > 0 && second > 0) gMatchStarted = true;
    if (gMatchStarted && (first == 0 || second == 0)) {
        if (cleaned == false) { gWinSince = -1; return; }
        if (gWinSince < 0) gWinSince = now;
        if (now - gWinSince >= ${VICTORY_DELAY}) {
            if (first > 0) gWinner = 1;
            if (second > 0) gWinner = 2;
        }
        return;
    }
    gWinSince = -1;
    for (color = 1; <= 8) {
        if (xsArrayGetInt(gAlive, color) == 0) continue;
        owner = xsArrayGetInt(gOwners, color);
        navalBuilders(color);
        int enemyCenter = firstCenter;
        if (navalTeam(color) == 1) enemyCenter = secondCenter;
        int hold = 0;
        if (xsArrayGetInt(gCenter, color) > 0 && enemyCenter == 0) hold = xsArrayGetInt(gHold, color) + 1;
        xsArraySetInt(gHold, color, hold);
        // DE rejects modulo mixed into a logical condition, despite xs-check accepting it.
        int prestigeRemainder = hold % ${CENTER_BONUS_INTERVAL};
        if (hold > 0 && prestigeRemainder == 0) {
            xsArraySetInt(gPrestige, color, xsArrayGetInt(gPrestige, color) + ${CENTER_BONUS});
        }
        int razings = xsCeilToInt(xsPlayerAttribute(owner, cAttributeRazings));
        int pending = xsArrayGetInt(gPendingCannons, color);
        if (now >= xsArrayGetInt(gNextSiege, color)) {
            pending++;
            xsArraySetInt(gNextSiege, color, now + ${SIEGE_INTERVAL});
        }
        if (razings > xsArrayGetInt(gRazings, color)) pending = pending + razings - xsArrayGetInt(gRazings, color);
        xsArraySetInt(gRazings, color, razings);
        int cannonRemainder = hold % ${CENTER_CANNON_INTERVAL};
        if (hold > 0 && cannonRemainder == 0) {
            pending++;
        }
        // All port production, including queued siege, shares the ordinary wave clock.
        xsArraySetInt(gPendingCannons, color, pending);
        int rank = navalRank(color);
        if (navalExists(xsArrayGetInt(gFlagship, color), owner)) {
            xsArraySetInt(gNextFlagship, color, 0);
        } else {
            if (xsArrayGetInt(gNextFlagship, color) == 0)
                xsArraySetInt(gNextFlagship, color, now + ${FLAGSHIP_INTERVAL});
        }
        int heroDue = xsArrayGetInt(gNextFlagship, color);
        if (heroDue > 0 && now >= heroDue) {
            int flagship = ${LONGBOAT};
            if (rank >= 2) flagship = ${TURTLE_SHIP};
            if (rank >= 3) flagship = ${ADMIRAL};
            if (navalBirth(color, flagship, 0, true))
                xsArraySetInt(gNextFlagship, color, 0);
        }
        if (now >= xsArrayGetInt(gNextWave, color)) {
            navalWave(color);
            xsArraySetInt(gNextWave, color, now + ${WAVE_INTERVAL});
        }
    }
}

rule navalHeartbeat
active
minInterval 1
{
    navalTick();
}
