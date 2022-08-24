# Experimental Notes
## RIDE
### CIFAR100-LT
* 1
	* accuracy 48.16%
### CIFAR10-LT
* 1
	* accuracy 81.10%
## ResNet18
### CIFAR100-LT
* 1 & 2
	* CELoss 2 runs
	* accuray 39.91%
* 3
	* LDAMLoss
	* accuracy 42%
### CIFAR10-LT
* 1
	* LDAMLoss
	* accuracy 76.47%

## ResNet18-MoE
### CIFAR100-LT
* 0815_130523
	* num_expert 	8
	* moe_top_k 	2
	* CELoss
	* accuray 39.83%
* 2
	* num_expert 	64
	* moe_top_k 	16
	* CELoss
	* accuracy 40.94%
* 3
	* num_expert 	128
	* moe_top_k   	32
	* CELoss
	* accuracy 39.09%
* 4
	* num_expert 	128
	* moe_top_k 	64
	* LDAMLoss
	* accuracy 41.19%
* 5
	* num_expert 128
	* moe_top_k 8
	* LDAMLoss 43.18%
* 
### CIFAR10-LT
* 1
	* num_expert 8
	* moe_top_k 2
	* LDAMLoss
	* accuary 77.29%

## ResNet32-MoE
### CIFAR100-LT
* 1
	*       "num_expert": 8,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [1, 1, 1, 0],
            "basic_block_moe_idx": [0, 1, 1, 1, 1],
            "reduce_dimension": true,
	        "use_norm": true
	* accuracy 35.95%
* 2
	*       "num_expert": 128,
	        "moe_top_k": 16,
            "num_classes": 100,
            "layer_moe_idx": [1, 1, 1, 0],
            "basic_block_moe_idx": [0, 1, 1, 1, 1],
            "reduce_dimension": true,
	        "use_norm": true
	* accuracy 34.82%
* 3 out.txt
	*       "num_expert": 128,
	        "moe_top_k": 16,
            "num_classes": 100,
            "layer_moe_idx": [1, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": true,
	        "use_norm": true
* 4 out1.txt
	*       "num_expert": 128,
	        "moe_top_k": 16,
            "num_classes": 100,
            "layer_moe_idx": [1, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": true
* 5 out2.txt
	*       "num_expert": 128,
	        "moe_top_k": 16,
            "num_classes": 100,
            "layer_moe_idx": [1, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
* 6
	*       "num_expert": 32,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [1, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 37.25%
* 7
	*       "num_expert": 32,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.26%
* 8
### CIFAR10-LT
* 1
	*      "num_expert": 8,
	        "moe_top_k": 2,
            "num_classes": 10,
            "layer_moe_idx": [1, 1, 1, 0],
            "basic_block_moe_idx": [0, 1, 1, 1, 1],
            "reduce_dimension": true,
	        "use_norm": true
	* accuracy 72.90%
* 2
	*       "num_expert": 32,
	        "moe_top_k": 8,
            "num_classes": 10,
            "layer_moe_idx": [1, 1, 1, 0],
            "basic_block_moe_idx": [0, 1, 1, 1, 1],
            "reduce_dimension": true,
	        "use_norm": true
	* accuracy 72.99%
## Try to Do
- [ ] Add a meta json file describing all runs in the same arch for convenience
- [x] add `logits`