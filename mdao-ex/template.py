"""
This file implements the two-component coupled model.
Now, replace the objective function. This involves
- implement a new component for objective function
- add the component to the coupled model
- connect variables to the new component
- update the optimizaiton problem definition

Follow the TODO comments in the code below.
"""

import numpy as np
import openmdao.api as om


class Component1(om.ExplicitComponent):

    def setup(self):
        """ define inputs and outputs """
        # inputs
        self.add_input('x', val=np.zeros(2))   # vector!
        self.add_input('y2', val=0.)

        # outputs
        self.add_output('y1', val=0.)

        # partials
        # I'm lazy, so I use finite difference for now.
        self.declare_partials('y1', '*', method='fd')

    def compute(self, inputs, outputs):
        """ do actual computation """
        x = inputs['x']
        y2 = inputs['y2']
        y1 = x[0] + x[1] + y2**2
        outputs['y1'] = y1


class Component2(om.ExplicitComponent):

    def setup(self):
        """ define inputs and outputs """
        # inputs
        self.add_input('x', val=np.zeros(2))
        self.add_input('y1', val=0.)

        # outputs
        self.add_output('y2', val=0.)

        # partials
        self.declare_partials('y2', '*', method='fd')

    def compute(self, inputs, outputs):
        """ do actual computation """
        x = inputs['x']
        y1 = inputs['y1']
        y2 = x[0]**2 + x[1]**2 - np.sqrt(y1)
        outputs['y2'] = y2


class ObjectiveFunction(om.ExplicitComponent):
    # TODO: implement objective function here
    def setup(self):
        """ define input and output"""
        # inputs
        self.add_input('x', val=np.zeros(2))
        self.add_input('y1', val=0.)
        self.add_input('y1', val=0.)

        # outputs
        self.add_output('f', val=0.)

        # partials
        self.declare_partials('f', '*', method='fd')

    def compute(self, inputs, outputs):
        """ do actual computation """
        x = inputs['x']
        y1 = inputs['y1']
        y2 = inputs['y2']
        f = x + y1 + y2
        outputs['f'] = f


class CoupledModel(om.Group):
    """ couple component 1 and 2 """

    def setup(self):
        """ add components as subsystem, and connect variables """

        # design variable (input to the model)
        indep = self.add_subsystem('input', om.IndepVarComp())
        indep.add_output('x', val=np.zeros(2))

        # add component 1 to this group
        self.add_subsystem('comp1', Component1())

        # add component 2 to this group
        self.add_subsystem('comp2', Component2())

        # connect coupling variables (y1 and y2)
        # Comp 1 outputs y1, which will be an input to Comp 2
        self.connect('comp1.y1', 'comp2.y1')
        # Comp 2 outputs y2, which will be an input to Comp 1
        self.connect('comp2.y2', 'comp1.y2')

        # TODO: add objective function component here> DONE
        self.add_subsystem('obj', ObjectiveFunction())
        # TODO: connect x, y1, y2 to the objective function component > DONE
        self.connect('comp1.y1', 'obj.y1')
        self.connect('comp2.y2', 'obj.y2')

        # connect input x to each variables
        self.connect('input.x', ['comp1.x', 'comp2.x', 'obj'])

        # add solvers for cycle
        # self.nonlinear_solver = om.NonlinearBlockGS(iprint=2, maxiter=100)   # nonlinear block Gauss-Seidel
        self.nonlinear_solver = om.NewtonSolver(
            iprint=2, maxiter=10, solve_subsystems=True)   # Newton's method
        self.linear_solver = om.DirectSolver()   # direct solver for linear system


if __name__ == '__main__':
    # create OpenMDAO problem
    prob = om.Problem()

    # add the model you just built
    prob.model.add_subsystem('coupled', CoupledModel(), promotes=['*'])

    # define optimization problem
    prob.model.add_design_var('input.x', lower=0.5, upper=1.5)   # design vars
    prob.model.add_objective('obj.f')   # TODO: replace the objective here.
    # prob.model.add_constraint('comp1.y1', lower=-10, upper=10.)  # add constraints like this

    # attach optimizer
    prob.driver = om.ScipyOptimizeDriver()

    # setup the model
    prob.setup(check=True)

    om.n2(prob)

    # set initial value of x
    prob.set_val('input.x', np.array([1., 1.]))

    # run nonlinear solver
    # prob.run_model()

    # run optimization
    prob.run_driver()

    # get optimized solution
    x_opt = prob.get_val('input.x')
    f_opt = prob.get_val('obj.f')   # TODO: get the objective value here.
    print('\n x_opt =', x_opt)
    print(' f_opt =', f_opt)
