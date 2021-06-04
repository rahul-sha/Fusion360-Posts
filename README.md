# Fusion360-Posts
Collection of Posts I use in Fusion 360. So far only have for fanuc 0i-MD.
**Try it at your own risk.**

Here are the changes made to the generic fanuc post from Fusion 360 Library:

For fanuc-0I-MD (modded-2403).
- Program name in the next line.
- Time Stamp for when the file is post.
- Simplified Description of tool list.
- Sequence numbers according to tool change.
- M09, M01 occur before the tool change and the next operation.
- Removed tool comment and instead use tool type as an indicator for each operation.
---
For fanuc-0I-MD (modded-1304),
- Removed P or dwell time value from tapping and drill operations due to personal preference.
---
For fanuc-0I-MD presetter (modded-0406),

_Using [Metrol TM26D](https://metrol-europe.com/tm26d/) touch type presetter._
- Added Presetter commands, M65, corresponding tool number and B-code when using **manual nc Measure tool** command.
- Optional global tolerance U code in microns through the options.
---
**Todo:**
- Sequence numbers according to Operation change.
- Option to have P or dwell time value in the post selection, instead of hard no.
- Tool by tool tolerance U code for presetter command.
- Optional Presetter feed control based on individual tool.
- Tool return to a designated home location.
