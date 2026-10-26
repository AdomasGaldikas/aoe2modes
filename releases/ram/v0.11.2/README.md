# RAM v0.11.2 playtest release

This release carries forward the v0.11.1 native exact-reference leader attack
increase: +3 base pierce attack every eight game seconds for each starting
leader. The original HP effects, ranged leaders and separate selection remain.
Native in-game attack growth still requires a fresh-match test.

The serialized Data Mod now copies the original Khan's population storage
values into every civilization's special leader. Inca, Muisca and Mapuche
previously inherited half-population values from their donor units; the other
civilizations retain their original accounting. The DAT round-trip verifies the
storage values for all 63 player tables. The archive build also rejects stale,
changed or unlisted files in existing output directories without deleting them.

The center, balance, and existing audio files are carried forward. Voice
playback, center rewards and multiplayer distribution remain subject to player
testing. For a fresh match select the matching RAM v0.11.2 Data Mod and
scenario. Old saves and games retain their embedded scenario triggers.
