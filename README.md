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

For Sequence numbers according to tool change:

```javascript
skipBlock = !insertToolCall;
    //Added tool description and moved around M03 code for desired effect.
    writeBlock("\n" + "N"+ sequenceNumber +"\n"+"T" + toolFormat.format(tool.number), mFormat.format(6),"("+ xyzFormat.format(tool.diameter) +" "
    + getToolTypeName(tool.type)+")\n");
    //Added sequence number increment. Do not use the sequence number setting
    //Moving this operation comment after tool change
    sequenceNumber += 1;
    if (hasParameter("operation-comment")) {
      var comment = getParameter("operation-comment");
      if (comment && ((comment !== lastOperationComment) || !patternIsActive || insertToolCall)) {
        //writeln(""); Removed the line from making additional line
        writeComment(comment);
        lastOperationComment = comment;
      } else if (!patternIsActive || insertToolCall) {
        writeln("");
      }
    } else {
      writeln("");
    }

    if (tool.comment) {
      //Remve the need for tool comment all together
      //writeComment(tool.comment);
    }
```
---
For fanuc-0I-MD (modded-1304),
- Removed P or dwell time value from tapping and drill operations due to personal preference.
---
For fanuc-0I-MD presetter (modded-0406),

_Using [Metrol TM26D](https://metrol-europe.com/tm26d/) touch type presetter._
- Added Presetter commands, M65, corresponding tool number and B-code when using **manual nc Measure tool** command.
- Optional global tolerance U code in microns through the options.

User Defined Options
```javascript
  globalPresetterTolerance: {
    title: "Presetter Tolerance",
    description: "Enable Global Tolerance",
    group: 0,
    type: "boolean",
    value: false,
    scope: "post"
  },
  toolPresetterTolerance: {
    title: "Global Presetter Tolerance (µ)",
    description: "Tolerance value 'u' in presetter",
    group: 0,
    type: "integer",
    value: 100,
    scope: "post"
  },
```
Actual Code
```javascript
case COMMAND_TOOL_MEASURE:
    var measureTool;
    var globalPresetterTolerance = getProperty("globalPresetterTolerance");
    valuetoolPresetterTolerance = getProperty("toolPresetterTolerance")* 0.001;

    if (!measureTool && globalPresetterTolerance) {
      writeBlock(
        mFormat.format(65),
        "T" + toolFormat.format(tool.number),
        "B" + xyzFormat.format(tool.number),
        "U" + valuetoolPresetterTolerance,
      );
    measureTool = true;
    }
    else {
      writeBlock(
        mFormat.format(65),
        "T" + toolFormat.format(tool.number),
        "B" + xyzFormat.format(tool.number)
      );
    measureTool = true;
    
    };
    return;
```
---
**Todo:**
- Sequence numbers according to Operation change.
- Option to have P or dwell time value in the post selection, instead of hard no.
- Tool by tool tolerance U code for presetter command.
- Optional Presetter feed control based on individual tool.
- Tool return to a designated home location.
- Cleanup Userdefined section for my context and remvoing unused settings.
