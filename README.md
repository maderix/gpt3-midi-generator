# gpt-3 MIDI Generator

This is a simple tool that uses [gpt-3](https://github.com/openai/gpt-3) to generate MIDI music notes and then renders those notes to a monotone midi.

This tool is an experiment to see if Large language models can pick up some music theory and generate music based on note patterns. It is NOT a replacement for a real music generator and there are definately more capable ways to generate music.
Check out Magenta's [Music Generation](https://magenta.tensorflow.org/music_rnn) for a more robust music generator.
Also OpenAI's Jukebox is a more robust music generator.

Nevertheless, this is a fun experiment and I hope you find it useful.

Listen to some samples here:

https://twitter.com/originalmaderix/status/1534951205339660290?s=20&t=B0dcYkyHiZ1rXMr1MG04dA



## Requirements
<<<<<<< Updated upstream
- pygame
- wave
- openai api
- numpy
=======
1. Python 3.6+
2. pygame
3. wave
4. openai api
5. numpy
>>>>>>> Stashed changes

# Installation

To install, simply clone this repository and install the requirements:

```
git clone https://github.com/maderix/gpt-3-midi-generator.git
cd gpt-3-midi-generator
pip install -r requirements.txt
```

# Usage

To use, simply run `python gpt3_midi_generator.py`. By default, this will generate 100 notes for the Star Wars theme. The generated notes will be saved to `notes` folder, and a wav file will be generated and saved to `generated` folder.


You can customize the behavior with the following arguments:

#### `--model` 
The model to use for generation.Currently, the following models are supported:
 'text-davinci-002'
 'text-curie-001'
 'text-babbage-001'
 'text-ada-001'

#### `--prompt`

The prompt to use for gpt-3. This should be a string of space-separated phrase like 'Star Wars theme' or 'The original spiderman theme'.

#### `--length`

The length of the generated MIDI in notes.

#### `--temperature`

The temperature to use for gpt-3. This should be a float between 0 and 1, where 0 is the most deterministic and 1 is the most random.


#### `--play_song`

Whether or not to play the generated song. This requires pygame to be installed.

## Mixer settings

#### `--channels`
Default is 2.

#### `--sample_rate`
Default is 44100.

#### `--sample_width`
Default is 2.

More settings to be added in future

## OpenAI API

To use this tool, you need to sign up for an OpenAI API key. You can do so [here](https://openai.com/api/).
The request made by this tool will incur billing to your OpenAI account! Please measure usage accordingly.
Alternatively you can use a smaller model for generation (curie, babbage, etc.) by using the `--model` flag. In my experience, the curie is almost as good as davinci but incurs significantly less cost.

## Issues
Please report any issues by raising a bug request on this repo.


# License
MIT License
