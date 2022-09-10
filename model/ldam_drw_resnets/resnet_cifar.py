# From https://github.com/kaidic/LDAM-DRW/blob/master/models/resnet_cifar.py
'''
Properly implemented ResNet for CIFAR10 as described in paper [1].
The implementation and structure of this file is hugely influenced by [2]
which is implemented for ImageNet and doesn't have option A for identity.
Moreover, most of the implementations on the web is copy-paste from
torchvision's resnet and has wrong number of params.
Proper ResNet-s for CIFAR10 (for fair comparision and etc.) has following
number of layers and parameters:
name      | layers | params
ResNet20  |    20  | 0.27M
ResNet32  |    32  | 0.46M
ResNet44  |    44  | 0.66M
ResNet56  |    56  | 0.85M
ResNet110 |   110  |  1.7M
ResNet1202|  1202  | 19.4m
which this implementation indeed has.
Reference:
[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
    Deep Residual Learning for Image Recognition. arXiv:1512.03385
[2] https://github.com/pytorch/vision/blob/master/torchvision/models/resnet.py
If you use this implementation in you work, please don't forget to mention the
author, Yerlan Idelbayev.
'''
from math import prod
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init
from torch.nn import Parameter

import os
import sys
basedir = os.getenv('basedir')
sys.path.append(basedir + 'fastmoe/examples/resnet')

import logging

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logger.addHandler(c_handler)

__all__ = ['ResNet_s', 'resnet20', 'resnet32', 'resnet44', 'resnet56', 'resnet110', 'resnet1202']

def _weights_init(m):
    classname = m.__class__.__name__
    if isinstance(m, nn.Linear) or isinstance(m, nn.Conv2d):
        init.kaiming_normal_(m.weight)

class NormedLinear(nn.Module):

    def __init__(self, in_features, out_features):
        super(NormedLinear, self).__init__()
        self.weight = Parameter(torch.Tensor(in_features, out_features))
        self.weight.data.uniform_(-1, 1).renorm_(2, 1, 1e-5).mul_(1e5)

    def forward(self, x):
        out = F.normalize(x, dim=1).mm(F.normalize(self.weight, dim=0))
        return out

class LambdaLayer(nn.Module):

    def __init__(self, lambd):
        super(LambdaLayer, self).__init__()
        self.lambd = lambd

    def forward(self, x):
        return self.lambd(x)

class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1, option='A'):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != planes:
            if option == 'A':
                """
                For CIFAR10 ResNet paper uses option A.
                """
                self.planes = planes
                self.in_planes = in_planes
                # self.shortcut = LambdaLayer(lambda x: F.pad(x[:, :, ::2, ::2], (0, 0, 0, 0, planes // 4, planes // 4), "constant", 0))
                self.shortcut = LambdaLayer(lambda x:
                                            F.pad(x[:, :, ::2, ::2], (0, 0, 0, 0, (planes - in_planes) // 2, (planes - in_planes) // 2), "constant", 0))
            # ?

            elif option == 'B':
                self.shortcut = nn.Sequential(
                     nn.Conv2d(in_planes, self.expansion * planes, kernel_size=1, stride=stride, bias=False),
                     nn.BatchNorm2d(self.expansion * planes)
                )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out

sys.path.append(basedir + 'fastmoe/fmoe')
from resnetff import FMoEResNetFF
from resnetconv import FMoEResNetConv

class CustomizedMoEBasicBlock(FMoEResNetConv):
    """The Residual block of ResNet."""
    def __init__(
        self,
        input_channels,
        num_channels,
        d_model,
        moe_num_expert=8,
        moe_top_k=2,
        # use_1x1conv=False,
        strides=1,
        option='A'
    ):

        # FMoEResNetConv only takes care of one convolutional layer
        super().__init__(
            num_expert=moe_num_expert,
            num_channels=num_channels,
            d_model=d_model,
            top_k=moe_top_k
            )

        self.conv1 = nn.Conv2d(
            input_channels,
            num_channels,
            kernel_size=3,
            padding=1,
            stride=strides
            )

        self.shortcut = nn.Sequential()
        if strides != 1 or input_channels != num_channels:
            if option == 'A':
                """
                For CIFAR10 ResNet paper uses option A.
                """
                self.planes = num_channels
                self.in_planes = input_channels
                # self.shortcut = LambdaLayer(lambda x: F.pad(x[:, :, ::2, ::2], (0, 0, 0, 0, num_channels // 4, num_channels // 4), "constant", 0))
                self.shortcut = LambdaLayer(
                    lambda x: F.pad(
                        x[:, :, ::2, ::2],
                        (0, 0, 0, 0, (num_channels - input_channels) // 2, (num_channels - input_channels) // 2),
                        "constant",
                        0
                        )
                    )
            # ?

            elif option == 'B':
                self.shortcut = nn.Sequential(
                    nn.Conv2d(
                        input_channels,
                        self.expansion * num_channels,
                        kernel_size=1,
                        stride=strides,
                        bias=False
                        ),
                    nn.BatchNorm2d(self.expansion * num_channels)
                    )
        # if use_1x1conv:
        #     self.conv3 = nn.Conv2d(
        #         input_channels,
        #         num_channels,
        #         kernel_size=1,
        #         stride=strides)
        # else:
        #     self.conv3 = None

        self.bn1 = nn.BatchNorm2d(num_channels)
        self.bn2 = nn.BatchNorm2d(num_channels)

        # self.bn3 = nn.BatchNorm2d(num_channels)

    def forward(self, X):
        Y = F.relu(self.bn1(self.conv1(X)))
        Y = self.bn2(super().forward(Y))
        # if self.conv3:
        #     X = self.bn3(self.conv3(X))
        Y += self.shortcut(X)
        Y = F.relu(Y)
        return Y

class ResNet_s(nn.Module):

    def __init__(self, block, num_blocks, num_classes=10, reduce_dimension=False, layer2_output_dim=None, layer3_output_dim=None, use_norm=False, s=30):
        super(ResNet_s, self).__init__()
        self.in_planes = 16

        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(16)
        self.layer1 = self._make_layer(block, 16, num_blocks[0], stride=1)

        if layer2_output_dim is None:
            if reduce_dimension:
                layer2_output_dim = 24
            else:
                layer2_output_dim = 32

        if layer3_output_dim is None:
            if reduce_dimension:
                layer3_output_dim = 48
            else:
                layer3_output_dim = 64

        self.layer2 = self._make_layer(block, layer2_output_dim, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, layer3_output_dim, num_blocks[2], stride=2)

        if use_norm:
            self.linear = NormedLinear(layer3_output_dim, num_classes)
        else:
            s = 1
            self.linear = nn.Linear(layer3_output_dim, num_classes)
        
        self.s = s

        self.apply(_weights_init)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion

        return nn.Sequential(*layers)

    def _hook_before_iter(self):
        assert self.training, "_hook_before_iter should be called at training time only, after train() is called"
        count = 0
        for module in self.modules():
            if isinstance(module, nn.BatchNorm2d):
                if module.weight.requires_grad == False:
                    module.eval()
                    count += 1

        if count > 0:
            print("Warning: detected at least one frozen BN, set them to eval state. Count:", count)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        self.feat_before_GAP = out
        out = F.avg_pool2d(out, out.size()[3])
        out = out.view(out.size(0), -1)
        self.feat = out
        
        out = self.linear(out)
        out = out * self.s # This hyperparam s is originally in the loss function, but we moved it here to prevent using s multiple times in distillation.
        return out

class ResNet_s_MoE(nn.Module):

    def __init__(
        self,
        block,
        moe_block,
        num_blocks,
        num_expert,
        moe_top_k,
        num_classes=10,
        layer_moe_idx=[True, True, True, False],
        basic_block_moe_idx=[False, True, True, True, True],
        reduce_dimension=False,
        layer2_output_dim=None,
        layer3_output_dim=None,
        use_norm=False,
        s=30,
        hw=[32, 32]
        ):
        super(ResNet_s_MoE, self).__init__()
        self.in_planes = 16
        self.h, self.w = hw

        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1, bias=False)
        # (32, 32)
        self.bn1 = nn.BatchNorm2d(16)
        if layer_moe_idx[0] == True:
            self.layer1 = self._make_layer_moe(
                block,
                moe_block,
                16,
                num_blocks[0],
                1,
                basic_block_moe_idx,
                (self.h, self.w),
                num_expert,
                moe_top_k
                )
        else:
            self.layer1 = self._make_layer(block, 16, num_blocks[0], stride=1)
        # (32, 32)

        if layer2_output_dim is None:
            if reduce_dimension:
                layer2_output_dim = 24
            else:
                layer2_output_dim = 32

        if layer3_output_dim is None:
            if reduce_dimension:
                layer3_output_dim = 48
            else:
                layer3_output_dim = 64

        if layer_moe_idx[1] == True:
            self.layer2 = self._make_layer_moe(
                block,
                moe_block,
                layer2_output_dim,
                num_blocks[1],
                2,
                basic_block_moe_idx,
                (self.h, self.w),
                num_expert,
                moe_top_k
                )
        else:
            self.layer2 = self._make_layer(block, layer2_output_dim, num_blocks[1], stride=2)

        self.h = int(self.h / 2)
        self.w = int(self.w / 2)

        logger.debug(f'(self.h, self.w) ({self.h}, {self.w})')

        if layer_moe_idx[2] == True:
            self.layer3 = self._make_layer_moe(
                block,
                moe_block,
                layer3_output_dim,
                num_blocks[2],
                2,
                basic_block_moe_idx,
                (self.h, self.w),
                num_expert,
                moe_top_k
            )
        else:
            self.layer3 = self._make_layer(block, layer3_output_dim, num_blocks[2], stride=2)

        self.h = int(self.h / 2)
        self.w = int(self.w / 2)
        # ? Strange huh. float h, w will cause the TypeError: new(): argument 'size' must be tuple of ints, but found element of type float at pos 2 error

        if use_norm:
            self.linear = NormedLinear(layer3_output_dim, num_classes)
        else:
            s = 1
            self.linear = nn.Linear(layer3_output_dim, num_classes)
        
        self.s = s

        self.apply(_weights_init)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion

        return nn.Sequential(*layers)

    def _make_layer_moe(self, block, moe_block, planes, num_blocks, stride, basic_block_moe_idx, hw, num_expert, moe_top_k):
        h, w = hw
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for idx, stride in enumerate(strides):
            if basic_block_moe_idx[idx] == True and stride == 1:
                # logger.info(f'planes {planes}')
                # logger.debug(f'hw {hw}')
                # logger.debug(f'prod(hw) {prod(hw)}')
                # print(hw)
                # ? Where is the logger saved?

                layers.append(
                    moe_block(
                        self.in_planes,
                        planes,
                        int(planes * h * w), # d_model
                        moe_num_expert=num_expert,
                        moe_top_k=moe_top_k,
                        strides=1,
                        option='A'
                    )
                )
            else:
                layers.append(block(self.in_planes, planes, stride))
            
            if stride == 2:
                h = int(h / 2)
                w = int(w / 2)

            self.in_planes = planes * block.expansion

        return nn.Sequential(*layers)

    def _hook_before_iter(self):
        assert self.training, "_hook_before_iter should be called at training time only, after train() is called"
        count = 0
        for module in self.modules():
            if isinstance(module, nn.BatchNorm2d):
                if module.weight.requires_grad == False:
                    module.eval()
                    count += 1

        if count > 0:
            print("Warning: detected at least one frozen BN, set them to eval state. Count:", count)
    # ? What does this function do?

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        self.feat_before_GAP = out
        out = F.avg_pool2d(out, out.size()[3])
        out = out.view(out.size(0), -1)
        self.feat = out

        out = self.linear(out)

        self.logits = out

        out = out * self.s # This hyperparam s is originally in the loss function, but we moved it here to prevent using s multiple times in distillation.
        # ?
        return out


def resnet20():
    return ResNet_s(BasicBlock, [3, 3, 3])


def resnet32(num_classes=10, use_norm=False):
    return ResNet_s(BasicBlock, [5, 5, 5], num_classes=num_classes, use_norm=use_norm)


def resnet44():
    return ResNet_s(BasicBlock, [7, 7, 7])


def resnet56():
    return ResNet_s(BasicBlock, [9, 9, 9])


def resnet110():
    return ResNet_s(BasicBlock, [18, 18, 18])


def resnet1202():
    return ResNet_s(BasicBlock, [200, 200, 200])


def test(net):
    import numpy as np
    total_params = 0

    for x in filter(lambda p: p.requires_grad, net.parameters()):
        total_params += np.prod(x.data.numpy().shape)
    print("Total number of params", total_params)
    print("Total layers", len(list(filter(lambda p: p.requires_grad and len(p.data.size())>1, net.parameters()))))


if __name__ == "__main__":
    for net_name in __all__:
        if net_name.startswith('resnet'):
            print(net_name)
            test(globals()[net_name]())
            print()