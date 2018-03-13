class OpenshiftTools:

    def __init__(self):
        pass

    # ============================================================================== #
    #   Functions to format json file in order to push to openshift API              #
    #   session to create all format functions of this class                         #
    # ============================================================================== #
    #
    def insert_environment(self, dc, overwrite, environment, json_data):
        """
            Method to insert all new Openshift environment and update all environment
            that already exists.

        :param dc:              Specific name of the deployment-config.
        :param overwrite:       Variable to control if will be overwriting existing variables (True/False).
        :param environment:     List of variables to be add into a DeploymentConfig.
        :param json_data:       Variable with all json formatted and ready to push to API/OAPI.
        :return:                Return the gathered json from API/OAPI with new envs inside.
        """

        if dc is None or json_data is None or environment is None:
            print("==> Error: DeploymentConfig, json_data or Environment not informed, exiting...")
            exit(1)
        else:
            # List with all new environment to be add in our DC
            lista_variaveis = []

            for item in environment.split(','):
                env = item.split('=', maxsplit=1)
                lista_variaveis.append(
                    {
                        'name': '{0}'.format(env[0]),
                        'value': '{0}'.format(env[1])
                    })

            # List to control and ensures no duplications in our DC
            list_not_add = []

            for containers in json_data['spec']['template']['spec']['containers']:
                if dc in containers['name']:
                    if overwrite:
                        for env in containers['env']:
                            for new_env in lista_variaveis:
                                if env['name'] == new_env['name']:
                                    env['value'] = new_env['value']
                                    list_not_add.append(new_env['name'])
                                    pass
                                pass
                            pass
                        pass
                        for item in lista_variaveis:
                            if item['name'] not in list_not_add:
                                containers.setdefault('env', []).append(item)
                                pass
                            pass
                        pass
                    else:
                        for item in lista_variaveis:
                            containers['env'].append(item)
                            pass
                        pass
                    pass
                else:
                    for item in lista_variaveis:
                        containers.setdefault('env', []).append(item)
                        pass
                    pass
                pass
            # Return data formated and ready for OAPI/API
            return json_data

        # Impossible to get here... But keep it for curiosity rs
        exit(1)

    #
    def insert_resourcelimits(self, dc, cpu_type, cpu_req, cpu_lim, mem_type, mem_req, mem_lim, json_data):
        """
            Method to insert a resource-limits to a DeploymentConfig inside a project on Openshift.

        :param dc:              Specific name of the deployment-config.
        :param cpu_type:        Variable that shows and control the type(C,mC) imputed.
        :param cpu_req:         Variable with the CPU requirement (lowest value) for it.
        :param cpu_lim:         Variable with the CPU maximum usage (highest value) for it.
        :param mem_type:        Variable that shows and control the type(M,G) imputed.
        :param mem_req:         Variable with the MEM requirement (lowest value) for it.
        :param mem_lim:         Variable with the MEM maximum usage (highest value) for it.
        :param json_data:       Variable with all json formatted and ready to push to API/OAPI.
        :return:                Return the gathered json from API/OAPI with new envs inside.
        """

        if dc is None or json_data is None:
            print("==> Error: DeploymentConfig or json_data not informed, exiting...")
            exit(1)
        else:
            for containers in json_data['spec']['template']['spec']['containers']:
                #
                # Check if key exist.
                if not containers['resources'].get('requests'):
                    containers['resources'].setdefault('requests', {})

                # Check if key exist.
                if not containers['resources'].get('limits'):
                    containers['resources'].setdefault('limits', {})

                # ------------------------------------------------ #

                # Define resource requests. if has some value
                if cpu_req is not None:
                    containers['resources'].setdefault('requests', {'cpu', cpu_req})

                if mem_req is not None:
                    containers['resources'].setdefault('requests', {'mem', mem_req})

                # ------------------------------------------------ #

                # Define resource limits, if has some value
                if cpu_lim is not None:
                    containers['resouces'].setdefault('limits', {'cpu': cpu_lim})

                if mem_lim is not None:
                    containers['resouces'].setdefault('limits', {'mem': mem_lim})

                # ------------------------------------------------ #

        return json_data

    def insert_route(self, service, tls_enabled, type_tls, json_data):
        """
            Method to format/insert all values passed into the json.
            It check's if the key exists or not to insert or to create and
            then insert into.

        :param service:     Name of the service this route will refer to.
        :param tls_enabled: Enable/Disable TLS in this route.
        :param type_tls:    If tlsEnabled, set the TLS type. If not, even touch it.
        :param json_data:   Variable with all json formatted and ready to push to API/OAPI.
        :return:            Return the gathered json from API/OAPI with the route values inside.
        """

        # Check TLS usage.
        # if not set True, then delete de TLS field
        if tls_enabled:
            json_data['spec'].setdefault('tls', {'termination': str(type_tls)})
        else:
            json_data['spec']['tls'].delete()

        # Update route service
        json_data['spec']['to'].setdefault('name', str(service))

        #
        return json_data

    def insert_probe_liveness(self, path, init_delay, timeout, json_data):
        """
            Method to insert/edit a LivenessProbe from a specified DeploymentConfig

        :param path:            Path for liveness to probe for.
        :param init_delay:      Initial delay (from creation) to start probing.
        :param timeout:         Time to consider it a TimeOut in probing.
        :param json_data:       Variable with all json formatted and ready to push to API/OAPI.
        :return:                Return the gathered json from API/OAPI with the route values inside.
        """

        for containers in json_data['spec']['template']['spec']['containers']:
            containers.setdefault('livenessProbe', {
                'failureThreshold': 3,
                'httpGet': {
                    'path': path,
                    'port': 8080,
                    'scheme': 'HTTP'
                },
                'initialDelaySeconds': init_delay,
                'periodSeconds': 10,
                'successThreshold': 1,
                'timeoutSeconds': timeout
            })
        return json_data

    def insert_probe_readiness(self, path, init_delay, timeout, json_data):
        """
            Method to insert/edit a ReadinessProbe from a specified DeploymentConfig

        :param path:            Path for readiness to probe for.
        :param init_delay:      Initial delay (from creation) to start probing.
        :param timeout:         Time to consider it a TimeOut in probing.
        :param json_data:       Variable with all json formatted and ready to push to API/OAPI.
        :return:                Return the gathered json from API/OAPI with the route values inside.
        """
        for containers in json_data['spec']['template']['spec']['containers']:
            containers.setdefault('readinessProbe', {
                'failureThreshold': 3,
                'httpGet': {
                    'path': path,
                    'port': 8080,
                    'scheme': 'HTTP'
                },
                'initialDelaySeconds': int(init_delay),
                'periodSeconds': 10,
                'successThreshold': 1,
                'timeoutSeconds': int(timeout)
            })
        return json_data

    def insert_autoscale(self, scale_minimum, scale_maximum, cpu_usage, json_data):
        """
            Method to insert/edit a scale from a specified DeploymentConfig

        :param scale_minimum:       Minimum scale required for this deploymentconfig (default 1)
        :param scale_maximum:       Maximum scale required for this deploymentconfig (defalt 1)
        :param cpu_usage:           CPU usage requested to scale a deploymentconfig (default 80%)
        :param json_data:           Variable with all json formatted and ready to push to API/OAPI.
        :return:                    Return the gathered json from API/OAPI with the scale values.
        """
        # ================================================== #
        # Validation process (Default values)
        if int(scale_minimum) <= 1 or scale_minimum is None:
            scale_minimum = 1

        if int(scale_maximum) <= 1 or scale_maximum is None:
            scale_maximum = 1

        if int(cpu_usage) <= 1 or cpu_usage is None:
            cpu_usage = 80

        # ================================================== #
        if json_data['kind'] == 'HorizontalPodAutoscaler':
            ####
            if json_data['spec'].get('minReplicas'):
                json_data['spec']['minReplicas'] = int(scale_minimum)
            else:
                json_data['spec'].setdefault('minReplicas', int(scale_minimum))
            ####
            if json_data['spec'].get('maxReplicas'):
                json_data['spec']['maxReplicas'] = int(scale_maximum)
            else:
                json_data['spec'].setdefault('maxReplicas', int(scale_maximum))
            ####
            if json_data['spec'].get('targetCPUUtilizationPercentage'):
                json_data['spec']['targetCPUUtilizationPercentage'] = int(cpu_usage)
            else:
                json_data['spec'].setdefault('targetCPUUtilizationPercentage', int(cpu_usage))
            ####
        return json_data

