# text2midi
A program that takes text and converts it to MIDI art

## Usage

For now, you can run `text2midi` as follows. This will take the first argument (the message string), and generate the MIDI file that draws out the given message string.
```bash
python -m text2midi "<message_string>" path/to/output/file.mid
```

For example, you could run something like,

```bash
python -m text2midi "Hello, World\!" hello_world.mid
```

Now, to actually see this MIDI file (in piano roll) you can use the DAW of your choice. Logic Pro X, Reaper, GarageBand (?) would work just fine. 
