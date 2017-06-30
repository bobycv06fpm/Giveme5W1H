import json
from extractor.extractors.candidate import Candidate


class Writer:
    def __init__(self, outputPath, preprocessedPath):
        """
        :param path: Absolute path to the output directory
        """
        self._outputPath = outputPath
        self._preprocessedPath = preprocessedPath
        
    def _writeJson(self,  outputObject):
        outfile = open(self._outputPath +'/'+ outputObject['dId']+'.json', 'w')
        outfile.write(json.dumps(outputObject, sort_keys=False, indent=2))
        outfile.close()

    def writePickle(self, document):
        with open(self._preprocessedPath, 'wb') as f:
            # Pickle the 'data' document using the highest protocol available.
            pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)

    def get_preprocessedFilePath(self, id):
        return self._preprocessedPath + '/' + id + '.pickle'

    def getPreprocessedPath(self):
        return self._preprocessedPath
        
    def write(self, document):
        """
        :param document: The parsed Document
        :type document: Document

        :return: None
        """

        if self._outputPath:

            # reuse the input json as template for the output json
            output = document.get_rawData()


            # check if there isn`t already a fiveWoneH literal
            fiveWoneHLiteral =  output.setdefault('fiveWoneH',{})

            #Extract answers
            answers = document.get_answers()

            for question in answers:
                # check if question literal is there
                questionLiteral = fiveWoneHLiteral.setdefault(question, {'annotated': None, 'extracted': []})
                # check if extracted literal is there
                extractedLiteral = questionLiteral.setdefault('extracted', [])
                for answer in answers[question]:
                    if type(answer) is Candidate:
                        # answer was already refactored
                        words = []
                        for part in answer.getParts():
                            words.append({'text': part.getText(), 'tag': part.getPosTag()})
                        extractedLiteral.append({'score': answer.getScore(), 'words': words})
                    else:
                        # fallback for none refactored extractors
                        candidate_json = {'score': answer[1], 'words': []}
                        for candidateWord in answer[0]:
                            candidate_json['words'].append({ 'text':candidateWord[0], 'tag':candidateWord[1]})
                        extractedLiteral.append(candidate_json)

            self._writeJson( output)