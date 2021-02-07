import os

import numpy as np
import torch
import torch.nn as nn

from core_config import *
from core import Core

class CoreHandler():
    def __init__(self, core_name):
        """init core and handle this core.
        Args:
            core_name: str, CORE_ARGS's key
        """
        self.core_name = core_name
        assert core_name in CORE_ARGS

        self.core_arg = CORE_ARGS[core_name]
        self._check_arg(self.core_arg)

        arg = self.core_arg

        if 'regress' in arg['MODEL_TYPE']: # init regress model
            self.core = getattr(Core, 'RegressCore')(arg['MODEL_PATH'],  model_type=arg['MODEL_TYPE'],
                                        preprocess=arg['PREPROCESS'], device_name=arg['DEVICE_NAME'])
        else: # init focal model or classify model
            self.core = getattr(Core, 'ClassifyCore')(arg['MODEL_PATH'], model_type=arg['MODEL_TYPE'],
                                        preprocess=arg['PREPROCESS'], device_name=arg['DEVICE_NAME'],
                                        num_classes=arg['NUM_CLASSES'])
            
    def get_score(self, imageArr):
        """get score from imageArr
        Args:
            imageArr: PIL.Image
        Return:
            score: float
        """
        result = self.core.classify(imageArr)

        if 'regress' in self.core_name: # regress model post process
            score, THRESHOLD = result[0], self.core_arg['THRESHOLD']
            # when using regress model, good class label is 0, bad is 1.
            # using threshold to reverse the output value.
            if score < THRESHOLD:
                score = THRESHOLD + abs(score - THRESHOLD)
                if score >= 1: score = 1
            else:
                score = THRESHOLD - abs(score - THRESHOLD)
                if score <= 0: score = 0
            return score
        elif 'focal' in self.core_name: # focal model post process
            assert len(result) == self.core_arg['NUM_CLASSES']
            good, not_bad, bad = result
            print('focal post process {}'.format(result, flush=True))
            if np.argmax(result) == 0:
                if good-not_bad > not_bad - bad:
                    return 0.95
                else:
                    return 0.85
            elif np.argmax(result) == 1:
                if good - not_bad > not_bad - bad:
                    return 0.65
                else:
                    return 0.75
            else:
                return 0.6
        else: # classify model post process
            score = nn.functional.softmax(torch.Tensor(result), dim=-1)[1].item()

            return score
        
    def _check_arg(self, arg):
        """check the core arg and log the arg
        Args:
            arg: dict, value of CORE_ARGS
        """
        assert 'MODEL_PATH' in arg and os.path.exists(arg['MODEL_PATH'])
        assert 'MODEL_TYPE' in arg and 'DEVICE_NAME' in arg and 'PREPROCESS' in arg

        if 'regress' in self.core_name: # check regress model's arg
            assert 'THRESHOLD' in arg
        elif 'focal' in self.core_name: # check focal model's arg
            assert 'NUM_CLASSES' in arg
        else: # check classify model's arg
            pass
        
        print('GPU Worker set up, config:\n'
              '{}'.format(arg), flush=True)
              