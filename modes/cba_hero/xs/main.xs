// CBA Hero — match clock and wave pacing.
//
// Division of labour with the trigger layer:
//   * XS owns the clock. It counts waves, scales wave size, and publishes both into
//     trigger variables so trigger conditions can gate on them.
//   * Triggers own the map. Spawning and attack-move orders need concrete tile
//     coordinates, which the Python build already knows.
//
// Constants marked ${...} are substituted at build time by aoe2modes.lib.xs.read_xs,
// so mode.toml stays the single source of truth for pacing.

const int WAVE_INTERVAL_SECONDS = ${WAVE_INTERVAL};
const int WAVE_SIZE_BASE        = ${WAVE_SIZE_BASE};
const int WAVE_SIZE_STEP        = ${WAVE_SIZE_STEP};
const int WAVE_SIZE_CAP         = ${WAVE_SIZE_CAP};

int gWave = 0;

// Wave size grows linearly and then plateaus, so late-game lag stays bounded.
int waveSizeFor(int wave = 0) {
    return (minInt(WAVE_SIZE_BASE + (wave * WAVE_SIZE_STEP), WAVE_SIZE_CAP));
}

void main() {
    gWave = 0;
    publish(VAR_WAVE, 0);
    publish(VAR_WAVE_SIZE, waveSizeFor(0));
    publish(VAR_MATCH_SECONDS, 0);
    logLine("Match start. First wave in " + WAVE_INTERVAL_SECONDS + "s.");
}

rule matchClock
    active
    minInterval 1
{
    publish(VAR_MATCH_SECONDS, matchSeconds());
}

rule waveTick
    active
    minInterval 1
{
    xsSetRuleMinIntervalSelf(WAVE_INTERVAL_SECONDS);

    gWave = gWave + 1;
    publish(VAR_WAVE, gWave);
    publish(VAR_WAVE_SIZE, waveSizeFor(gWave));

    if (gWave % 5 == 0) {
        logLine("Wave " + gWave + " — reinforcements growing.");
    }
}
