from transformers import pipeline

class BART:
   def __init__(self):
      self.name = 'bart'
      # self.model = pipeline('summarization', model='sshleifer/distilbart-cnn-6-6')
      self.model = pipeline('summarization', model='bart_model/')

      return