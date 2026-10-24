// RAM_SIGNALS_BEGIN -- requests originate ONLY in synchronized MP selection triggers.
int gRamSignalLast = -1;

int ramSignalTeam(int color = 0) {
    if (color <= 4) return(1);
    return(2);
}

bool ramSignalAllowed(int color = 0, int event = 0) {
    if (color < 1 || color > 8 || event < 1 || event > 24) return(false);
    if (xsTriggerVariable(32 + color - 1) != 1) return(false);
    int target = event;
    if (event > 16) target = event - 16;
    else if (event > 8) target = event - 8;
    if (xsTriggerVariable(32 + target - 1) != 1) return(false);
    if (event <= 8) return(target == color);
    if (event <= 16) return(ramSignalTeam(target) != ramSignalTeam(color));
    return(target != color && ramSignalTeam(target) == ramSignalTeam(color));
}

void ramRequestSignal(int color = 0, int event = 0) {
    if (ramSignalAllowed(color, event) == false) return;
    if (gRamSignalLast < 0) gRamSignalLast = xsArrayCreateInt(9, -10000, "ramSignalLast");
    int now = xsGetGameTime();
    if (now - xsArrayGetInt(gRamSignalLast, color) < ${COOLDOWN_SECONDS}) return;
    if (xsTriggerVariable(${QUEUE_BASE} + color - 1) != 0) return;
    xsSetTriggerVariable(${QUEUE_BASE} + color - 1, event);
    xsArraySetInt(gRamSignalLast, color, now);
}

bool ramSignalCanDispatch(int color = 0) {
    if (xsTriggerVariable(${VOICE_BUSY}) != 0) return(false);
    int cursor = xsTriggerVariable(${CURSOR});
    for (offset = 1; <= 8) {
        int candidate = cursor + offset;
        if (candidate > 8) candidate = candidate - 8;
        int event = xsTriggerVariable(${QUEUE_BASE} + candidate - 1);
        if (ramSignalAllowed(candidate, event)) return(candidate == color);
    }
    return(false);
}

void ramSignalHousekeeping() {
    for (color = 1; <= 8) {
        int event = xsTriggerVariable(${QUEUE_BASE} + color - 1);
        if (event != 0 && ramSignalAllowed(color, event) == false) {
            xsSetTriggerVariable(${QUEUE_BASE} + color - 1, 0);
        }
    }
}

rule ramSignalHeartbeat
    active
    minInterval 1
{
    ramSignalHousekeeping();
}
// RAM_SIGNALS_END
