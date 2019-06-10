import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative

def bifurcation_data_fixed_x(
    f, init, y_points=100, dropped_steps=2000, lyapunov=False, deriv=None, **kwargs
):
    x = init
    lyap = 0

    for i in range(dropped_steps):
        x = f(x)

    res = np.zeros(y_points)

    for i in range(y_points):
        x = f(x)
        res[i] = x

        if lyapunov:
            if deriv is None:
                lyap += np.log(np.absolute(derivative(f, x)))
            else:
                lyap += np.log(np.absolute(deriv(x)))

    lyap /= dropped_steps + y_points

    return res, lyap


def bifurcation_plot_data(
    dynamic_generator, init, parameter_range, y_points=100, **kwargs
):
    x_list = np.array([])
    y_list = np.array([])
    lyap_x = []
    lyap_y = []

    for p in parameter_range:
        f = dynamic_generator(p)

        deriv = None
        if "deriv_generator" in kwargs:
            deriv = kwargs["deriv_generator"](p)

        y_res, lyap = bifurcation_data_fixed_x(
            f, init=init, y_points=y_points, deriv=deriv, **kwargs
        )

        x_pad = np.full(y_points, p)
        x_list = np.append(x_list, x_pad)
        y_list = np.append(y_list, y_res)

        lyap_x.append(p)
        lyap_y.append(lyap)

    return (x_list, y_list, lyap_x, lyap_y)


def bifurcation_and_lyapunov_plots(dynamic_generator, init, parameter_range, **kwargs):

    if not "alpha" in kwargs:
        kwargs["alpha"] = 0.25

    bif_x, bif_y, lya_x, lya_y = bifurcation_plot_data(
        dynamic_generator,
        init=init,
        parameter_range=parameter_range,
        lyapunov=True,
        **kwargs
    )

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 9))

    ax1.plot(bif_x, bif_y, "k,", alpha=kwargs["alpha"])
    ax1.set_title("Bifurcation Diagram")
    ax1.set_xlim(parameter_range[0], parameter_range[-1])

    if "xlabel" in kwargs:
        plt.xlabel(kwargs["xlabel"])

    if "ylabel" in kwargs:
        plt.ylabel(kwargs["ylabel"])

    ax2.plot(lya_x, lya_y, "k-", linewidth=1)
    ax2.set_title("Lyapunov Exponents")
    ax2.axhline(color="k", linewidth=0.5)
    ax2.set_xlim(parameter_range[0], parameter_range[-1])

    if "xlabel" in kwargs:
        plt.xlabel(kwargs["xlabel"])

    if "xlabel" in kwargs:
        plt.ylabel("Lyapunov exponent")

    if "suptitle" in kwargs:
        fig.suptitle(kwargs["suptitle"])

    plt.tight_layout()

    if "file_name" in kwargs:
        plt.savefig(kwargs["file_name"], dpi=300)
    else:
        plt.show()


def bifurcation_plot(
    dynamic_generator,
    init=np.array([0.4]),
    parameter_range=np.linspace(0, 1, num=1000),
    **kwargs
):
    if not "alpha" in kwargs:
        kwargs["alpha"] = 0.25

    if not "figsize" in kwargs:
        kwargs["figsize"] = (8, 4.5)

    if not "ax" in kwargs:
        fig, ax1 = plt.subplots(1, 1, figsize=kwargs["figsize"])
    else:
        ax1 = kwargs['ax']

    bif_x, bif_y, lya_x, lya_y = bifurcation_plot_data(
        dynamic_generator, init=init, parameter_range=parameter_range, **kwargs
    )


    ax1.plot(bif_x, bif_y, "k,", alpha=kwargs["alpha"])
    
    if "set_title" in kwargs:
        ax1.set_title(kwargs["set_title"])
    
    ax1.set_xlim(parameter_range[0], parameter_range[-1])

    if "xlabel" in kwargs:
        ax1.set_xlabel(kwargs["xlabel"])

    if "ylabel" in kwargs:
        ax1.set_ylabel(kwargs["ylabel"])

    plt.tight_layout()

    if "file_name" in kwargs:
        plt.savefig(kwargs["file_name"], dpi=300)
    elif not "ax" in kwargs:
        plt.show()


def cobweb_plot(dynamic, init, iterations, domain=np.linspace(0, 1), **kwargs):

    if not "alpha" in kwargs:
        kwargs["alpha"] = 0.5

    if not "ax" in kwargs:
        fig, ax = plt.subplots(1, 1)
    else:
        ax = kwargs["ax"]

    # Plot the map
    func = list(map(dynamic, domain))
    # ax.plot(domain, dynamic(domain), 'k', linewidth=2) # fails on maps that operate on vectors
    ax.plot(domain, func, "k", linewidth=2)

    # Plot the y=x line of reflection
    ax.plot([domain[0], domain[-1]], [domain[0], domain[-1]], "k--", linewidth=1)

    x = init

    for i in range(iterations):
        xPrime = dynamic(x)

        # from reflection line to curve
        ax.plot([x, x], [x, xPrime], "k", linewidth=kwargs["alpha"])

        # from curve to reflection line
        ax.plot([x, xPrime], [xPrime, xPrime], "k", linewidth=1)

        ax.plot([x], [xPrime], "ok", alpha=kwargs["alpha"])

        x = xPrime

    if "xlabel" in kwargs:
        ax.set_xlabel(kwargs["xlabel"])

    if "ylabel" in kwargs:
        ax.set_ylabel(kwargs["ylabel"])

    if "set_title" in kwargs:
        ax.set_title(kwargs["set_title"])

    if not "ax" and not "file_name" in kwargs:
        plt.show()
    elif "file_name" in kwargs:
        plt.savefig(kwargs["file_name"], dpi=300)
