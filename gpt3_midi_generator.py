from generate_midi import *


'''
Provide a helpful prompt for gpt-3 to specify the note types and get an idea of format.
You can experiment with different note types by adding or removing new notes.
Make sure to change the table in frequencies.py as well.
'''
#notes credit : https://noobnotes.net/super-mario-bros-theme-nintendo/
prompt_string = '''
Generate keyboard midi notes for 'Spiderman' theme:
D D# D D#
F F# F F#
G# G A# G#
D D# D D#
F F# F F#
G# G A# G#
A# A B A#
G G# G G#
F F# F F#
G# G A# G#
A# A B A#
G G# G G#
F F# F F#

Generate midi notes for "Mario" theme:
E E E
C E G G
C G E
A B Bb A
G E G A
F G E C D B
C G E
A B Bb A
G E G A
F G E C D B
G F# F D E
G A C
A C D
G F# F D E
C* C* C*
G F# F D E
G A C
A C D
D# D C
C C C
C D E C A G
C C C
C D E


Generate midi notes for "Twinkle Twinkle little star"
C C G G
A A G F
F F E E
D D C C
G G F F
E E D D
C C G G
A A G F
F F E E
D D C C
G G F F
E E D D
C C G G
F F E E
D D C

'''


import os
import openai

gpt_3_models = [
    'text-davinci-002',
    'text-davinci-001',
    'davinci-instruct-beta',
    'text-curie-001',
    'text-babbage-001',
    'text-ada-001',
    #add more models in future
]
if __name__ == '__main__':
    import argparse

    argparser = argparse.ArgumentParser(description='Use gpt-3 to generate midi music')
    argparser.add_argument('--prompt', type=str, default="Star Wars", help='Prompt to use for gpt-3 for notes generation')
    argparser.add_argument('--length', type=int, default=256, help='Length of generated midi')
    argparser.add_argument('--temperature', type=float, default=0.7, help='Temperature to use for gpt-3')
    #argparser.add_argument('--notes_file', type=str, default='notes/generated.txt', help='File to save notes to')
    #argparser.add_argument('--wav_file', type=str, default='generated/out.wav', help='File to save generated wav to')
    argparser.add_argument('--play_song', type=bool, default=True, help='Play the generated song')
    #advanced arguments
    argparser.add_argument('--model', type=str, default='text-davinci-001', help='Model to use for gpt-3')
    argparser.add_argument('--top_p', type=float, default=1.0, help='Top p to use for gpt-3')
    #frequency_penalty
    argparser.add_argument('--frequency_penalty', type=float, default=0.0, help='Frequency penalty to use for gpt-3')
    #presence_penalty
    argparser.add_argument('--presence_penalty', type=float, default=0.0, help='Presence penalty to use for gpt-3')
    #mixer arguments
    argparser.add_argument('--channels', type=int, default=4, help='Number of channels to use for gpt-3')
    argparser.add_argument('--sample_rate', type=int, default=22050, help='Sample rate to use for gpt-3')
    argparser.add_argument('--sample_width', type=int, default=2, help='Sample width to use for gpt-3')
    args = argparser.parse_args()

    #apply validations on arguments
    if args.model not in gpt_3_models:
        raise Exception('Model not supported. Supported models are: ' + str(gpt_3_models))
    if args.temperature < 0.0:
        raise ValueError('--temperature must be greater than 0.0')
    if args.top_p < 0.0 or args.top_p > 1.0:
        raise ValueError('--top_p must be between 0.0 and 1.0')
    if args.frequency_penalty < 0.0 or args.frequency_penalty > 1.0:
        raise ValueError('--frequency_penalty must be between 0.0 and 1.0')
    if args.presence_penalty < 0.0 or args.presence_penalty > 1.0:
        raise ValueError('--presence_penalty must be between 0.0 and 1.0')
    #length should be greater than 32 and less than 1024
    if args.length < 32 or args.length > 1024:
        raise ValueError('--length must be between 32 and 1024')

    #open and load the keyfile
    if os.path.exists('openai_key_file.txt'):
        keyfile = open('openai_key_file.txt', 'r')
        key = keyfile.read().split('\n')
        for line in key:
            if line.startswith('#'):
                continue
            else:
                openai.api_key = line
                break
        keyfile.close()
    elif os.getenv("OPENAI_API_KEY") is not None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        print("Please set your OpenAI API key in openai_key_file.txt or OPENAI_API_KEY environment variable")
        exit()
    
    prompt = prompt_string + '\nGenerate midi notes for "' +  args.prompt + '" :\n'
    #print(prompt)
try:
    response = openai.Completion.create(
      model=args.model,
      prompt=prompt,
      temperature=args.temperature,
      max_tokens=args.length,
      top_p=args.top_p,
      frequency_penalty=args.frequency_penalty,
      presence_penalty=args.presence_penalty
    )
except openai.OpenAIError as e:
    print('error communicating with OpenAI API:')
    print(e)
    exit()
finally:
    #parse the response and start generation
    #print(response.choices[0].text)
    generated_notes = response.choices[0].text
    #save the notes to a file
    notes_file_path = 'notes/' + '_'.join(args.prompt.split(' ')) + '.txt'
    notes_file = open(notes_file_path, 'w')
    notes_file.write(generated_notes)
    notes_file.close()
    #generate midi notes
    generated_wav_path = 'generated/' + '_'.join(args.prompt.split(' ')) + '.wav'
    print('Generating midi notes for ' + args.prompt + '...')
    print(notes_file_path, generated_wav_path)
    generate_and_save_wav(notes_file_path,
                        generated_wav_path,
                        args.channels,
                        args.sample_rate,
                        args.sample_width,
                        args.play_song)

