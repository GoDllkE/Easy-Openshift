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

        if dc is None or json_data is None or new_envs is None:
            print("==> Error: DeploymentConfig, json_data or Environment not informed, exiting...")
            exit(1)
        else:
            # List with all new environment to be add in our DC
            lista_variaveis = []

            for item in environment.split(','):
                env = item.split(' ', maxsplit=1)
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

    def validate_limits_fields(self, cpu_type, cpu_req, cpu_lim, mem_type, mem_req, mem_lim):
        """
            Method to validate all resource-limits data desired. Not only validate but also
            format everything to be pushed into the OAPI/API.

        :param cpu_type:        Variable that shows and control the type(C,mC) imputed.
        :param cpu_req:         Variable with the CPU requirement (lowest value) for it.
        :param cpu_lim:         Variable with the CPU maximum usage (highest value) for it.
        :param mem_type:        Variable that shows and control the type(M,G) imputed.
        :param mem_req:         Variable with the MEM requirement (lowest value) for it.
        :param mem_lim:         Variable with the MEM maximum usage (highest value) for it.
        :return:                Return all Variables validated/formatted and ready to be inserted on json.
        """

        # Regex
        regex = '\d'
        decimal_regex = '\d.\d'

        if cpu_type in ['milicore', 'core']:
            if cpu_type == 'milicore':
                cpu_type = 'm'
            else:
                cpu_type = ''
        else:
            print("==> Error: Invalid CPU Type ({0}), exiting".format(cpu_type))
            exit(1)

        if mem_type in ['Mega', 'Giga']:
            if mem_type == 'Mega':
                mem_type = 'M'
            else:
                mem_type = 'G'
        else:
            print("==> Error: Invalid MEMORY Type ({0}), exiting".format(mem_type))
            exit(1)

        # Check cpu_request field
        if not re.match(regex, str(cpu_req)) \
                and not re.match(regex, str(cpu_req)) \
                and not re.match(decimal_regex, str(cpu_req)) \
                and not re.match(decimal_regex, str(cpu_req)):
            print("==> Warning: Not a valid value for CPU_REQUEST ({0}), "
                  "setting the default one...".format(cpu_req))
            cpu_req = 50

        # Check cpu_limits field
        if not re.match(regex, str(cpu_lim)) \
                and not re.match(regex, str(cpu_lim)) \
                and not re.match(decimal_regex, str(cpu_lim)) \
                and not re.match(decimal_regex, str(cpu_lim)):
            print("==> Warning: Not a valid value for CPU_LIMIT ({0}), "
                  "setting the default one...".format(cpu_lim))
            cpu_lim = 1024

        # Check memory_request field
        if not re.match(regex, str(mem_req)) \
                and not re.match(regexstr(mem_req)) \
                and not re.match(decimal_regex, str(mem_req)) \
                and not re.match(decimal_regex, str(mem_req)):
            print("==> Warning: Not a valid value for MEMORY_REQUEST ({0}), "
                  "setting the default one...".format(mem_req))
            mem_req = 512

        # Check memory_limits field (for Mega or Giga)
        if not re.match(regex, str(mem_lim)) \
                and not re.match(regex, str(mem_lim)) \
                and not re.match(decimal_regex, str(mem_lim)) \
                and not re.match(decimal_regex, str(mem_lim)):
            print("==> Warning: Not a valid value for MEMORY_LIMIT ({0}), "
                  "setting the default one...".format(mem_lim))
            mem_lim = 1024

        # Validate values and their scale
        if cpu_req > cpu_lim:
            print("==> Error: CPU_REQUEST ({0}) is greater than CPU_LIMITS ({1}), "
                  "fix it!".format(cpu_req, cpu_lim))
            exit(1)
        elif mem_req > mem_lim:
            print("==> Error: MEM_REQUEST ({0}) is greater than MEM_LIMITS ({0}), "
                  "fix it!".format(mem_req, mem_lim))
            exit(1)

        # Return values formatted
        return '{0}{1}'.format(cpu_req, cpu_type), \
               '{0}{1}'.format(cpu_lim, cpu_type), \
               '{0}{1}'.format(mem_req, mem_type), \
               '{0}{1}'.format(mem_lim, mem_type)

    #
    def insert_resourcelimits(self, dc, cpu_type, cpu_req, cpu_lim, mem_type, mem_req, mem_lim, json_data):
        """
            Method to insert a resouce-limits to a DeploymentConfig inside a project on Openshift.

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
            # Internal validation function
            cpu_req, cpu_lim, mem_req, mem_lim = self.validate_limits_fields(
                cpu_type, cpu_req, cpu_lim,
                mem_type, mem_req, mem_lim
            )

            # All new values to be add formatted
            new_lim = {'cpu': '{0}'.format(cpu_lim), 'memory': '{0}'.format(mem_lim)}
            new_req = {'cpu': '{0}'.format(cpu_req), 'memory': '{0}'.format(mem_req)}

            for containers in json_data['spec']['template']['spec']['containers']:
                if containers['name'] == dc:
                    if 'resources' not in containers:
                        containers.setdefault('resources', {'requests': {}, 'limits': {}})
                    containers['resources']['limits'] = new_lim
                    containers['resources']['requests'] = new_req
            return json_data

    def edit_route(self, service, tls_enabled, type_tls, json_data):
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

        if tls_enabled:
            json_data['spec']['tls'] = {'termination': type_tls}
        else:
            json_data['spec']['tls'].delete()
        json_data['spec']['to']['name'] = service
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
            if 'livenessProbe' in containers:
                containers['livenessProbe']['httpGet']['path'] = path
                containers['livenessProbe']['httpGet']['port'] = 8080
                containers['livenessProbe']['httpGet']['scheme'] = 'HTTP'
                containers['livenessProbe']['initialDelaySeconds'] = init_delay
                containers['livenessProbe']['timeoutSeconds'] = timeout
                pass
            else:
                containers['livenessProbe'] = {
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
                }
                pass
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
            if 'readinessProbe' in containers:
                containers['readinessProbe']['httpGet']['path'] = path
                containers['readinessProbe']['httpGet']['port'] = 8080
                containers['readinessProbe']['httpGet']['scheme'] = 'HTTP'
                containers['readinessProbe']['initialDelaySeconds'] = init_delay
                containers['readinessProbe']['timeoutSeconds'] = timeout
                pass
            else:
                containers['readinessProbe'] = {
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
                }
                pass
        return json_data
