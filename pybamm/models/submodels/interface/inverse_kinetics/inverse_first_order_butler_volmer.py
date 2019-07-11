#
# Bulter volmer class
#

import pybamm
from ..base_interface import BaseInterface


class BaseInverseFirstOrderButlerVolmer(BaseInterface):
    """
    A base submodel that implements the inverted form of the Butler-Volmer relation to
    solve for the reaction overpotential.

    Parameters
    ----------
    param
        Model parameters
    domain : iter of str, optional
        The domain(s) in which to compute the interfacial current. Default is None,
        in which case j.domain is used.

    """

    def __init__(self, param, domain):
        super().__init__(param, domain)

    def get_coupled_variables(self, variables):
        # Unpack
        # Multiply c_e_0 by 1 to change its id slightly and thus avoid clash with
        # the c_e_0 in delta_phi_0
        c_e_0 = variables["Leading-order average electrolyte concentration"] * 1
        delta_phi_0 = variables[
            "Leading-order average "
            + self.domain.lower()
            + " electrode surface potential difference"
        ]
        c_e = variables[self.domain + " electrolyte concentration"]
        j_0 = variables[
            "Average " + self.domain.lower() + " electrode interfacial current density"
        ]

        # Solve first-order linear problem for first-order potential
        c_e_1_av = (pybamm.average(c_e) - c_e_0) / self.param.C_e
        delta_phi_1_av = -j_0.diff(c_e_0) * c_e_1_av / j_0.diff(delta_phi_0)
        delta_phi = delta_phi_0 + self.param.C_e * delta_phi_1_av

        # Update variables dictionary
        variables.update(
            self._get_standard_surface_potential_difference_variables(delta_phi)
        )

        return variables


sum("Derivative w.r.t. c of ...")
sum("Derivative w.r.t. delta_phi of ...")