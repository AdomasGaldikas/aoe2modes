# CBA Hero 4v4: RAM v0.9.0

## RAM v0.9.0 civilization leaders and first balance pass

Each player's starting leader now uses a separate civilization-specific unit
definition copied from an existing DE hero, including its native graphics,
weapons, movement, class and attack animation. Examples include King Arthur for
Britons, Vytautas for Lithuanians, Saladin for Saracens and El Cid for Spanish.
The full 62-civilization catalog is in `assets/leaders/catalog.json`. Where no
suitable national land hero exists, explicitly documented commanders or visual
proxies are used. Arthur is legendary; the roster is game flavour, not one
historical period's simultaneous rulers.

Ranged leaders start with 300 HP and 25 attack, matching the old Genghis baseline.
Infantry leaders start with 450 HP/35 attack and melee cavalry with 420 HP/35
attack to compensate for closing to melee range. Melee leaders have 3/3 armour;
ranged leaders have 2/2. All use a two-second nominal reload while keeping native
attack animation timing. Existing +5 HP/+3 attack growth every eight game seconds
is retained; attack growth targets the actual melee or ranged damage class.
Special auras, splash, charge and weapon switching are disabled for these
isolated leader copies. Ordinary hero armies keep their original definitions.

The original eight placed references remain intact. Main leaders use selection
group 3 and stay separate from spawned units, even with the same appearance.
The Data Mod appends one reserved definition to every civilization's unit table;
removing these additions must restore all input DAT bytes exactly. Native DE
match loading, combat animation, save/load and double-click behavior still need
fresh-match acceptance. This scenario requires its matching Data Mod and cannot
be distributed as a working resource-only sound pack.

The initial army balance pass is deliberately limited:

| Civilization | Change |
| --- | --- |
| Lithuanians | Elite Leitis +8 HP; army cap 60 to 64; ten-second waves retained |
| Romans | Centurion wave interval eight to nine seconds |
| Varangians | Jarl army cap 80 to 72; wave interval eight to nine seconds |

These adjustments preserve native army weapons, counters and movement. They are
starting playtest values, not evidence of equal win rates. Center geometry,
team payouts, voice files and normal game speed are unchanged.

## RAM v0.8.0 civilization-wide selection voices

The selection-voice catalog now covers every civilization in the installed DE
dataset, including Chronicles and the latest additions. There are four newly
generated male military replies per supported civilization: infantry, bow archer,
mounted unit and leader. The existing five civilization sets are unchanged.
Contemporary language proxies are documented individually rather than presented
as reconstructed medieval or ancient speech. Romans use Latin through Higgs;
other new generated sets use the retained local OmniVoice model.

Where reliable local language support or native wording is unavailable, the
civilization keeps its original DE voices. Every such decision and its reason
is explicit in the packaged voice manifest. No stock game recordings are
extracted or redistributed. Native wording, pronunciation and live playback
still require listening review.

The package validates its complete civilization list against the actual game
dataset. A later game update that adds or renames a civilization fails with a
coverage error rather than silently leaving it unhandled. The hill, physical
control ram, 180-second kill payouts and normal gameplay pacing are unchanged.
Use the v0.8.0 Data Mod with its matching scenario in a fresh match.

## RAM v0.7.0 hill and moving control ram

The normal-speed release returns to the RAM name. Its mixed-content Data Mod
includes the twenty current military selection replies for Turks, Persians,
Khmer, Lithuanians and Spanish, alongside the existing center and Backup audio.
The separate Five Civ Voices test title is no longer the release name.

The center is a broad raised plateau with ordinary graded slopes on all eight
approaches. A protected Gaia ram shows the same percentage as the center HUD:
50/50 places it in the middle, 100/0 at Team 1's flag, and 0/100 at Team 2's
flag. Its synchronized position follows control directly, including contested
and empty-center equalization; players do not escort, attack or garrison it.
The indicator does not block armies, count toward capture or keep a player alive.

Team-wide snapshot kill payouts remain every 180 game seconds, up to 25 per
active teammate. Both teams present still equalize toward 50/50; neutral pays
neither team. Existing normal-speed progression and leader selection are retained.

Build the complete package with the optional DAT tooling installed:

```sh
python -m pip install -e '.[dev,ram-data]'
python modes/ram/package.py --game-dir /path/to/AoE2DE
```

Use **CBA Hero 4v4 RAM v0.7.0** as the Data Mod with its matching scenario in a
fresh match. A resource-only sound pack cannot enable the custom selection
bindings. Hill traversal, protected-ram rendering and multiplayer playback need
fresh native DE acceptance; Khmer and Lithuanian pronunciation remain experimental.


## RAM v0.6.0 playful announcer and villager selection

All **62 spoken lines** now use an original, brighter game-show announcer style:
faster delivery, lifted pitch and clarity EQ replace the old bass-heavy voice.
The spoken messages, private team recipients and shared audio queue are retained.
Every clip has a new event name so an older cached sound cannot mask the change.
Cooldowns are rebuilt from the new clips' actual durations. This release needs
both the v0.6.0 scenario and its updated sound assets; older scenarios and their
sound names remain available in previous release archives.

Double-click selects the **same exact unit type**, including upgraded forms and
Heroes. The exception is ordinary **villagers**: male and female villagers share
one selection group, including all their working forms. The change applies to
the player unit tables at match startup, so newly created builders also use it.
Civilizations and other civilian units do not become a shared selection group.
The eight starting Genghis Khan leaders use a separate group from spawned
Genghis armies in both directions. Each leader keeps its original reference,
stats, appearance and periodic HP/attack growth; no units are replaced.
The mixed-content Data Mod still uses the unchanged installed game dataset.
Native DE selection and second-client playback require a fresh-match check.

Release validation: all 14 RAM regression tests pass, including the frozen
normal-speed baseline with optional features disabled, strict audit, embedded XS
checks and execution of serialized center, private-signal and audio queues.
The written scenario checks all 64 native-owner leader bindings and all 27
villager forms. An independent local speech recognizer identifies the intended
player numbers and kill amounts across all 62 final clips. These checks do not
prove native selection behavior or audio playback on a second game client.

## RAM v0.5.0 team center control

Center kills now benefit **every active teammate**, including players with no
units in the center. A shared countdown pays once per 180 game seconds using
the control percentage **at that instant**, as requested. The leading team
must have at least one eligible combat unit on the point. Closed, defeated,
disconnected or unresolved slots cannot receive awards.

| Control split | Kills per active player on the leading team |
| --- | ---: |
| 50/50 | 0 |
| 55/45 | 2 |
| 60/40 | 5 |
| 75/25 | 12 |
| 100/0 | 25 |

For a team's control share `s > 50`, the award is
`floor(25 * (s - 50) / 50)`; the other team receives zero. The internal meter
uses exact integer steps, so contest cannot overshoot neutral or leak a reward
at 50/50. At the defaults, one team captures neutral to full in 60 seconds;
reversing full enemy control takes 120 seconds. Whenever both teams are present,
the meter drifts toward 50/50 over 300 seconds from full control, regardless of
unit numbers or Hero strength. It stays at neutral until a team leaves.
An empty point also returns toward neutral over 300 seconds and pays nothing.

The HUD shows both shares, both current awards and the common payout countdown.
Two fixed team flags show their team's share and award in their names. Actual
native kill awards, chat notices, Hero progression and existing spoken amounts
remain connected. The existing four-unit reinforcement bonus still requires
personal presence and full, uncontested control; contest pauses it.

This is a **scenario-only gameplay change** and reuses all v0.4.0 voice files.
A fresh v0.5.0 scenario is required; the existing RAM voice pack is compatible.
The mixed-content package also includes the new scenario for distribution.
Automated execution checks are separate from live DE acceptance.

## RAM v0.4.0 selectable team signals

Each player has an isolated signal island near the outer edge, beside their base
sector. Its eight colored Outposts are buttons: select one to request **Help**,
**Attack** one of the four enemies, or tell one of the other three teammates
**Don't feed**. The selected post's name identifies its command and owner.
The announcer voice and a `[TEAM]` chat line reach only that player's
occupied team slots, including the sender. Teams are P1–P4 and P5–P8.

Each player has a 12-game-second cooldown and one pending request. Deselect and
reselect to repeat; holding a post selected never repeats. Multi-selection
accepts at most one request. Only the island's owner can trigger its posts.
Closed or eliminated targets cannot be called, and eliminated players cannot
originate signals. Occupied defeated teammates can still hear their team.
Signals share the existing announcer queue and dispatch between players in
round-robin order, ahead of queued center notices once the current clip ends.
One-use Backup announcements retain priority. The 24 new lines bring the speech
library to 62 clips.

Input uses synchronized **Object Selected Multiplayer** conditions. Local-only
selection and local-player checks never mutate synchronized state. Native
owner selectors resolve both selection and private playback; audio routing
does not treat displayed colors as runtime player identities. Gaia ownership,
protected posts and a water moat keep these controls outside combat and defeat
logic. A fresh v0.4.0 match and the matching sound package are required.

Automated tests execute the written scenario's XS and native selection/audio
graph with independently permuted native selectors. Live DE selection and
second-client privacy remain separate acceptance checks.

RAM started as a self-contained copy of **normal RA v1.9**. Version 0.2.0 adds
an active center to that copy, keeping normal RA and RA Speed separate. Normal
army timings, unit statistics and the Hero ladder are retained. The mixed-content
package includes the original three-note startup chime at eight game seconds.

## RAM v0.3.0 deep-voice announcer

The same low-pitched Piper Joe voice now supplies **38 original speech clips**:

- Eight player-specific Scorpion Backup calls, broadcast to everyone.
- Exact center kill rewards from +1 through +25, spoken to the recipient.
- Team 1/2 securing the center, contested center and fully neutral center,
  broadcast to everyone. Capture requires the full meter; mere presence does
  not announce ownership. Status changes coalesce while waiting, with a
  12-game-second status cooldown.
- Center reinforcements, spoken to their recipient only after the first unit
  of a packet actually spawns. Population/space-blocked packets stay silent,
  and later delivery of the same partial packet does not repeat the line.

All speech shares the native Backup busy flag. Successful Backup calls have
dispatch priority, personal rewards remain in a bounded queue, and clips do not
overlap. Native cooldowns allow for audio playing in wall time while the game
clock runs faster: the default scale covers standard Fast (2x) as well as Normal.
The existing immediate, exact-amount center chat notice is retained.

Speech ships as canonical 48 kHz mono PCM WAV plus identical `.wem` aliases.
[DE update 185872](https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-185872/)
explicitly supports WAV data renamed to WEM and gives WEM lookup priority. The
aliases support native sound-event lookup without a third-party Wwise encoder.
The installer copies these uniquely named assets into this machine's game sound
directory as well as the mixed-content package.

RAM is published as an **unlisted Data Mod** under Wiorius:
[mod 551448](https://www.ageofempires.com/mods/details/551448/).
Restart DE to refresh subscribed mods, select this published RAM Data Mod when
creating the lobby, then select the RAM custom scenario. Joining players use
DE's mod subscription/download prompt to obtain the scenario and sound assets.
The normal scenario-file transfer alone does not carry external audio files.
Publication and the final listing are verified; a second-client download and
fresh multiplayer audio test remain unverified. See `publication.json` for the
stable service ID and uploaded archive hash; update this listing for later releases.
No active multiplayer match is interrupted for installation or testing.

`RAM-Sounds-v0.6.0.zip` contains the same scenario and speech as a normal resource
mod, with no `.dat`. Players can unpack it into a folder under `mods/local`,
enable **RAM Scenario and Sounds v0.6.0** in Mods, restart DE, then host the RAM
Custom Scenario with **Definitive Set**. Each computer needs this installed once.
The published mixed-content Data Mod remains the normal multiplayer path.

## RAM v0.2.2 center payout notifications

Each delivered center payout now shows its recipient a yellow chat notification,
for example **Center control: +15 kills!** The number is the exact queued award
applied to the native kill counter, including partial-control amounts and the
minimum +1 contested payout. The native payout invokes the notice after adding
kills and before clearing its queue, so a presence tick cannot announce an
undelivered reward. Other players do not receive that player's notification.

The message uses the existing XS owner bridge only to select the local viewer;
local-player checks never change synchronized state or the kill award. It is
embedded in the scenario and requires no extra audio file or Data Mod to display.
The 180-second payout interval and 5-to-25 growth settings are unchanged.

## RAM v0.2.1 corrections

Center payouts now add directly to the native **kills** resource (20), and thus
to the existing k HUD and normal kill-based Hero/age thresholds. The separate c
column and combined kill-plus-credit Hero guards are removed, avoiding double
counting. Native owner-resolved effects consume each queued center award once;
XS continues to sample presence and compute amounts. Only present combat-unit
owners accrue participation. Payout stays every 180 participation seconds:
continuous full control pays 15 after three held minutes, then 25 after six,
capped at 25. Capture time precedes held time. Contest pays the minimum 1,
pauses reinforcements and drains momentum. Absence pauses personal timers.

There are exactly **two** center flags: fixed Blue for Team 1 (P1–P4), fixed Teal
for Team 2 (P5–P8). Their color does not switch between individual teammates.
The old center flags, the additional flag ring, participant flags and all center
fire/torch effects are removed. The HUD shows capture percentage and payout.
Flags remain Gaia-owned to preserve player defeat and cleanup behavior.

Scorpion Backup announcements now use an entirely native one-use queue. The
successful activation sets its color's request; native playback acquires a shared
busy flag and plays the correct line to **every P1–P8**, regardless of camera
location. A native cooldown releases the busy flag after the clip and gap.
Simultaneous requests cannot overlap. A matching chat line confirms playback
was requested. No XS heartbeat is required to dispatch speech.

The voice WAVs use new `_v2` event names and a canonical 44-byte RIFF PCM header,
matching the working startup chime's container. FFmpeg metadata chunks were
removed without changing the decoded audio samples. The model/text/filter
provenance remains in `assets/audio/manifest.json` and `LICENSES.txt`.

The mixed-content Data Mod contains all required files for other clients. For
this machine's local testing, the installer also copies RAM's uniquely named
sound files into the installed game's `resources/_common/drs/sounds` directory.
That local convenience allows scenario-only testing if the unpublished Data Mod
is absent from the multiplayer selector. It does not distribute audio to another
computer: other clients must load the RAM package. Do not infer multiplayer
subscription/download acceptance from this local installation.

A new match is required; existing matches and saves contain their old scenario
logic. Restart DE after installing sounds so resource discovery can refresh.
The user's v0.2.0 test reported silent Backup audio, center points instead of
kills, and unwanted flags/fires. These are live reports; v0.2.0's automated
passes did not establish acceptance. v0.2.1 has new serialized native queue,
kill-delivery and visual-inventory regression tests. Fresh live verification
is still required.

## Build and package

From the repository root, with the project dependencies installed:

```sh
python -m aoe2modes build ram
python modes/ram/package.py --game-dir /path/to/steamapps/common/AoE2DE
python -m pytest tests/test_ram.py
```

The packaging command builds the scenario, copies the **unmodified installed**
`resources/_common/dat/empires2_x2_p1.dat`, synthesizes the chime, and writes:

- `dist/ram-mod/RAM-v0.6.0/` — local mixed-content mod directory.
- `dist/ram-mod/RAM-v0.6.0-mixed-content.zip` — mod upload ZIP, with `info.json`
  directly at its root.
- `dist/ram-mod/RAM-v0.6.0-manifest.json` — file sizes and SHA-256 hashes.

The mod contains:

```text
info.json
resources/_common/dat/empires2_x2_p1.dat
resources/_common/scenario/CBA Hero 4v4 RAM v0.6.0.aoe2scenario
resources/_common/drs/sounds/ram_startup_v1.wav
resources/_common/drs/sounds/ram_scorpion_p1_v3.wav  (through p8)
resources/_common/drs/sounds/ram_center_*.wav
resources/_common/drs/sounds/ram_team_*.wav
resources/_common/drs/sounds/ram_*.wem  (62 identical PCM speech aliases)
RAM_AUDIO_LICENSES.txt
RAM_AUDIO_MANIFEST.json
```

Rebuild the package after game dataset updates. The dataset is a game asset and
is intentionally kept in ignored build output, outside the source tree.

## Local and multiplayer acceptance

Close DE before installation. Copy the versioned mod directory to the active
profile's `mods/local`, or pass that parent directory to the packager's
`--install-local` option. Installation refuses to overwrite an existing folder.
Select published **CBA Hero 4v4 RAM v0.6.0** as the Data Mod when creating a lobby
and choose the matching v0.6.0 scenario. Unpublished local Data Mods can be absent
from the multiplayer selector; use the existing published listing for multiplayer.
Use a private unranked lobby, Normal game speed, opposing team
colors, and built-in AI opponents for a local smoke test.

A local mod installation does **not** test automatic downloads. That requires
publishing the ZIP as a data mod (unlisted is sufficient), selecting that
published mod when hosting, and joining from a second clean client/account.
Verify the download, dataset selection, scenario load, chime and normal spawning
on that client. Do not claim that acceptance from a local load or static tests.

Test screenshots, logs and live reports belong under
`/home/mo/.local/share/aoe2-ai-testing`, outside this repository.

## Previous v0.1.0 live validation on 2026-10-17

- Four RAM tests passed; scoped Ruff and `git diff --check` passed.
- 248,081 compared fields preserve normal RA v1.9 gameplay, allowing only branding
  and the audio probe. Strict scenario audit: zero errors and zero warnings.
- DE build 185872 recognises RAM as a data mod (gear icon), loads its dataset and
  bundled scenario in Skirmish, initializes all eight HUD rows, and spawns armies.
- Normal speed, cheats off, Full Tech Tree checkbox off, recording enabled; one
  human plus seven built-in AI opponents. This is a local smoke test, not a complete
  match or multiplayer acceptance.
- The original chime was detected in captured speaker output with normalized
  waveform correlation **0.960815**. No microphone input was recorded.
- Unpublished. No second client was available, so lobby subscription/download and
  remote audio remain untested. The user requested preparation only for now.
