#
# Class for two-dimensional current collectors
#
import pybamm
from .base_surface_form_current_collector import BaseSurfaceForm


class LeadingOrder(BaseSurfaceForm):
    """A submodel for Ohm's law plus conservation of current in the current collectors,
    which uses the voltage-current relationship from the SPM(e).

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel


    **Extends:** :class:`pybamm.current_collector.surface_form.BaseSurfaceForm`
    """

    def __init__(self, param):
        super().__init__(param)

    def get_coupled_variables(self, variables):

        delta_phi_n_av = variables[
            "Average negative electrode surface potential difference"
        ]
        delta_phi_p_av = variables[
            "Average positive electrode surface potential difference"
        ]
        phi_s_cn = delta_phi_n_av
        phi_s_cp = delta_phi_p_av - delta_phi_n_av
        variables = self._get_standard_potential_variables(phi_s_cn, phi_s_cp)

        # Define conductivity
        param = self.param
        vertical_conductivity = (
            param.l_n * param.sigma_n_dash * param.l_p * param.sigma_p_dash
        ) / (param.l_n * param.sigma_n_dash + param.l_p * param.sigma_p_dash)

        # Simple model: read off vertical current (no extra equation)
        delta_phi_difference = delta_phi_n_av - delta_phi_p_av
        I_s_perp = vertical_conductivity * pybamm.grad(delta_phi_difference)
        i_boundary_cc = pybamm.div(I_s_perp)

        # TODO: grad not implemented for 2D yet
        i_cc = pybamm.Scalar(0)

        variables.update(self._get_standard_current_variables(i_cc, i_boundary_cc))

        return variables

    def set_boundary_conditions(self, variables):

        delta_phi_n_av = variables[
            "Average negative electrode surface potential difference"
        ]
        delta_phi_p_av = variables[
            "Average positive electrode surface potential difference"
        ]
        delta_phi_difference = delta_phi_n_av - delta_phi_p_av

        # Set boundary conditions at top ("right") and bottom ("left")
        param = self.param
        i_cell = param.current_density_with_time
        top_bc = (param.l_n * param.l_p * param.sigma_n_dash * i_cell) / (
            param.l_n * param.sigma_n_dash * param.l_p * param.sigma_p_dash
        )
        self.boundary_conditions = {
            delta_phi_difference: {
                "left": (pybamm.Scalar(0), "Neumann"),
                "right": (top_bc, "Neumann"),
            }
        }