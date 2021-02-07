# 测试染色体分类的预处理以及分类代码是否可用
# 下为预处理代码
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import os
import pickle
import argparse
import itertools


import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import torch.nn.init as init
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

# from datasets.simple import *
# from resnet import *
from transforms import *
from plot import *
from resnet import *
from ClassifyCore import ClassifyCore


# 测试预处理

def read_image_list_pil():
    image_root = '/home/voyager/project/chromosome-classifier/input'
    image_list = os.listdir(image_root)
    #print(image_list)
    image_list = [image for image in image_list if 'JPG' in image]
    images = [Image.open(os.path.join(image_root, image_file)) for image_file in image_list]
    print(type(images[0]))
    return images, image_list


def show_image_list(images, idx=None):
    """images: list[ndarray] or list[PIL.Image]"""
    for image in images:
        plt.imshow(image)
        plt.show()
        
def get_transform(original_size=1024, resize=448):
    return transforms.Compose([
        transforms.Grayscale(),
        AutoLevel(0.7, 0.0001),
        transforms.CenterCrop(size=original_size),
        transforms.Resize(resize),
        transforms.ToTensor()
    ])

def get_pretrained_model(model_path=None, pretrained=False, num_classes=2):
    print('initing model:{}'.format('resnet101'))
    model = resnet101(pretrained, num_classes=num_classes)
    if model_path is None or os.path.exists(model_path) is False:
        model_path='/home/voyager/project/chromosome-classifier/checkpoint/epoch_0079_loss_0.198197.pth'
        print('invalid model path, using:{}'.format(model_path))
    checkpoint = torch.load(model_path)
    model.load_state_dict(checkpoint['net'])
    #print(model)
    return model

def test_preprocess():
    images = read_image_list_pil()
    trans = get_transform()
    image = trans(images[0])
    image = image.reshape(448, 448)
    print(type(image), image.shape)
    plt.imshow(image, cmap='gray')
    plt.show()
    
def test_model():
    images, name_list = read_image_list_pil()
    trans = get_transform() # (1, 448, 448)
    image = trans(images[0])
    print(image.shape)
    image = image.float().unsqueeze(dim=0)
    print(image.shape)
    model = get_pretrained_model()
    output = model(image)
    print(output)
    print(output.shape)
    output_s = torch.nn.functional.softmax(output, dim=1)
    print('output after softmax:{}, image:{}'.format(output_s, name_list[0]))
    scores, results = torch.max(torch.nn.functional.softmax(output, dim=1), dim=1)
    
    print('score :{}'.format(scores))
    print('results :{}'.format(results))
  
    
def test_core():
    model_path = '/home/voyager/project/chromosome-classifier/checkpoint/epoch_0079_loss_0.198197.pth'
    core = ClassifyCore(model_path)
    image_root = '/home/voyager/project/chromosome-classifier/input'
    image_list = os.listdir(image_root)
    #print(image_list)
    image_list = [image for image in image_list if 'JPG' in image]
    images = [os.path.join(image_root, image_file) for image_file in image_list]
    for img_path in images:
        output = core.classify(img_path)
        print(output)
        print('image:{} result:{} score:{}'.format(img_path, output[1], output[0]))
    
def main():
    test_core()

main()