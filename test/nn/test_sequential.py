import torch
import torch.fx
from torch.nn import Linear, ReLU, Dropout
from torch_sparse import SparseTensor

from torch_geometric.nn import Sequential, MessagePassing
from torch_geometric.nn import GCNConv, JumpingKnowledge, global_mean_pool


def test_sequential():
    x = torch.randn(4, 16)
    edge_index = torch.tensor([[0, 0, 0, 1, 2, 3], [1, 2, 3, 0, 0, 0]])
    batch = torch.zeros(4, dtype=torch.long)

    model = Sequential('x, edge_index', [
        (GCNConv(16, 64), 'x, edge_index -> x'),
        ReLU(inplace=True),
        (GCNConv(64, 64), 'x, edge_index -> x'),
        ReLU(inplace=True),
        Linear(64, 7),
    ])
    model.reset_parameters()

    assert str(model) == (
        'Sequential(\n'
        '  (0): GCNConv(16, 64)\n'
        '  (1): ReLU(inplace=True)\n'
        '  (2): GCNConv(64, 64)\n'
        '  (3): ReLU(inplace=True)\n'
        '  (4): Linear(in_features=64, out_features=7, bias=True)\n'
        ')')

    out = model(x, edge_index)
    assert out.size() == (4, 7)

    model = Sequential('x, edge_index, batch', [
        (Dropout(p=0.5), 'x -> x'),
        (GCNConv(16, 64), 'x, edge_index -> x1'),
        ReLU(inplace=True),
        (GCNConv(64, 64), 'x1, edge_index -> x2'),
        ReLU(inplace=True),
        (lambda x1, x2: [x1, x2], 'x1, x2 -> xs'),
        (JumpingKnowledge('cat', 64, num_layers=2), 'xs -> x'),
        (global_mean_pool, 'x, batch -> x'),
        Linear(2 * 64, 7),
    ])
    model.reset_parameters()

    out = model(x, edge_index, batch)
    assert out.size() == (1, 7)


def test_sequential_jittable():
    x = torch.randn(4, 16)
    edge_index = torch.tensor([[0, 0, 0, 1, 2, 3], [1, 2, 3, 0, 0, 0]])
    adj_t = SparseTensor(row=edge_index[0], col=edge_index[1]).t()

    model = Sequential('x: Tensor, edge_index: Tensor', [
        (GCNConv(16, 64).jittable(), 'x, edge_index -> x'),
        ReLU(inplace=True),
        (GCNConv(64, 64).jittable(), 'x, edge_index -> x'),
        ReLU(inplace=True),
        Linear(64, 7),
    ])
    torch.jit.script(model)(x, edge_index)

    model = Sequential('x: Tensor, edge_index: SparseTensor', [
        (GCNConv(16, 64).jittable(), 'x, edge_index -> x'),
        ReLU(inplace=True),
        (GCNConv(64, 64).jittable(), 'x, edge_index -> x'),
        ReLU(inplace=True),
        Linear(64, 7),
    ])
    torch.jit.script(model)(x, adj_t)


def symbolic_trace(module):
    class Tracer(torch.fx.Tracer):
        def is_leaf_module(self, module, *args, **kwargs) -> bool:
            return (isinstance(module, MessagePassing)
                    or super().is_leaf_module(module, *args, **kwargs))

    return torch.fx.GraphModule(module, Tracer().trace(module))


def test_sequential_tracable():
    model = Sequential('x, edge_index', [
        (GCNConv(16, 64), 'x, edge_index -> x1'),
        ReLU(inplace=True),
        (GCNConv(64, 64), 'x1, edge_index -> x2'),
        ReLU(inplace=True),
        (lambda x1, x2: x1 + x2, 'x1, x2 -> x'),
        Linear(64, 7),
    ])
    symbolic_trace(model)
