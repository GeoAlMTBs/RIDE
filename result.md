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
## Try to Do
* Add a meta json file describing all runs in the same arch for convenience
