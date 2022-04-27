import torch
import os

def transcription(clip):

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    # print('device = ' + str(device))
    model, decoder, utils = torch.hub.load(repo_or_dir='silero_model/',
                                        model='silero_stt',
                                        language='en', # also available 'de', 'es'
                                        device=device)
    (read_batch, split_into_batches,
    read_audio, prepare_model_input) = utils  # see function signature for details

    filename = clip[:-4]

    # remove spaces for naming directory
    if ' ' in filename:
        filename = ''.join(word for word in filename.split(' '))

    # split file
    if not os.path.isdir(filename):
        os.system('mkdir ' + filename)
        
        command = 'ffmpeg -i ' + clip + ' -f segment -segment_time 60 -c copy ' + filename + '/output_audio_file_%03d.mp3'

        os.system(command)

    files = os.listdir(filename)
    files.sort()

    text = []
    for f in files:
        path = os.path.join(filename, f)
        path = [path]
        inputs = prepare_model_input(read_batch(path), device=device)
        outputs = model(inputs)
        
        for o in outputs:
            text.append(decoder(o.cpu()))

    # delete directory
    os.system('rm -r ' + filename)
    os.system('rm ' + clip)

    return text