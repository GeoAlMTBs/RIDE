import torch.nn as nn
import torch.nn.functional as F
from base import BaseModel
from .fb_resnets import ResNet
from .fb_resnets import ResNeXt
from .fb_resnets import RIDEResNet
from .fb_resnets import RIDEResNeXt
from .fb_resnets import EAResNet
from .fb_resnets import EAResNeXt
from .ldam_drw_resnets import resnet_cifar
from .ldam_drw_resnets import ride_resnet_cifar
from .ldam_drw_resnets import ea_resnet_cifar

import os
import sys
basedir = os.getenv('basedir')
sys.path.append(basedir + 'fastmoe/examples/resnet')

from resnet import ResNet18MoE

# ?

class Model(BaseModel):
    requires_target = False

    def __init__(self, num_classes, backbone_class=None):
        super().__init__()
        if backbone_class is not None: # Do not init backbone here if None
            self.backbone = backbone_class(num_classes)

    def _hook_before_iter(self):
        self.backbone._hook_before_iter()

    def forward(self, x, mode=None):
        x = self.backbone(x)

        assert mode is None
        return x

class EAModel(BaseModel):
    # ? What's EA model? evaluation?
    requires_target = True
    confidence_model = True
    # ?
    def __init__(self, num_classes, backbone_class=None):
        super().__init__()
        if backbone_class is not None: # Do not init backbone here if None
            self.backbone = backbone_class(num_classes)

    def _hook_before_iter(self):
        self.backbone._hook_before_iter()

    def forward(self, x, mode=None, target=None):
        x = self.backbone(x, target=target)
    # ? backbone, this sort of thing

        assert isinstance(x, tuple) # logits, extra_info
        assert mode is None
        
        return x

class ResNet18MoEModel(Model):
    def __init__(self, num_classes, use_conv_moe, num_expert, moe_top_k):
        super().__init__(num_classes, None)
        # print('in resnet18moemodel: ', use_conv_moe)
        self.backbone = ResNet18MoE(num_classes, use_conv_moe, num_expert, moe_top_k)

class ResNet18MoEModelTemplate(Model):
    def __init__(
        self,
        num_expert,
        moe_top_k,
        num_classes,
        layer_moe_idx,
        basic_block_moe_idx,
        reduce_dimension=False,
        layer2_output_dim=None,
        layer3_output_dim=None,
        layer4_output_dim=None,
        use_norm=False,
        **kwargs
        ):
        super().__init__(num_classes, None)
        self.log_selected_experts = False
        self.num_classes = num_classes
        self.num_expert = num_expert
        self.top_k = moe_top_k
        self.backbone = resnet_cifar.ResNet_MoE(
            resnet_cifar.BasicBlock,
            resnet_cifar.CustomizedMoEBasicBlock,
            [2, 2, 2, 2],
            num_expert,
            moe_top_k,
            num_classes=num_classes,
            layer_moe_idx=layer_moe_idx,
            basic_block_moe_idx=basic_block_moe_idx,
            reduce_dimension=reduce_dimension,
            layer2_output_dim=layer2_output_dim,
            layer3_output_dim=layer3_output_dim,
            layer4_output_dim=layer4_output_dim,
            use_norm=use_norm,
            **kwargs
        )

    def enable_logging_experts(self):
        self.log_selected_experts = True
        self.backbone.sequential[4].sequential[1].enable_logging_experts()
        self.backbone.sequential[5].sequential[1].enable_logging_experts()

    def disable_logging_experts(self):
        self.log_selected_experts = False
        self.backbone.sequential[4].sequential[1].disable_logging_experts()
        self.backbone.sequential[5].sequential[1].disable_logging_experts()

class ResNet18MoEModelLayerLevel(Model):
    def __init__(
        self,
        num_expert,
        moe_top_k,
        num_classes,
        layer_moe_idx,
        reduce_dimension=False,
        layer2_output_dim=None,
        layer3_output_dim=None,
        layer4_output_dim=None,
        use_norm=False,
        **kwargs
        ):
        super().__init__(num_classes, None)
        self.log_selected_experts = False
        self.num_classes = num_classes
        self.num_expert = num_expert
        self.top_k = moe_top_k
        self.backbone = resnet_cifar.ResNetMoELayerLevel(
            resnet_cifar.BasicBlock,
            [2, 2, 2, 2],
            num_expert,
            moe_top_k,
            num_classes=num_classes,
            layer_moe_idx=layer_moe_idx,
            reduce_dimension=reduce_dimension,
            layer2_output_dim=layer2_output_dim,
            layer3_output_dim=layer3_output_dim,
            layer4_output_dim=layer4_output_dim,
            use_norm=use_norm,
            **kwargs
        )

    def enable_logging_experts(self):
        self.log_selected_experts = True
        self.backbone.sequential[4].enable_logging_experts()
        self.backbone.sequential[5].enable_logging_experts()

    def disable_logging_experts(self):
        self.log_selected_experts = False
        self.backbone.sequential[4].disable_logging_experts()
        self.backbone.sequential[5].disable_logging_experts()

class ResNet20MoEModel(Model):
    def __init__(
        self,
        num_expert,
        moe_top_k,
        num_classes,
        layer_moe_idx,
        basic_block_moe_idx,
        reduce_dimension=False,
        layer2_output_dim=None,
        layer3_output_dim=None,
        use_norm=False,
        **kwargs
        ):
        super().__init__(num_classes, None)
        self.log_selected_experts = False
        self.num_classes = num_classes
        self.num_expert = num_expert
        self.top_k = moe_top_k
        self.backbone = resnet_cifar.ResNet_s_MoE(
            resnet_cifar.BasicBlock,
            resnet_cifar.CustomizedMoEBasicBlock,
            [3, 3, 3],
            num_expert,
            moe_top_k,
            num_classes=num_classes,
            layer_moe_idx=layer_moe_idx,
            basic_block_moe_idx=basic_block_moe_idx,
            reduce_dimension=reduce_dimension,
            layer2_output_dim=layer2_output_dim,
            layer3_output_dim=layer3_output_dim,
            use_norm=use_norm,
            **kwargs
        )

    def enable_logging_experts(self):
        self.log_selected_experts = True
        self.backbone.sequential[4].sequential[1].enable_logging_experts()
        self.backbone.sequential[4].sequential[2].enable_logging_experts()

    def disable_logging_experts(self):
        self.log_selected_experts = False
        self.backbone.sequential[4].sequential[1].disable_logging_experts()
        self.backbone.sequential[4].sequential[2].disable_logging_experts()

class ResNet32MoEModel(Model):
    def __init__(
        self,
        num_expert,
        moe_top_k,
        num_classes,
        layer_moe_idx,
        basic_block_moe_idx,
        reduce_dimension=False,
        layer2_output_dim=None,
        layer3_output_dim=None,
        use_norm=False,
        **kwargs
        ):
        super().__init__(num_classes, None)
        self.log_selected_experts = False
        self.num_classes = num_classes
        self.num_expert = num_expert
        self.top_k = moe_top_k
        self.backbone = resnet_cifar.ResNet_s_MoE(
            resnet_cifar.BasicBlock,
            resnet_cifar.CustomizedMoEBasicBlock,
            [5, 5, 5],
            num_expert,
            moe_top_k,
            num_classes=num_classes,
            layer_moe_idx=layer_moe_idx,
            basic_block_moe_idx=basic_block_moe_idx,
            reduce_dimension=reduce_dimension,
            layer2_output_dim=layer2_output_dim,
            layer3_output_dim=layer3_output_dim,
            use_norm=use_norm,
            **kwargs
        )

    def enable_logging_experts(self):
        self.log_selected_experts = True
        self.backbone.sequential[4].sequential[3].enable_logging_experts()
        self.backbone.sequential[4].sequential[4].enable_logging_experts()

    def disable_logging_experts(self):
        self.log_selected_experts = False
        self.backbone.sequential[4].sequential[3].disable_logging_experts()
        self.backbone.sequential[4].sequential[4].disable_logging_experts()

class ResNet10Model(Model):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, use_norm=False, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        if num_experts == 1:
            self.backbone = ResNet.ResNet(ResNet.BasicBlock, [1, 1, 1, 1], dropout=None, num_classes=num_classes, use_norm=use_norm, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, **kwargs)
        else:
            self.backbone = RIDEResNet.ResNet(ResNet.BasicBlock, [1, 1, 1, 1], dropout=None, num_classes=num_classes, use_norm=use_norm, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, num_experts=num_experts, **kwargs)

class ResNet10EAModel(EAModel):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        self.backbone = EAResNet.ResNet(EAResNet.BasicBlock, [1, 1, 1, 1], dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, num_experts=num_experts, **kwargs)

class ResNet32Model(Model): # From LDAM_DRW
    def __init__(self, num_classes, reduce_dimension=False, layer2_output_dim=None, layer3_output_dim=None, use_norm=False, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        if num_experts == 1:
            self.backbone = resnet_cifar.ResNet_s(resnet_cifar.BasicBlock, [5, 5, 5], num_classes=num_classes, reduce_dimension=reduce_dimension, layer2_output_dim=layer2_output_dim, layer3_output_dim=layer3_output_dim, use_norm=use_norm, **kwargs)
        else:
            self.backbone = ride_resnet_cifar.ResNet_s(ride_resnet_cifar.BasicBlock, [5, 5, 5], num_classes=num_classes, reduce_dimension=reduce_dimension, layer2_output_dim=layer2_output_dim, layer3_output_dim=layer3_output_dim, use_norm=use_norm, num_experts=num_experts, **kwargs)

class ResNet32EAModel(EAModel): # From LDAM_DRW
    def __init__(self, num_classes, reduce_dimension=False, layer2_output_dim=None, layer3_output_dim=None, num_experts=2, **kwargs):
        super().__init__(num_classes, None)
        self.backbone = ea_resnet_cifar.ResNet_s(ea_resnet_cifar.BasicBlock, [5, 5, 5], num_classes=num_classes, reduce_dimension=reduce_dimension, layer2_output_dim=layer2_output_dim, layer3_output_dim=layer3_output_dim, num_experts=num_experts, **kwargs)

class ResNet50Model(Model):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, use_norm=False, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        if num_experts == 1:
            self.backbone = ResNet.ResNet(ResNet.Bottleneck, [3, 4, 6, 3], dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, use_norm=use_norm, **kwargs)
        else:
            self.backbone = RIDEResNet.ResNet(RIDEResNet.Bottleneck, [3, 4, 6, 3], dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, use_norm=use_norm, num_experts=num_experts, **kwargs)

class ResNet50EAModel(EAModel):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        assert num_experts != 1
        self.backbone = EAResNet.ResNet(EAResNet.Bottleneck, [3, 4, 6, 3], dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, num_experts=num_experts, **kwargs)

class ResNeXt50EAModel(EAModel):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        assert num_experts != 1
        self.backbone = EAResNeXt.ResNext(EAResNeXt.Bottleneck, [3, 4, 6, 3], groups=32, width_per_group=4, dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, num_experts=num_experts, **kwargs)

class ResNeXt50Model(Model):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        if num_experts == 1:
            self.backbone = ResNeXt.ResNext(ResNeXt.Bottleneck, [3, 4, 6, 3], groups=32, width_per_group=4, dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, **kwargs)
        else:
            self.backbone = RIDEResNeXt.ResNext(RIDEResNeXt.Bottleneck, [3, 4, 6, 3], groups=32, width_per_group=4, dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, num_experts=num_experts, **kwargs)

class ResNet101Model(Model):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, use_norm=False, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        if num_experts == 1:
            self.backbone = ResNet.ResNet(ResNet.Bottleneck, [3, 4, 23, 3], dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, use_norm=use_norm, **kwargs)
        else:
            self.backbone = RIDEResNet.ResNet(RIDEResNet.Bottleneck, [3, 4, 23, 3], dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, use_norm=use_norm, num_experts=num_experts, **kwargs)

class ResNet152Model(Model):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, use_norm=False, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        if num_experts == 1:
            self.backbone = ResNet.ResNet(ResNet.Bottleneck, [3, 8, 36, 3], dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, use_norm=use_norm, **kwargs)
        else:
            self.backbone = RIDEResNet.ResNet(RIDEResNet.Bottleneck, [3, 8, 36, 3], dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, use_norm=use_norm, num_experts=num_experts, **kwargs)

class ResNet152EAModel(EAModel):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, num_experts=1, **kwargs):
        super().__init__(num_classes, None)
        assert num_experts != 1
        self.backbone = EAResNet.ResNet(EAResNet.Bottleneck, [3, 8, 36, 3], dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, num_experts=num_experts, **kwargs)

class ResNeXt152Model(Model):
    def __init__(self, num_classes, reduce_dimension=False, layer3_output_dim=None, layer4_output_dim=None, num_experts=1):
        super().__init__(num_classes, None)
        if num_experts == 1:
            self.backbone = ResNeXt.ResNext(ResNeXt.Bottleneck, [3, 8, 36, 3], groups=32, width_per_group=4, dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim)
        else:
            self.backbone = RIDEResNeXt.ResNext(RIDEResNeXt.Bottleneck, [3, 8, 36, 3], groups=32, width_per_group=4, dropout=None, num_classes=num_classes, reduce_dimension=reduce_dimension, layer3_output_dim=layer3_output_dim, layer4_output_dim=layer4_output_dim, num_experts=num_experts)
