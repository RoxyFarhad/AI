from bayesnet import Node, BayesNet
import time

def sample_all_nonevidence(BN, evidence, num_samples):
    nonevidence = []
    for node in BN.nodes:
        if node.name not in evidence:
            nonevidence.append(node)

    print("Rejection sampling: \t", end="")
    total_accepted = 0
    total_samples = 0
    total_time = 0
    for node in nonevidence:
        start = time.time()
        estimate, accepted = BN.infer(node.name, evidence, num_samples, 'rejection')
        end = time.time()
        total_accepted += accepted
        total_samples += num_samples
        total_time += end-start
        print(node.name + ": " + "%.4f" % estimate + ", ", end="")
    print("\nAverage acceptance rate, time per sample: %.4f, " % (total_accepted/total_samples) + "%.6f" % (total_time/total_samples) + " sec")

    print("Likelihood weighting: \t", end="")
    total_weight = 0
    total_samples = 0
    total_time = 0
    for node in nonevidence:
        start = time.time()
        estimate, weight = BN.infer(node.name, evidence, num_samples, 'likelihood')
        end = time.time()
        total_weight += weight
        total_samples += num_samples
        total_time += end-start
        print(node.name + ": " + "%.4f" % estimate + ", ", end="")
    print("\nAverage sample weight, time per sample: %.4f, " % (total_weight/total_samples) + "%.6f" % (total_time/total_samples) + " sec")

    print("Gibbs sampling: \t\t", end="")
    total_time = 0
    total_samples = 0
    for node in nonevidence:
        start = time.time()
        estimate, N = BN.infer(node.name, evidence, num_samples, 'Gibbs')
        end = time.time()
        total_time += end-start
        total_samples += num_samples
        print(node.name + ": " + "%.4f" % estimate + ", ", end="")
    print("\nAverage time per sample: %.6f" % (total_time / total_samples) + " sec")

if __name__ == '__main__':
    # Simple diagnostic network
    influenza = Node('I', [], {(): 0.05})
    smokes = Node('S', [], {(): 0.2})
    sore_throat = Node('ST', [influenza], {(True,): 0.3, (False,): 0.001})
    fever = Node('F', [influenza], {(True,): 0.9, (False,): 0.05})
    bronchitis = Node('B', [influenza, smokes], {(True,True): 0.99, (True,False): 0.9, (False,True): 0.7, (False,False): 0.0001})
    coughing = Node('C', [bronchitis], {(True,): 0.8, (False,): 0.07})
    wheezing = Node('W', [bronchitis], {(True,): 0.6, (False,): 0.001})
    diagnostic_BN = BayesNet([influenza, smokes, sore_throat, fever, bronchitis, coughing, wheezing])

    print("Estimated marginals of diagnostic network given no evidence")
    sample_all_nonevidence(diagnostic_BN, {}, 10000)
    print("\nEstimated marginals of diagnostic network given influenza")
    sample_all_nonevidence(diagnostic_BN, {'I': True}, 10000)
    print("\nEstimated marginals of diagnostic network given no bronchitis")
    sample_all_nonevidence(diagnostic_BN, {'B': False}, 10000)
    print("\nEstimated marginals of diagnostic network given sore throat and fever")
    sample_all_nonevidence(diagnostic_BN, {'ST': True, 'F': True}, 10000)
    print("\nEstimated marginals of diagnostic network given neither coughing nor wheezing")
    sample_all_nonevidence(diagnostic_BN, {'C': False, 'W': False}, 10000)
    print("\nEstimated marginals of diagnostic network given sore throat, fever, coughing, and wheezing")
    sample_all_nonevidence(diagnostic_BN, {'ST': True, 'F': True, 'C': True, 'W': True}, 10000)
    print("\nEstimated marginals of diagnostic network given none of sore throat, fever, coughing, and wheezing")
    sample_all_nonevidence(diagnostic_BN, {'ST': False, 'F': False, 'C': False, 'W': False}, 10000)

    # Leader-follower network
    num_followers = 10
    L = Node('L', [], {(): 0.5})
    followers = []
    for i in range(num_followers):
        followers.append(Node('F'+str(i), [L], {(True,): 0.9, (False,): 0.1}))
    follower_BN = BayesNet([L] + followers)

    print("\nEstimated marginals of leader-follower network given no evidence")
    sample_all_nonevidence(follower_BN, {}, 10000)
    print("\nEstimated marginals of leader-follower network given one follower")
    sample_all_nonevidence(follower_BN, {'F0': True}, 10000)
    print("\nEstimated marginals of leader-follower network given half followers")
    evidence = {}
    for i in range(int(len(followers)/2)):
        evidence[followers[i].name] = True
    sample_all_nonevidence(follower_BN, evidence, 10000)
    print("\nEstimated marginals of leader-follower network given all followers")
    evidence = {}
    for node in followers:
        evidence[node.name] = True
    sample_all_nonevidence(follower_BN, evidence, 10000)