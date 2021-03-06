from pybamm import exp


def nca_electrolyte_reaction_rate_Kim2011(T, T_inf, E_r, R_g):
    """
    Reaction rate for Butler-Volmer reactions between NCA and LiPF6 in EC:DMC
    [1].

     References
    ----------
    .. [1] Kim, G. H., Smith, K., Lee, K. J., Santhanagopalan, S., & Pesaran, A.
    (2011). Multi-domain modeling of lithium-ion batteries encompassing
    multi-physics in varied length scales. Journal of The Electrochemical
    Society, 158(8), A955-A969.

    Parameters
    ----------
    T: :class: `numpy.Array`
        Dimensional temperature
    T_inf: double
        Reference temperature
    E_r: double
        Reaction activation energy
    R_g: double
        The ideal gas constant

    Returns
    -------
    : double
        Reaction rate
    """
    i0_ref = 4  # reference exchange current density at 100% SOC
    sto = 0.41  # stochiometry at 100% SOC
    c_s_max = 4.9 * 10 ** 4  # max electrode concentration
    c_s_ref = sto * c_s_max  # reference electrode concentration
    c_e_ref = 1.2 * 10 ** 3  # reference electrolyte concentration
    alpha = 0.5  # charge transfer coefficient

    m_ref = (
        2
        * i0_ref
        / (c_e_ref ** alpha * (c_s_max - c_s_ref) ** alpha * c_s_ref ** alpha)
    )
    arrhenius = exp(E_r / R_g * (1 / T_inf - 1 / T))

    return m_ref * arrhenius
