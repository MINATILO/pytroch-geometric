from .basic_gnn import GCN, GraphSAGE, GIN, GAT
from .jumping_knowledge import JumpingKnowledge
from .node2vec import Node2Vec
from .deep_graph_infomax import DeepGraphInfomax
from .autoencoder import InnerProductDecoder, GAE, VGAE, ARGA, ARGVA
from .signed_gcn import SignedGCN
from .re_net import RENet
from .graph_unet import GraphUNet
from .schnet import SchNet
from .dimenet import DimeNet
from .gnn_explainer import GNNExplainer
from .metapath2vec import MetaPath2Vec
from .deepgcn import DeepGCNLayer
from .tgn import TGNMemory
from .label_prop import LabelPropagation
from .correct_and_smooth import CorrectAndSmooth
from .attentive_fp import AttentiveFP

__all__ = [
    'GCN',
    'GraphSAGE',
    'GIN',
    'GAT',
    'JumpingKnowledge',
    'Node2Vec',
    'DeepGraphInfomax',
    'InnerProductDecoder',
    'GAE',
    'VGAE',
    'ARGA',
    'ARGVA',
    'SignedGCN',
    'RENet',
    'GraphUNet',
    'SchNet',
    'DimeNet',
    'GNNExplainer',
    'MetaPath2Vec',
    'DeepGCNLayer',
    'TGNMemory',
    'LabelPropagation',
    'CorrectAndSmooth',
    'AttentiveFP',
]

classes = __all__
