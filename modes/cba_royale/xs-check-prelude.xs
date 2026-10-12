// Validator-only signatures from DE update 185872. Never embedded.
void xsTaskUnits(int unitIds = -1, int actionType = 0, vector location = vector(-1, -1, -1),
    int locationObjectId = -1, bool isShiftQueue = false, bool isFormationCommand = false,
    bool shouldPlayUnloadSound = false, int patrolPoints = 0) {}
float xsGetUnitProperty(int unitId = -1, int property = 0, int typeOrPlayer = -1) { return (0.0); }
bool xsSetUnitProperty(int unitId = -1, int property = 0, float value = 0.0,
    int typeOrForce = -1) { return (false); }
bool xsSetUnitName(int unitId = -1, string name = "") { return (false); }
