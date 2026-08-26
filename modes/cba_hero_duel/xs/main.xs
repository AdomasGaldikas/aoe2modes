// CBA Hero Duel — a tighter clock than the 4v4.
//
// Same contract as cba_hero/xs/main.xs: XS owns the wave counter, triggers own the
// map. The duel additionally publishes a sudden-death flag once the match runs long,
// which the trigger layer uses to stop replacing chaff and let the heroes settle it.

const int WAVE_INTERVAL_SECONDS = ${WAVE_INTERVAL};
const int SUDDEN_DEATH_WAVE     = ${SUDDEN_DEATH_WAVE};
const int WAVE_SIZE_BASE        = ${WAVE_SIZE_BASE};
const int WAVE_SIZE_CAP         = ${WAVE_SIZE_CAP};

int gWave = 0;
bool gAnnouncedSuddenDeath = false;

void main() {
    gWave = 0;
    publish(VAR_WAVE, 0);
    publish(VAR_WAVE_SIZE, WAVE_SIZE_BASE);
    publish(VAR_MATCH_SECONDS, 0);
    logLine("Duel start. Sudden death at wave " + SUDDEN_DEATH_WAVE + ".");
}

rule duelClock
    active
    minInterval 1
{
    publish(VAR_MATCH_SECONDS, matchSeconds());
}

rule duelWave
    active
    minInterval 1
{
    xsSetRuleMinIntervalSelf(WAVE_INTERVAL_SECONDS);

    gWave = gWave + 1;
    publish(VAR_WAVE, gWave);
    publish(VAR_WAVE_SIZE, clampInt(WAVE_SIZE_BASE + gWave, WAVE_SIZE_BASE, WAVE_SIZE_CAP));

    if (gWave >= SUDDEN_DEATH_WAVE && gAnnouncedSuddenDeath == false) {
        gAnnouncedSuddenDeath = true;
        logLine("Sudden death — no more reinforcements.");
        xsDisableSelf();
    }
}
