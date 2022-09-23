[TOC]
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
	* LDAMLoss 
	* accuracy **43.18%**
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
* 3
	*       "num_expert": 128,
	        "moe_top_k": 16,
            "num_classes": 100,
            "layer_moe_idx": [1, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": true,
	        "use_norm": true
	* accuracy 36.89%
* 4
	*       "num_expert": 128,
	        "moe_top_k": 16,
            "num_classes": 100,
            "layer_moe_idx": [1, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": true
	* accuracy 38.36%
	* reduce_dimension is set to false compared to run 3, which increases model performance
* 5
	*       "num_expert": 128,
	        "moe_top_k": 16,
            "num_classes": 100,
            "layer_moe_idx": [1, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 38.80%
	* use_norm is set to false compared to the previous run, which improves acc.
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
	* Compared to run 6, expert should not be placed on the first layer?
* 8
	*       "num_expert": 32,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.98% < 42.00%(ResNet18)
	* Compared to run 7, there is no need to be so many experts? 
* 9
	*       "num_expert": 32,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 1, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 38.87%
	* Compared to run 8
* 10
	*       "num_expert": 32,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 1, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.96%
	* Compare it to run7. Add a moe on basic block might increase performance?
* 11
	*       "num_expert": 32,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 1, 1, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.58%
* 12
	*       "num_expert":32,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.75%
* 13
	*       "num_expert": 32,
	        "moe_top_k": 8,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.01%
* 14
	*       "num_expert": 32,
	        "moe_top_k": 16,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.55%
* 15
	*       "num_expert": 32,
	        "moe_top_k": 32,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.72%
* 16
   *        "num_expert": 8,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.35%
* 17
	*       "num_expert": 16,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.42%
* 18
	*       "num_expert": 64,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy **41.20%**
* 19
	*       "num_expert": 32,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 38.38%
* 20
	* 	    "num_expert": 128,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.49%
* 21
	*       "num_expert": 256,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.04%
* 22
	*       "num_expert": 1024,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 1, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.19%
	* Training takes too much time :( .
* 23
	* **Given a fixed number of experts, change the number of selected experts.**
	*       "num_expert": 8,
	        "moe_top_k": 1,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.91%
* 24
	*       "num_expert": 8,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 38.51%
* 25
	*       "num_expert": 8,
	        "moe_top_k": 3,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.14%
* 26
	*       "num_expert": 8,
	        "moe_top_k": 4,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.64%
* 27
	*       "num_expert": 8,
	        "moe_top_k": 5,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.30%
* 28
	*       "num_expert": 8,
	        "moe_top_k": 6,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.46%
* 29
	*       "num_expert": 8,
	        "moe_top_k": 7,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.28%
* 30
	*       "num_expert": 8,
	        "moe_top_k": 8,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 41.10%
* 31
	* **Given moe_top_k, change num_expert**
	*       "num_expert": 2,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.59%
* 32
	*       "num_expert": 4,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.68%
* 33
	*       "num_expert": 16,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 38.28%
* 34
	*       "num_expert": 32,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 39.16%
* 35
	*       "num_expert": 64,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.11%
* 36
	*       "num_expert": 4,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.68%
* 36
	*       "num_expert": 4,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy 40.15%
* 37
	*       "num_expert": 4,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 0, 0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy **41.15%**
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
## ResNet32
### CIFAR100-LT
* 1
	* accuracy 40.27%
## ResNet20MoE
### CIFAR100-LT
* 1
	* 	    "num_expert": 8,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy
		* overall **39.98%**
		* head 67.89%
		* middle 42.15%
		* tail 10.79%
* 2
	*      "num_expert": 16,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy
		* overall 39.01%
		* head 67.91%
		* middle 41.48%
		* tail 8.56%
* 3
	*      "num_expert": 4,
	        "moe_top_k": 2,
            "num_classes": 100,
            "layer_moe_idx": [0, 0, 1, 0],
            "basic_block_moe_idx": [0, 1, 1],
            "reduce_dimension": false,
	        "use_norm": false
	* accuracy
		* overall 38.98%
		* head 66.70%
		* middle 41.52%
		* tail 9.62%
### CIFAR10-LT
## ResNet20
### CIFAR100-LT
* 1
	* accuracy 39.09%
* 2
	* accuracy 39.11%
		* head 67.85%
		* middle 42.03%
		* tail 8.38%
	* Compared to run No.1 of MoE, this model performs poorly on tail classes.
## Try to Do
- [ ] Add a meta json file describing all runs in the same arch for convenience
- [x] add `logits`
