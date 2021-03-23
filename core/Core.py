# coding:utf-8
import os
import io
import time
import multiprocessing
from functools import partial

from PIL import Image, ImageMath

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision

from .models import * # cp from /home/voyager/jpz/chromosome/models
from .transforms import * # cp from /home/voyager/jpz/chromosome/transforms.py

from .temperature_scaling import ModelWithTemperature

ORIGINAL_SIZE = 1024
INPUT_SIZE = 512 # model input

class CoreDataset(Dataset):
    def __init__(self, trans):
        self.img_paths = []
        self.trans = trans

    def __getitem__(self, i):
        img = Image.open(self.img_paths[i])

        if img.mode == 'I':
            img = _convert_I16_to_L(img)

        img = img.convert('RGB')
        img = self.trans(img).float()

        return img

    def __len__(self):
        return len(self.img_paths)

    def _convert_I16_to_L(self, i16_img):
        return ImageMath.eval('im/256', {'im':i16_img}).convert('L')

class AbstractCore():
    def classify(self, img_path):
        """classify input chromosome img
        Args:
            img_path: str/PIL.Image
        Returns:
            res: list, model output data
        """
        start = time.time()
        self.net.eval()
        
        img = Image.open(img_path)
        
        if img.mode == 'I':
            img = self._convert_I16_to_L(img)
            
        img = img.convert('RGB')
        
        data = self.trans(img).float().unsqueeze(dim=0)
        data = data.to(self.device)

        with torch.no_grad():
            output = self.net(data)
            res = output.cpu().numpy().tolist()[0]
            
            return res

    def classify_batch(self, img_paths):
        """classify input chromosome img
        Args:
            img_path: str
        Returns:
            res: ndarray, model output data
        """
        self.dataset.img_paths = img_paths

        self.net.eval()

        results = []
        
        for data in self.loader:
            data = data.to(self.device)

            with torch.no_grad():
                output = self.net(data)
                res = output.cpu()

                results.append(res)

        return torch.cat(results)

    def _convert_I16_to_L(self, i16_img):
        im2 = ImageMath.eval('im/256', {'im':i16_img}).convert('L')
        
        return im2

class RegressCore(AbstractCore):
    def __init__(self, model_path, model_type='regress_resnet34', preprocess='autolevel',
                      device_name='cpu'):
        if os.path.exists(model_path) is False:
            raise Exception('model path {} not exists'.format(model_path))
        self.model_path = model_path
        self.model_type = model_type
        self.device_name = device_name
        
        self.device = torch.device(self.device_name)
        if preprocess == 'autolevel':
            Auto = Identity()
        elif preprocess == 'automask':
            Auto = AutoMask()
        else:
            raise Exception('No Such preprocess {}'.format(preprocess))
        
        self.trans = transforms.Compose([
            transforms.Grayscale(),
            Auto,
            AutoLevel(0.7, 0.0001),
            transforms.CenterCrop(size=ORIGINAL_SIZE),
            transforms.Resize(INPUT_SIZE),
            transforms.ToTensor()
        ])
        
        if model_type not in globals():
            raise Exception('No such model {} in core/models/'.format(model_type))
        self.net = globals()[model_type](False, num_classes=1)
        checkpoint = torch.load(model_path, map_location=lambda storage,loc: storage)
        self.net.load_state_dict(checkpoint['net'])
        self.net.to(self.device)
        
class ClassifyCore(AbstractCore):
    def __init__(self, model_path, model_type='resnet101', preprocess='autolevel', device_name='cpu',
                     num_classes=1, batch_size=1):
        if os.path.exists(model_path) is False:
            raise Exception('model path {} not exists'.format(model_path))
        self.model_path = model_path
        self.model_type = model_type
        self.device_name = device_name
        self.num_classes = num_classes
        
        self.device = torch.device(self.device_name)
        if preprocess == 'autolevel':
            Auto = AutoLevel(0.7, 0.0001)
        elif preprocess == 'automask':
            Auto = AutoMask()
        else:
            raise Exception('No Such preprocess {}'.format(preprocess))
        
        self.trans = transforms.Compose([
            PadSquare(),
            transforms.Resize((INPUT_SIZE, INPUT_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        if model_type not in globals():
            raise Exception('No such model {} in core/models/'.format(model_type))
        
        self.net = globals()[model_type](False, num_classes=num_classes)
        self.net = ModelWithTemperature(self.net)

        checkpoint = torch.load(model_path, map_location=lambda storage,loc: storage)

        # self.net.load_state_dict(checkpoint['net'])

        if 'module' in list(checkpoint.keys())[0]:
            new_state_dict = {}

            for key, value in checkpoint.items():
                new_state_dict[key.split('.', 1)[1]] = value

            self.net.load_state_dict(new_state_dict)
        else:
            self.net.load_state_dict(checkpoint)

        self.net.to(self.device)

        self.dataset = CoreDataset(self.trans)
        self.loader = DataLoader(
            self.dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=0,
            pin_memory=False
        )
