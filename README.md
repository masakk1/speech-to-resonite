# speech-to-resonite
STR (Speech-To-Resonite), is a tool that bridges the gap between speech-recognition and Resonite. Targeted mostly at development.

This python program exposes a websocket port (8069) that sends both speech and recognized commands.
Which means that the commands have to be configured in the program, outside Resonite.

> [!NOTE]
> This is heavily targeted towards development. Which means that it will detect only development-specific commands! Useful as a development copilot, but not as speech-to-text. Use other tools for that.

> [!WARNING]
> The node list is **likely outdated!** - If you want to update the node list, check out [Updating](#updating).

## Installation
STR requires python 3. The dependencies are listed in the `requirements.txt` file. Though they are more of a reference.

## Usage
### STRMng - Existing tool
There's an already made tool built with-in resonite that allows you to *spawn* nodes, though it doesn't do much more.

Open an issue if you need the tool.

### Custom tools
#### Implementation
To make your own implementation, you'll have to listen for the port `8069` and parse strings like this:
`SPK-{speech}CMD-{command}`

1. `SPK-{speech}` is the raw recognized words. It often makes grammar errors, but may be useful.
2. `CMD-{command}` is the parsed string parsed using the `data/config.json`. Which tries to recognize commands as well as grammar correction.

#### Configuration
Speech-to-resonite relies on `data/config.json` to do most of the parsing and grammar correction. 

- `cmd`: the list of available commands. It will match the highest in the list.
- `node_type_fallback`: the fallback node in case of an empty *"type"* command.
- `grammar`: additional grammar for the vosk model.
  - `add`: list of words for the vosk model to recognize. Words/Letters separated by spaces count as different words. So "u long" would be both "u" and "long". (though adding types shouldn't be necessary)
  - `remove`: list of words for the vosk model to ignore. These are on top of the existing dictionaries
- `bindings`: all the aliases for commands and node names
  - `cmd`: list of commands to parse. `new` being the command and `replace` being the text to replace.
  - `node`: list of aliases for node names. `new` being the string to add and `replace` being the text to replace. **Used by NEWNODE**
  - `node_type`: same as nodes but for node types. **Used by NODETYPE**.

#### Note
I'm cheating a little here by relying on the command NEWNODE and NODETYPE. These are actually calculated in the program, not Resonite. Since I wanted to do phonetic searches, which give out-standing results at the cost of doing it outside of Resonite.

### Updating
It will quickly get out of date, so I recommend updating the node list every now and then.

To do so, inside `data/dictionaries/`:

1. Update `funnystring.txt` from this repo: https://github.com/Spaceey1/funnyResoniteNodeListString. Note that that one might be outdated itself, but you can update it with the provided tools.
2. Update `typestring.txt` with whatever types you know have been added. Unfortunately, I did these manually. Though this is fine since most of the time you'll be using the default types and converting them from there.
3. Run the python script `funnystring_to_json.py` like so: `funnystring_to_json.py <funnystring.txt> <typestring.txt> <resonite-node-database.json>` - Make sure the output is inside `dictionaries` and that the `funnystring.txt` follows the same format.

Otherwise you could make your own `resonite-node-database.json`. So long as you provide the same format.

