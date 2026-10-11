// Validator-only declaration for DE update 185872; never embedded.
// https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-185872/
int xsUnsyncGetLocalPlayerId() { return(0); }

// New exact-reference movement API from the same update. Validator only.
void xsTaskUnits(int unitIds = -1, int actionType = 0, vector location = vector(-1, -1, -1),
                 int locationObjectId = -1, bool isShiftQueue = false,
                 bool isFormationCommand = false, bool shouldPlayUnloadSound = false,
                 int patrolPoints = 0) {}

bool xsSetUnitOwner(int unitId = -1, int playerId = -1, bool flashUnit = true) { return(false); }
bool xsSetUnitProperty(int unitId = -1, int property = 0, float value = 0, int typeOrForce = 0) { return(false); }
