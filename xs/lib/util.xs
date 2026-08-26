// Shared helpers used by every mode in this repo.
// Included via `xs.include = ["lib/util.xs"]` in a mode.toml.

// Trigger-variable ids that XS and the trigger layer agree on.
// Keep these in sync with aoe2modes.lib.variables in the Python side.
const int VAR_WAVE          = 0;
const int VAR_WAVE_SIZE     = 1;
const int VAR_MATCH_SECONDS = 2;

void logLine(string message = "") {
    xsChatData("[cba] " + message);
}

int clampInt(int value = 0, int low = 0, int high = 0) {
    if (value < low) {
        return (low);
    }
    if (value > high) {
        return (high);
    }
    return (value);
}

int maxInt(int a = 0, int b = 0) {
    if (a > b) {
        return (a);
    }
    return (b);
}

int minInt(int a = 0, int b = 0) {
    if (a < b) {
        return (a);
    }
    return (b);
}

// Whole seconds since the match started. xsGetTime() reports milliseconds.
int matchSeconds() {
    return (xsGetTime() / 1000);
}

// Publish a value so trigger conditions ("Variable Value") can read it.
void publish(int variableId = 0, int value = 0) {
    xsSetTriggerVariable(variableId, value);
}
