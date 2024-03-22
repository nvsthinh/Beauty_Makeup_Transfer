import numpy as np
import base64
import io
import json


import os, glob, cv2
import random
import dlib

from torch.utils.data import Dataset
from PIL import Image

import torch
import torch.nn.init as init
from torch.autograd import Variable
from torchvision.utils import save_image
import torch.nn as nn
import torchvision.transforms as T

import time
import datetime

from tqdm import tqdm as tqdm

import torchvision.models as models

from torchvision import transforms
from torch.utils.data import DataLoader
import torch
import PIL
from PIL import Image

from torch.backends import cudnn

'''--------------------------- Dataset ---------------------------'''
class MAKEUP(Dataset):
    def __init__(self, makeup_path, non_makeup_path, transform, mode, transform_mask, cls_list, landmarks_checkpoint_path):
        self.transform = transform
        self.mode = mode
        self.transform_mask = transform_mask
        self.landmarks_checkpoint_path = landmarks_checkpoint_path

        self.As = [non_makeup_path]
        self.Bs = [makeup_path]

        self.noiA = len(self.As)
        self.noiB = len(self.Bs)

        print(f"Number of Non Makeup Images: {self.noiA}, Makeup Images: {self.noiB}")

    def __getitem__(self, index):
        idxA = random.choice(range(self.noiA))
        idxB = random.choice(range(self.noiB))

        image_A = self.align_faces(self.As[idxA])
        image_B = Image.open(self.Bs[idxB]).convert("RGB")

        image_A = Image.fromarray(cv2.resize(np.array(image_A), (256, 256)))
        image_B = Image.fromarray(cv2.resize(np.array(image_B), (256, 256)))
        return self.transform(image_A), self.transform(image_B)

    def __len__(self):
            num_A = len(self.As)
            num_B = len(self.Bs)
            return num_A * num_B

    def __len__(self):
            num_A = len(self.As)
            num_B = len(self.Bs)
            return num_A * num_B

    def align_faces(self, image_path):
      # Read Image
      img = dlib.load_rgb_image(image_path)

      # Face Detection
      detector = dlib.get_frontal_face_detector()

      # Landmark Detection
      sp = dlib.shape_predictor(self.landmarks_checkpoint_path)
      dets = detector(img, 1)
      objs = dlib.full_object_detections()

      for detection in dets:
          s = sp(img, detection)
          objs.append(s)

      faces = dlib.get_face_chips(img, objs, size=256, padding=0.35)

      return faces[0]

'''--------------------------- Data Loader ---------------------------'''

def ToTensor(pic):
    # handle PIL Image
    if pic.mode == 'I':
        img = torch.from_numpy(np.array(pic, np.int32, copy=False))
    elif pic.mode == 'I;16':
        img = torch.from_numpy(np.array(pic, np.int16, copy=False))
    else:
        img = torch.ByteTensor(torch.ByteStorage.from_buffer(pic.tobytes()))
    # PIL image mode: 1, L, P, I, F, RGB, YCbCr, RGBA, CMYK
    if pic.mode == 'YCbCr':
        nchannel = 3
    elif pic.mode == 'I;16':
        nchannel = 1
    else:
        nchannel = len(pic.mode)
    img = img.view(pic.size[1], pic.size[0], nchannel)
    # put it from HWC to CHW format
    # yikes, this transpose takes 80% of the loading time/CPU
    img = img.transpose(0, 1).transpose(0, 2).contiguous()
    if isinstance(img, torch.ByteTensor):
        return img.float()
    else:
        return img

def get_loader(origin_img_path, style_img_path, landmarks_checkpoint_path):
    # return the DataLoader
    dataset_name = 'MAKEUP'
    makeup_path = style_img_path
    non_makeup_path = origin_img_path
    transform = transforms.Compose([
    transforms.Resize(256),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])])
    transform_mask = transforms.Compose([
        transforms.Resize(256, interpolation=PIL.Image.NEAREST),
        ToTensor])
    print('Makeup Path: ', style_img_path)
    print('Non Makeup Path: ', origin_img_path)

    dataset_test = eval(dataset_name)(makeup_path=makeup_path, non_makeup_path=non_makeup_path, transform=transform, mode= "test",\
                                                            transform_mask =transform_mask, cls_list = ['A_OM', 'B_OM'], landmarks_checkpoint_path=landmarks_checkpoint_path)

    data_loader_test = DataLoader(dataset=dataset_test,
                             batch_size=1,
                             shuffle=False)

    return data_loader_test

"""-------------------------------- Model ------------------------"""
class ResidualBlock(nn.Module):
    """Residual Block."""
    def __init__(self, dim_in, dim_out):
        super(ResidualBlock, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(dim_in, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True),
            nn.ReLU(inplace=True),
            nn.Conv2d(dim_out, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True))

    def forward(self, x):
        return x + self.main(x)

class Generator_branch(nn.Module):
    """Generator. Encoder-Decoder Architecture."""
    # input 2 images and output 2 images as well
    def __init__(self, conv_dim=64, repeat_num=6, input_nc=3):
        super(Generator_branch, self).__init__()

        # Branch input
        layers_branch = []
        layers_branch.append(nn.Conv2d(input_nc, conv_dim, kernel_size=7, stride=1, padding=3, bias=False))
        layers_branch.append(nn.InstanceNorm2d(conv_dim, affine=True))
        layers_branch.append(nn.ReLU(inplace=True))
        layers_branch.append(nn.Conv2d(conv_dim, conv_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
        layers_branch.append(nn.InstanceNorm2d(conv_dim*2, affine=True))
        layers_branch.append(nn.ReLU(inplace=True))
        self.Branch_0 = nn.Sequential(*layers_branch)

        # Branch input
        layers_branch = []
        layers_branch.append(nn.Conv2d(input_nc, conv_dim, kernel_size=7, stride=1, padding=3, bias=False))
        layers_branch.append(nn.InstanceNorm2d(conv_dim, affine=True))
        layers_branch.append(nn.ReLU(inplace=True))
        layers_branch.append(nn.Conv2d(conv_dim, conv_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
        layers_branch.append(nn.InstanceNorm2d(conv_dim*2, affine=True))
        layers_branch.append(nn.ReLU(inplace=True))
        self.Branch_1 = nn.Sequential(*layers_branch)

        # Down-Sampling, branch merge
        layers = []
        curr_dim = conv_dim*2
        layers.append(nn.Conv2d(curr_dim*2, curr_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
        layers.append(nn.InstanceNorm2d(curr_dim*2, affine=True))
        layers.append(nn.ReLU(inplace=True))
        curr_dim = curr_dim * 2

        # Bottleneck
        for i in range(repeat_num):
            layers.append(ResidualBlock(dim_in=curr_dim, dim_out=curr_dim))

        # Up-Sampling
        for i in range(2):
            layers.append(nn.ConvTranspose2d(curr_dim, curr_dim//2, kernel_size=4, stride=2, padding=1, bias=False))
            layers.append(nn.InstanceNorm2d(curr_dim//2, affine=True))
            layers.append(nn.ReLU(inplace=True))
            curr_dim = curr_dim // 2

        self.main = nn.Sequential(*layers)

        layers_1 = []
        layers_1.append(nn.Conv2d(curr_dim, curr_dim, kernel_size=3, stride=1, padding=1, bias=False))
        layers_1.append(nn.InstanceNorm2d(curr_dim, affine=True))
        layers_1.append(nn.ReLU(inplace=True))
        layers_1.append(nn.Conv2d(curr_dim, curr_dim, kernel_size=3, stride=1, padding=1, bias=False))
        layers_1.append(nn.InstanceNorm2d(curr_dim, affine=True))
        layers_1.append(nn.ReLU(inplace=True))
        layers_1.append(nn.Conv2d(curr_dim, 3, kernel_size=7, stride=1, padding=3, bias=False))
        layers_1.append(nn.Tanh())
        self.branch_1 = nn.Sequential(*layers_1)
        layers_2 = []
        layers_2.append(nn.Conv2d(curr_dim, curr_dim, kernel_size=3, stride=1, padding=1, bias=False))
        layers_2.append(nn.InstanceNorm2d(curr_dim, affine=True))
        layers_2.append(nn.ReLU(inplace=True))
        layers_2.append(nn.Conv2d(curr_dim, curr_dim, kernel_size=3, stride=1, padding=1, bias=False))
        layers_2.append(nn.InstanceNorm2d(curr_dim, affine=True))
        layers_2.append(nn.ReLU(inplace=True))
        layers_2.append(nn.Conv2d(curr_dim, 3, kernel_size=7, stride=1, padding=3, bias=False))
        layers_2.append(nn.Tanh())
        self.branch_2 = nn.Sequential(*layers_2)

    def forward(self, x, y):
        input_x = self.Branch_0(x)
        input_y = self.Branch_1(y)
        input_fuse = torch.cat((input_x, input_y), dim=1)
        out = self.main(input_fuse)
        out_A = self.branch_1(out)
        out_B = self.branch_2(out)
        return out_A, out_B

"""-------------------------------- Solver MakeupGAN to Test ------------------------"""
class Solver_makeupGAN(object):
    def __init__(self, data_loaders, snapshot_path, test_model):
        # Data loader
        self.data_loader_test = data_loaders

        # Model hyper-parameters
        self.g_conv_dim = 64
        self.g_repeat_num = 6

        # Hyper-parameteres
        self.test_model = test_model

        # Path
        self.snapshot_path = snapshot_path

    def to_var(self, x, requires_grad=True):
        if torch.cuda.is_available():
            x = x.cuda()
        if not requires_grad:
            return Variable(x, requires_grad=requires_grad)
        else:
            return Variable(x)

    def de_norm(self, x):
        out = (x + 1) / 2
        return out.clamp(0, 1)


    def test(self):
        # Load trained parameters
        self.G = Generator_branch(self.g_conv_dim, self.g_repeat_num)
        G_path = os.path.join(self.snapshot_path, '{}_G.pth'.format(self.test_model))
        self.G.load_state_dict(torch.load(G_path, map_location=torch.device('cpu')))
        self.G.eval()
        for i, (img_A, img_B) in enumerate(self.data_loader_test):
            start = time.time()
            real_org = self.to_var(img_A)
            real_ref = self.to_var(img_B)

            image_list = []
            # Get makeup result
            fake_A, fake_B = self.G(real_org, real_ref)
            image_list.append(fake_A)
            image_list = torch.cat(image_list, dim=3)

            output_img = self.de_norm(image_list.data).squeeze()

            transform = T.ToPILImage()
            pil_img = transform(output_img)

            print(f"average time : {time.time() - start:.3f}s")

            return pil_img

"""-------------------------------- Apply BeautyGAM Filter ------------------------"""

def apply_beautygan_filter(origin_img_path, style_img_path):
    try:
        # enable cudnn
        cudnn.benchmark = True
        snapshot_path =  'D:\Project\DPL302m\AppTest\Beauty_Makeup_Transfer_Final\model'
        test_model = '400_139'
        landmarks_checkpoint_path = 'D:\Project\DPL302m\AppTest\Beauty_Makeup_Transfer_Final\model\shape_predictor_5_face_landmarks.dat'

        # get the DataLoader
        data_loaders = get_loader(origin_img_path, style_img_path, landmarks_checkpoint_path)
        #get the solver
        solver = Solver_makeupGAN(data_loaders, snapshot_path, test_model)

        pil_img = solver.test()

        # Save the PIL Image to a bytes buffer
        img_buffer = io.BytesIO()
        pil_img.save(img_buffer, format="PNG")
        img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        # print(img_str)
        # print(orig_str)
        return img_str
        # return {"orig_image": orig_str}
    except Exception as e:
        return {"Error": str(e)}