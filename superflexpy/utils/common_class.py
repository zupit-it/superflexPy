"""
Copyright 2019 Marco Dal Molin et al.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This file is part of the SuperflexPy modelling framework. For details about it,
visit the page https://superflexpy.readthedocs.io

CODED BY: Marco Dal Molin
DESIGNED BY: Marco Dal Molin, Fabrizio Fenicia

This file contains the implementation of a class that implements methods that
are useful for Unit, Node, and Network.
"""


class CommonClass(object):
    """
    This is the abstract class for the cration of the components Unit, Node,
    and Network. It defines a series of methods that are common among the
    components.
    """

    _content_pointer = {}
    _content = []  # Note that it can also be a dictionary

    def get_parameters(self, names=None):
        """
        This method returns the parameters of the element.

        Parameters
        ----------
        names : list(str)
            Names of the parameters to return. The names must be the ones
            returned by the mehod get_parameters_name. If None, all the
            parameters are returned.

        Returns
        -------
        dict:
            Parameters of the element.
        """

        parameters = {}

        if names is None:
            for c in self._content_pointer.keys():
                position = self._content_pointer[c]
                try:
                    cont_pars = self._content[position].get_parameters()
                except AttributeError:
                    continue
                for k in cont_pars:
                    if k not in parameters:
                        parameters[k] = cont_pars[k]
        else:
            for n in names:
                position = self._find_content_from_name(n)
                if position is None:
                    for c in self._content_pointer.keys():
                        position = self._content_pointer[c]
                        try:
                            cont_pars = self._content[position].get_parameters([n])
                            break
                        except (AttributeError, KeyError):  # Attribute error because the content may not have the method, Key error because the parameter may not belong to the content
                            continue
                else:
                    cont_pars = self._content[position].get_parameters([n])

                parameters = {**parameters, **cont_pars}

        return parameters

    def get_parameters_name(self):
        """
        This method returns the names of the parameters of the element.

        Returns
        -------
        list(str):
            List with the names of the parameters.
        """

        return list(self.get_parameters().keys())

    def _find_content_from_name(self, name):

        splitted_name = name.split('_')

        try:
            class_id = self.id
        except AttributeError:  # We are in a Model
            class_id = None

        if class_id is not None:
            # HRU or Catchment
            if class_id in splitted_name:
                ind = splitted_name.index(class_id)
            else:
                ind = -1  # TODO: check

            position = self._content_pointer[splitted_name[ind + 1]]
        else:
            # Model
            for c in self._content_pointer.keys():
                if c in splitted_name:
                    position = self._content_pointer[c]
                    break
                else:
                    position = None

        return position

    def set_parameters(self, parameters):
        """
        This method sets the values of the parameters.

        Parameters
        ----------
        parameters : dict
            Contains the parameters of the element to be set. The keys must be
            the ones returned by the method get_parameters_name. Only the
            parameters that have to be changed should be passed.
        """

        for p in parameters.keys():
            position = self._find_content_from_name(p)

            if position is None:
                for c in self._content_pointer.keys():
                    try:
                        position = self._content_pointer[c]
                        self._content[position].set_parameters({p: parameters[p]})
                        break
                    except (KeyError, ValueError):
                        continue
            else:
                self._content[position].set_parameters({p: parameters[p]})

    def get_states(self, names=None):
        """
        This method returns the states of the element.

        Parameters
        ----------
        names : list(str)
            Names of the states to return. The names must be the ones
            returned by the mehod get_states_name. If None, all the
            states are returned.

        Returns
        -------
        dict:
            States of the element.
        """

        states = {}

        if names is None:
            for c in self._content_pointer.keys():
                position = self._content_pointer[c]
                try:
                    cont_st = self._content[position].get_states()
                except AttributeError:
                    continue
                for k in cont_st:
                    if k not in states:
                        states[k] = cont_st[k]
        else:
            for n in names:
                position = self._find_content_from_name(n)
                if position is None:
                    for c in self._content_pointer.keys():
                        position = self._content_pointer[c]
                        try:
                            cont_st = self._content[position].get_states([n])
                            break
                        except (AttributeError, KeyError):  # Attribute error because the content may not have the method, Key error because the parameter may not belong to the content
                            continue
                else:
                    cont_st = self._content[position].get_states([n])

                states = {**states, **cont_st}

        return states

    def get_states_name(self):
        """
        This method returns the names of the states of the element.

        Returns
        -------
        list(str):
            List with the names of the states.
        """

        return list(self.get_states().keys())

    def set_states(self, states):
        """
        This method sets the values of the states.

        Parameters
        ----------
        states : dict
            Contains the states of the element to be set. The keys must be
            the ones returned by the method get_states_name. Only the
            states that have to be changed should be passed.
        """

        for s in states.keys():
            position = self._find_content_from_name(s)

            if position is None:
                for c in self._content_pointer.keys():
                    try:
                        position = self._content_pointer[c]
                        self._content[position].set_states({s: states[s]})
                        break
                    except (KeyError, ValueError):
                        continue
            else:
                self._content[position].set_states({s: states[s]})

    def reset_states(self, id=None):
        """"
        This method sets the states to the values provided to the __init__
        method. If a state was initialized as None, it will not be reset.

        Parameters
        ----------
        id : list(str)
            List of element's id where the method is applied.
        """

        if id is None:
            for c in self._content_pointer.keys():
                position = self._content_pointer[c]
                try:
                    self._content[position].reset_states()
                except AttributeError:
                    continue
        else:
            if isinstance(id, str):
                id = [id]
            for i in id:
                position = self._find_content_from_name(i)

                # TODO: With states we do not have the case position = None
                self._content[position].reset_states()

    def get_timestep(self):
        """
        This method returns the timestep used by the element.

        Returns
        -------
        float
            Timestep
        """
        return self._dt

    def set_timestep(self, dt):
        """
        This method sets the timestep used by the element.

        Parameters
        ----------
        dt : float
            Timestep
        """

        self._dt = dt

        for c in self._content_pointer.keys():
            position = self._content_pointer[c]

            try:
                self._content[position].set_timestep(dt)
            except AttributeError:
                continue

    def define_solver(self, solver):
        """
        This method define the solver to use for the differential equation.

        Parameters
        ----------
        solver : superflexpy.utils.root_finder.RootFinder
            Solver used to find the root(s) of the differential equation(s).
            Child classes may implement their own solver, therefore the tipe
            of the solver is not enforced.
        """

        for c in self._content_pointer.keys():
            position = self._content_pointer[c]

            try:
                self._content[position].define_solver(solver)
            except AttributeError:
                continue
