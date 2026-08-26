// Randomness helpers.
//
// Every player's XS instance runs the same code on the same seed, so these stay in
// sync across a multiplayer lobby as long as they are only called from rules that
// every player runs. Never branch on xsGetLocalPlayerId() before calling them.

// Inclusive on both ends. xsGetRandomNumberMax(n) yields 0..n-1.
int randRange(int low = 0, int high = 0) {
    if (high <= low) {
        return (low);
    }
    return (low + xsGetRandomNumberMax(high - low + 1));
}

// Returns true with `percent` probability.
bool chance(int percent = 50) {
    return (randRange(1, 100) <= percent);
}

// Pick a random entry from an int array created with xsArrayCreateInt.
int randomFrom(int arrayId = -1) {
    int size = xsArrayGetSize(arrayId);
    if (size <= 0) {
        return (-1);
    }
    return (xsArrayGetInt(arrayId, randRange(0, size - 1)));
}
