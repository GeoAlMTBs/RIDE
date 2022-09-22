import torch

def accuracy(output, target, return_length=False):
    with torch.no_grad():
        pred = torch.argmax(output, dim=1)
        assert pred.shape[0] == len(target)
        correct = 0
        correct += torch.sum(pred == target).item()
    if return_length:
        return correct / len(target), len(target)
    else:
        return correct / len(target)
    
def top_k_acc(output, target, k=5, return_length=False):
    with torch.no_grad():
        pred = torch.topk(output, k, dim=1)[1]
        assert pred.shape[0] == len(target)
        correct = 0
        for i in range(k):
            correct += torch.sum(pred[:, i] == target).item()
    if return_length:
        return correct / len(target), len(target)
    else:
        return correct / len(target)

def head_acc(output, target, return_length=False):
    num_cls = 100
    with torch.no_grad():
        pred = torch.argmax(output, dim=1)
        assert pred.shape[0] == len(target)
        selec_idx = torch.lt(target, num_cls // 3)
        length = torch.sum(selec_idx).item()
        new_target = torch.masked_select(target, selec_idx)
        new_pred = torch.masked_select(pre, selec_idx)
        correct = 0
        correct += torch.sum(new_pred == new_target).item()
    if return_length:
        return correct / length, length
    else:
        return correct / length

def middle_acc(output, target, return_length=False):
    num_cls = 100
    with torch.no_grad():
        pred = torch.argmax(output, dim=1)
        assert pred.shape[0] == len(target)
        selec_idx = torch.lt(target, 2 * num_cls // 3) * torch.ge(target, num_cls // 3)
        length = torch.sum(selec_idx).item()
        new_target = torch.masked_select(target, selec_idx)
        new_pred = torch.masked_select(pre, selec_idx)
        correct = 0
        correct += torch.sum(new_pred == new_target).item()
    if return_length:
        return correct / length, length
    else:
        return correct / length

def tail_acc(output, target, return_length=False):
    num_cls = 100
    with torch.no_grad():
        pred = torch.argmax(output, dim=1)
        assert pred.shape[0] == len(target)
        selec_idx = torch.ge(target, 2 * num_cls // 3)
        length = torch.sum(selec_idx).item()
        new_target = torch.masked_select(target, selec_idx)
        new_pred = torch.masked_select(pre, selec_idx)
        correct = 0
        correct += torch.sum(new_pred == new_target).item()
    if return_length:
        return correct / length, length
    else:
        return correct / length