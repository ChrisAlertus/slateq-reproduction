import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# TODO write returns for each of these pdfs

def get_power_law(a, m):
    """
    Defining a discrete power law probability density function of length

        a : a parameter of the distribution that controls 
        m : number of discrete values in the range of the r.v 
            following the power law
    """

    values = np.arange(1, m+1, dtype='float')
    pmf = 1/values**a
    pmf /= pmf.sum()

    return stats.rv_discrete(values=(range(1, m+1), pmf)), pmf



def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    """
    Sample from a truncated normal distribution with parameters specified

    Args:
        mean : real value representing the mean of the r.v
        sd : real number representing the standard deviation of the r.v
        low : lower bound value for the r.v
        upp: upper bound value on the r.v.
    """
    return stats.truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def get_normal(mean=0, sd=1):
    """
    Sample from a normal distribution with parameters specified

    Args:
        mean : real value representing the mean of the r.v
        sd : real number representing the standard deviation of the r.v
    """
    return stats.norm(loc=mean, scale=sd)

def get_constant_distribution(constant=10):
    """
    Sample from a constant distribution

    Args:
        constant : value to return from constant "distribution"
    """
    return stats.uniform(loc=constant, scale=0)

if __name__ == "__main__":
    # Demo of the Power Law
    a, m = 1.004, 10
    distribution, pmf  = get_power_law(a=a, m=m)

    N = 10**4
    sample = distribution.rvs(size=N)

    plt.hist(sample, bins=np.arange(m)+0.5)
    plt.show()

    # Demo of the truncated normal
    sample = get_truncated_normal(mean=8, sd=2, low=1, upp=10)
    plt.hist(sample.rvs(10000), normed=True)
    plt.show()

    # Demo of the truncated mean
    sample = get_normal(mean=8, sd=2)
    plt.hist(sample.rvs(10000), normed=True)
    plt.show()

    # Demo of uniform distibution
    sample = get_constant_distribution(constant=10)
    plt.hist(sample.rvs(10000), normed=True)
    plt.show()