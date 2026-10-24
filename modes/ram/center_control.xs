// RAM_CENTER_BEGIN -- synchronized state; never use local-player APIs here.
int gRamPresence = -1;
int gRamSurvey = -1;
int gRamWaveClock = -1;
int gRamPending = -1;
int gRamLast = -1;
int gRamBalance = 0;
int gRamOwner = 0;
int gRamPayoutClock = 0;
int gRamVoiceState = 4;
// Fixed-point steps divide exactly: capture/equalization never overshoot 50/50.
const int cRamControlScale = ${CONTROL_SCALE};
const int cRamControlMinimum = ${CONTROL_MINIMUM};
const int cRamTeamOneFlag = ${TEAM1_FLAG};
const int cRamTeamTwoFlag = ${TEAM2_FLAG};
const int cRamCenterRam = ${CENTER_RAM};
const float cRamCenterRamMidX = ${CENTER_RAM_MID_X};
const float cRamCenterRamY = ${CENTER_RAM_Y};
const float cRamCenterRamHalfTravel = ${CENTER_RAM_HALF_TRAVEL};

void ramKeepCenterRamProperty(int property = 0, float value = 0) {
    if (xsGetUnitProperty(cRamCenterRam, property, -1) == value) return;
    if (xsSetUnitProperty(cRamCenterRam, property, value, -1) == false) return;
}

void ramProtectCenterRam() {
    if (xsDoesUnitExist(cRamCenterRam) == false) return;
    if (xsGetUnitOwner(cRamCenterRam) != 0) {
        if (xsSetUnitOwner(cRamCenterRam, 0, false) == false) return;
    }
    // Native attribute129 is an HP-floor multiplier:1.0 prevents attack damage
    // below full base HP, including splash/attack-ground damage. The pinned
    // parser omits its float-storage enum, so set it with the native XS API.
    if (xsGetUnitAttribute(cRamCenterRam, 129, -1) != 1.0) {
        xsEffectAmount(cSetUnitAttribute, cRamCenterRam, 129, 1.0, 0);
    }
    // Installed Constants.xs: capture6, deletion7, targeting8, attackable9,
    // selection10 and stance11. Zero capture blocks Gaia proximity claiming.
    ramKeepCenterRamProperty(6, 0.0);
    ramKeepCenterRamProperty(7, 0.0);
    ramKeepCenterRamProperty(8, 0.0);
    ramKeepCenterRamProperty(9, 0.0);
    ramKeepCenterRamProperty(10, 0.0);
    ramKeepCenterRamProperty(11, 3.0);
}

void ramMoveCenterRam() {
    if (xsDoesUnitExist(cRamCenterRam) == false) return;
    ramProtectCenterRam();
    // Positive balance belongs to Team1's left flag. Floating-point travel
    // follows every fixed-point step rather than rounding to displayed percent.
    float fraction = 1.0 * gRamBalance / cRamControlScale;
    if (fraction > 1.0) fraction = 1.0;
    if (fraction < -1.0) fraction = -1.0;
    float x = cRamCenterRamMidX - fraction * cRamCenterRamHalfTravel;
    // Exact-reference native repositioning avoids pathfinding and collision.
    // Never recreate the meter: its original scenario reference survives saves.
    vector destination = xsVectorSet(x, cRamCenterRamY, -1.0);
    if (xsSetUnitPosition(cRamCenterRam, destination, false) == false) return;
}

// Tint Gaia objects without transferring ownership. An eliminated player's
// cleanup must neither delete the shared indicators nor be kept alive by them.
void ramTint(int reference = -1, int color = 0) {
    if (xsDoesUnitExist(reference) == false) return;
    float tint = 8;
    if (color > 0) tint = color - 1;
    if (xsGetUnitProperty(reference, 13, -1) == tint) return;
    if (xsSetUnitProperty(reference, 13, tint, -1) == false) return;
}

void ramName(int reference = -1, string text = "") {
    if (xsSetUnitName(reference, text) == false) return;
}

int ramTeam(int color = 0) {
    if (color <= 4) return(1);
    return(2);
}

void ramInitialize() {
    gRamPresence = xsArrayCreateInt(9, 0, "ramPresence");
    gRamSurvey = xsArrayCreateInt(0, -1, "ramSurvey");
    gRamWaveClock = xsArrayCreateInt(9, 0, "ramWaveClock");
    gRamPending = xsArrayCreateInt(9, 0, "ramPending");

}

bool ramCenterEligible(int color = 0) {
    if (color < 1 || color > 8) return(false);
    int owner = cbaWorldPlayerForColor(color);
    if (owner < 1) return(false);
    if (xsTriggerVariable(32 + color - 1) != 1) return(false);
    return(xsGetPlayerInGame(owner));
}

int ramPresenceFor(int color = 0) {
    if (ramCenterEligible(color) == false) return(0);
    int owner = cbaWorldPlayerForColor(color);
    gRamSurvey = xsGetPlayerUnitIds(owner, -1, gRamSurvey);
    for (index = 0; < xsArrayGetSize(gRamSurvey)) {
        int reference = xsArrayGetInt(gRamSurvey, index);
        if (xsDoesUnitExist(reference) == false) continue;
        if (xsGetUnitOwner(reference) != owner) continue;
        if (xsGetUnitHitpoints(reference) <= 0) continue;
        if (xsGetUnitProperty(reference, 5, -1) >= 0) continue;
        if (xsGetUnitObjectId(reference) == ${PENGUIN}) continue;
        // Living combat classes only. No villagers, Kings, controllers, trade,
        // decorations or garrisoned units; a forward Castle cannot capture.
        if (xsGetUnitProperty(reference, 10004, -1) != 70) continue;
        int kind = xsGetUnitClass(reference);
        if ((${CLASSES}) == false) continue;
        vector point = xsGetUnitPosition(reference);
        float x = xsVectorGetX(point);
        float y = xsVectorGetY(point);
        if (x < ${X1} || x >= ${X2} || y < ${Y1} || y >= ${Y2}) continue;
        return(1);
    }
    return(0);
}

int ramIncomeFor(int team = 0, int present = 0) {
    if (present <= 0) return(0);
    int advantage = gRamBalance;
    if (team == 2) advantage = 0 - advantage;
    if (advantage <= 0) return(0);
    return(advantage * ${CREDIT_CAP} / cRamControlScale);
}

void ramEqualize(int seconds = 1) {
    int step = cRamControlScale / seconds;
    if (gRamBalance > 0) {
        gRamBalance = gRamBalance - step;
        if (gRamBalance < 0) gRamBalance = 0;
    }
    else if (gRamBalance < 0) {
        gRamBalance = gRamBalance + step;
        if (gRamBalance > 0) gRamBalance = 0;
    }
}

bool ramBirth(int color = 0) {
    if (ramCenterEligible(color) == false) return(false);
    int owner = cbaWorldPlayerForColor(color);
    if (owner < 1 || gCbaUnitByCiv < 0) return(false);
    int civ = xsGetPlayerCivilization(owner);
    if (civ < 1 || civ >= xsArrayGetSize(gCbaUnitByCiv)) return(false);
    int unit = xsArrayGetInt(gCbaUnitByCiv, civ);
    if (unit < 0) return(false);
    if (cbaHasPopulationRoom(owner, unit, 1) == false) return(false);
    int reference = -1;
    ${BIRTHS}
    return(false);
}

void ramIndicators(int state = 0) {
    ramMoveCenterRam();
    // Fixed team colors: Blue for P1-P4, Teal for P5-P8. Never switch the
    // controlling team's flag to whichever teammate happens to be sampled last.
    int first = 0;
    int second = 0;
    if (gRamOwner == 1 || state == 3) first = 1;
    if (gRamOwner == 2 || state == 3) second = 5;
    ramTint(cRamTeamOneFlag, first);
    ramTint(cRamTeamTwoFlag, second);
    int ramColor = 0;
    if (gRamOwner == 1) ramColor = 1;
    if (gRamOwner == 2) ramColor = 5;
    ramTint(cRamCenterRam, ramColor);
    ramName(cRamTeamOneFlag, "Team 1 (P1-P4): " + xsTriggerVariable(${METER})
        + "% | +" + xsTriggerVariable(${TEAM1_RATE}) + " kills per teammate / ${PAYOUT_SECONDS}s");
    ramName(cRamTeamTwoFlag, "Team 2 (P5-P8): " + xsTriggerVariable(${TEAM2_SHARE})
        + "% | +" + xsTriggerVariable(${TEAM2_RATE}) + " kills per teammate / ${PAYOUT_SECONDS}s");
}

void ramCenterTick() {
    if (xsTriggerVariable(56) != 1) return;
    if (gRamPresence < 0) ramInitialize();
    int now = xsGetGameTime();
    // One observation per game second; never credit a scheduling gap using a
    // single current snapshot. The shared clock and arrays survive save/load.
    if (now <= gRamLast) return;
    gRamLast = now;
    int first = 0;
    int second = 0;
    for (color = 1; <= 8) {
        int present = ramPresenceFor(color);
        xsArraySetInt(gRamPresence, color, present);
        xsSetTriggerVariable(${PRESENT_BASE} + color - 1, present);
        if (color <= 4) first = first + present;
        else second = second + present;
        if (ramCenterEligible(color) == false) {
            xsSetTriggerVariable(${KILL_PENDING_BASE} + color - 1, 0);
            xsArraySetInt(gRamWaveClock, color, 0);
            xsArraySetInt(gRamPending, color, 0);
        }
    }
    bool contested = first > 0 && second > 0;
    int solo = 0;
    int state = 0;
    if (first > 0 && second == 0) solo = 1;
    if (second > 0 && first == 0) solo = 2;
    state = solo;
    if (contested) state = 3;
    if (solo == 1) gRamBalance = gRamBalance + cRamControlScale / ${CAPTURE_SECONDS};
    if (solo == 2) gRamBalance = gRamBalance - cRamControlScale / ${CAPTURE_SECONDS};
    // Any opposing presence contests. Outnumbering an enemy never pushes the
    // bar through neutral while both teams remain on the point.
    if (contested) ramEqualize(${EQUALIZE_SECONDS});
    if (first == 0 && second == 0) ramEqualize(${EMPTY_RESET_SECONDS});
    if (gRamBalance > cRamControlScale) gRamBalance = cRamControlScale;
    if (gRamBalance < cRamControlMinimum) gRamBalance = cRamControlMinimum;
    int previous = gRamOwner;
    gRamOwner = 0;
    if (gRamBalance > 0) gRamOwner = 1;
    if (gRamBalance < 0) gRamOwner = 2;
    if (gRamOwner != previous) {
        for (color = 1; <= 8) {
            xsArraySetInt(gRamWaveClock, color, 0);
            xsArraySetInt(gRamPending, color, 0);
        }
    }
    int firstRate = ramIncomeFor(1, first);
    int secondRate = ramIncomeFor(2, second);
    gRamPayoutClock = gRamPayoutClock + 1;
    if (gRamPayoutClock >= ${PAYOUT_SECONDS}) {
        // Snapshot at the payout tick, deliberately not a time average.
        // One holder earns the SAME award for every living teammate.
        for (color = 1; <= 8) {
            if (ramCenterEligible(color) == false) continue;
            int award = firstRate;
            if (ramTeam(color) == 2) award = secondRate;
            if (award <= 0) continue;
            int earned = xsTriggerVariable(${CREDIT_BASE} + color - 1);
            xsSetTriggerVariable(${CREDIT_BASE} + color - 1, earned + award);
            int queued = xsTriggerVariable(${KILL_PENDING_BASE} + color - 1);
            xsSetTriggerVariable(${KILL_PENDING_BASE} + color - 1, queued + award);
        }
        xsSetTriggerVariable(${TEAM1_LAST}, firstRate);
        xsSetTriggerVariable(${TEAM2_LAST}, secondRate);
        gRamPayoutClock = 0;
    }
    bool holding = false;
    if (solo == 1 && gRamBalance == cRamControlScale) holding = true;
    if (solo == 2 && gRamBalance == cRamControlMinimum) holding = true;
    for (color = 1; <= 8) {
        if (holding == false || ramTeam(color) != solo) continue;
        if (xsArrayGetInt(gRamPresence, color) == 0) continue;
        int pending = xsArrayGetInt(gRamPending, color);
        int wave = xsArrayGetInt(gRamWaveClock, color);
        if (pending == 0) wave = wave + 1;
        if (wave >= ${REINFORCEMENT_SECONDS}) {
            pending = ${REINFORCEMENT_UNITS};
            wave = 0;
        }
        for (index = 0; < ${REINFORCEMENT_UNITS}) {
            if (pending <= 0) break;
            if (ramBirth(color) == false) break;
            if (${CENTER_AUDIO_ENABLED} == 1 && pending == ${REINFORCEMENT_UNITS}) {
                xsSetTriggerVariable(${CENTER_WAVE_VOICE_BASE} + color - 1, 1);
            }
            pending = pending - 1;
        }
        xsArraySetInt(gRamPending, color, pending);
        xsArraySetInt(gRamWaveClock, color, wave);
    }
    int firstShare = 50 + gRamBalance * 50 / cRamControlScale;
    xsSetTriggerVariable(${METER}, firstShare);
    xsSetTriggerVariable(${TEAM2_SHARE}, 100 - firstShare);
    xsSetTriggerVariable(${TEAM1_RATE}, firstRate);
    xsSetTriggerVariable(${TEAM2_RATE}, secondRate);
    xsSetTriggerVariable(${TEAM1_PRESENT}, first);
    xsSetTriggerVariable(${TEAM2_PRESENT}, second);
    xsSetTriggerVariable(${COUNTDOWN}, ${PAYOUT_SECONDS} - gRamPayoutClock);
    xsSetTriggerVariable(${STATE}, state);
    xsSetTriggerVariable(${BONUS}, firstRate + secondRate);
    if (${CENTER_AUDIO_ENABLED} == 1) {
        int speechState = 0;
        if (contested) speechState = 3;
        else if (solo == 1 && gRamBalance == cRamControlScale) speechState = 1;
        else if (solo == 2 && gRamBalance == cRamControlMinimum) speechState = 2;
        else if (first == 0 && second == 0 && gRamBalance == 0) speechState = 4;
        if (speechState == 0) xsSetTriggerVariable(${CENTER_STATUS_VOICE}, 0);
        else if (speechState != gRamVoiceState) {
            xsSetTriggerVariable(${CENTER_STATUS_VOICE}, speechState);
            gRamVoiceState = speechState;
        }
    }
    ramIndicators(state);
}

rule ramCenterHeartbeat
    active
    minInterval 1
{
    ramCenterTick();
}
// RAM_CENTER_END

// RAM_CENTER_NOTICES_BEGIN -- presentation only, after the native kill award.
// Local player identity must never affect synchronized center or reward state.
void ramAnnounceCenterKills(int color = 0) {
    if (color < 1 || color > 8) return;
    int owner = cbaWorldPlayerForColor(color);
    if (owner < 1 || owner != xsUnsyncGetLocalPlayerId()) return;
    int amount = xsTriggerVariable(${KILL_PENDING_BASE} + color - 1);
    if (amount <= 0) return;
    xsChatData("<YELLOW>Team center control: +%d kills!", amount);
}
// RAM_CENTER_NOTICES_END
