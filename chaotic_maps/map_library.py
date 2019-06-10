import numpy as np


def logistic_map(r):
    def dynamic(x):
        return r * x * (1 - x)

    return dynamic


def logistic_map_deriv(r):
    def deriv(x):
        return r - 2 * r * x

    return deriv


def gauss_map_family(alpha):
    def generator(beta):
        def map(x):
            return np.exp(-1 * alpha * (x ** 2)) + beta

        return map

    return generator


def sin_map(mu):
    def dynamic(x):
        return mu * np.sin(np.pi * x)

    return dynamic


def sin_map_deriv(mu):
    def deriv(x):
        return mu * np.cos(np.pi * x) * np.pi

    return deriv


def cos_map(mu):
    def dynamic(x):
        return mu * np.cos(np.pi * x)

    return dynamic


def cos_map_deriv(mu):
    def deriv(x):
        return -1 * mu * np.sin(np.pi * x) * np.pi


def tent_map(mu):
    def dynamic(x):
        if x[0] < 0.5:
            return mu * x
        else:
            return mu * (1 - x)

    return dynamic


def cubic_map(r):
    def dynamic(x):
        return r * x - x ** 3

    return dynamic


def henon_map_family(b):
    def generator(a):
        def dynamic(x):
            # Yields overflow errors in numpy after more than ~25 iterations
            prime = np.array((1 - (a * x[0] * x[0]) + (b * x[1]), x[0]))
            return prime

        return dynamic

    return generator


def discrete_time_imitative_logit_family(A):
    A = np.array(A)

    def generator(beta):
        def dynamic(x):
            u = (x, 1 - x)
            adjusted_payoffs = np.exp(A.dot(u) * beta)
            bar = np.inner(u, adjusted_payoffs)
            top = np.multiply(u, adjusted_payoffs)
            return top[0] / bar

        return dynamic

    return generator


def discrete_time_replicator(A):
    A = np.array(A)

    def dynamic(x):
        u = (x, 1 - x)
        payoffs = A.dot(u)
        bar = np.inner(u, payoffs)
        return x * payoffs[0] / bar

    return dynamic


def smoothed_best_response_family(A):
    A = np.array(A)

    def generator(beta):
        def dynamic(x):
            u = (x, 1 - x)
            smoothed_payoffs = np.exp(A.dot(u) * beta)
            denom = sum(smoothed_payoffs)
            return smoothed_payoffs[0] / denom

        return dynamic

    return generator
