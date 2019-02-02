
import numpy as np

def run_whole(n_parts, n_rounds, n_info, n_particles, mutation_rate, base_prob, act_prob = None, max_rule = False):

    if act_prob is None:
        act_prob = base_prob
    
    goods = []
    final_pops = []
    net_evidences = []
    posts = []    
    
    for i in range(n_parts):
        
        good = np.random.random() < 0.5
        
        out = run_part(n_rounds, n_info, n_particles, mutation_rate, base_prob, act_prob, good, max_rule)
        
        goods += [good]
        final_pops += [out['final_pop']]
        net_evidences += [out['net_evidence']]
        posts += [out['post']]        

    return goods, final_pops, net_evidences, posts

def run_part(n_rounds, n_info, n_particles, mutation_rate, base_prob, act_prob, good, max_rule):

    data = np.random.random([n_rounds,n_info]) < (good * base_prob + (1 - good) * (1 - base_prob))

    num_good,num_bad = particle_filter(data, n_rounds, n_particles, mutation_rate, act_prob, max_rule)

    x = np.sum(data)
    y = np.sum(1 - data)
    post = base_prob**x * (1 - base_prob)**y
    post /= (base_prob**x * (1 - base_prob)**y + (1 - base_prob)**x * base_prob**y)
    
    return {'net_evidence':np.mean(data), 'final_pop':(num_good/(num_good + num_bad)), 'post':post}


def particle_filter(data, n_rounds, n_particles, mutation_rate, base_prob, max_rule):
    
    p = 0.5

    for i in range(n_rounds):
        
        num_good = np.random.binomial(n_particles, p)
        num_bad = n_particles - num_good
        
        round_good_like = likelihood(data[i], base_prob)
        round_bad_like = likelihood(data[i], 1 - base_prob)
        
        p = good_particle_prob(num_good, num_bad, round_good_like, round_bad_like)
        
        if max_rule:
            p = 1 if p > 0.5 else 0
        
        p = (1 - mutation_rate) * p + mutation_rate * 0.5

    return num_good, num_bad

def good_particle_prob(num_good, num_bad, round_good_like, round_bad_like):
    
    good_weight = num_good * round_good_like
    bad_weight = num_bad * round_bad_like
    
    return good_weight / (good_weight + bad_weight)

def likelihood(data, prob):
    """
    >>> likelihood(np.array([0,0,0,1]), 0.6)
    0.038400000000000011
    """
    
    return np.prod(prob * data  + (1 - prob) * (1 - data))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

