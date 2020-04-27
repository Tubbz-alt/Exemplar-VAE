import torch
import os
import numpy as np

def importing_model(args):
    if args.model_name == 'vae':
        from models.VAE import VAE
    elif args.model_name == 'hvae_2level':
        from models.HVAE_2level import VAE
    elif args.model_name == 'convhvae_2level':
        from models.convHVAE_2level import VAE
    elif args.model_name == 'new_vae':
        from models.new_vae import VAE
    elif args.model_name == 'conv_cifar':
        from models.conv_cifar import VAE
    elif args.model_name == 'fully_hconv':
        from models.fully_hconv import VAE
    elif args.model_name == 'conv_resnet_vae':
        from models.conv_resnet_vae import VAE
    elif args.model_name == 'CelebA':
        from models.celebA import VAE
    else:
        raise Exception('Wrong name of the model!')
    return VAE


def save_model(save_path, load_path, content):
    torch.save(content, save_path)
    os.rename(save_path, load_path)


def load_model(load_path, model, optimizer=None):
    checkpoint = torch.load(load_path)
    model.load_state_dict(checkpoint['state_dict'])
    if optimizer is not None:
        optimizer.load_state_dict(checkpoint['optimizer'])
    return checkpoint


def scaled_logit(x, lambd):
    x = lambd + (1-2*lambd)*x
    return np.log(x) - np.log1p(-x)

def scaled_logit_torch(x, lambd):
    x = lambd + (1-2*lambd)*x
    return x.log() - (-x).log1p()

def inverse_scaled_logit(x, lambd):
    sigmoid = torch.nn.Sigmoid()
    return (sigmoid(x) - lambd)/(1-2*lambd)


def reparameterize(mu, logvar):
    std = logvar.mul(0.5).exp_()
    eps = mu.new_empty(size=std.shape).normal_()
    return eps.mul(std).add_(mu)
