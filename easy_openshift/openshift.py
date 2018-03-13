""" Openshift-Module

What it is?
    This module has purpose to create easy and fast ways to communicate with the
    API/OAPI from Openshift, allowing the developer to create and manage their own
    data with their own way.

Why?
    Python is a great language and very well used for DevOps Automantions. With it,
    creating a Openshift module will easy many steps and automantions allowing a
    better infrastructure automation or management with great performance.

Usage:
    To use this module, just import this module and create a new instance of it.
    If you need CRUD functions for those API/OAPI methods, you can import the
    extension class of this module, named 'OpenshiftTools'.

Original Authors:
    - Gustavo Toledo de Oliveira
        Email: gustavot53@gmail.com

Contribuitors:
    - <some-one>

Observations:
    Since this module going open-source, if you want to contribuite with some
    functions or a function improvement, please, put your name on 'Contribuitors'
    section.

    Ps: Keep the code very well documented, that's an order!

"""
import base64
import json
import requests

# Disable warning messages
requests.packages.urllib3.disable_warnings()


class Openshift:

    # ============================================================================== #
    #   Constructor                                                                  #
    #   Let's keep it empty!                                                         #
    # ============================================================================== #
    #
    def __init__(self):
        pass

    # ============================================================================== #
    #   Methods/Functions                                                            #
    #   Where all the magic is located                                               #
    # ============================================================================== #
    #
    def api_comunicator(type_action):
        def action_decotator(func):
            def func_wrapper(*args):
                """
                    Function to run any communication with the API throughout
                    the requests module.

                :param args: All required arguments to run a certain action.
                The required args are: 'host', 'project', 'token', 'json_data',

                :return: Return a JSON with data required or some confirmation.
                """
                try:
                    host = func(*args)[1]
                    token = func(*args)[2]
                    json_config = func(*args)[3]

                    if type_action in ["get", "put", "patch", "post", "delete"]:
                        if type_action == "get":
                            header = {'Accept': 'application/json', 'Authorization': 'Bearer {0}'.format(token)}
                            response = requests.get(host, verify=False, headers=header)
                            return json.loads(response.content)

                        elif type_action == "patch":
                            header = {'Accept': 'application/json', 'Content-Type': 'application/merge-patch+json',
                                      'Authorization': 'Bearer {0}'.format(token)}
                            response = requests.patch(host, verify=False, headers=header, json=json_config)
                            return json.loads(response.content)

                        elif type_action == "put":
                            header = {'Accept': 'application/json', 'Content-Type': 'application/json',
                                      'Authorization': 'Bearer {0}'.format(token)}
                            response = requests.put(host, verify=False, headers=header, json=json_config)
                            return json.loads(response.content)

                        elif type_action == "post":
                            header = {'Accept': 'application/json', 'Content-Type': 'application/json',
                                      'Authorization': 'Bearer {0}'.format(token)}
                            response = requests.post(host, verify=False, headers=header, json=json_config)
                            return json.loads(response.content)

                        elif type_action == "delete":
                            pass

                    else:
                        print("==> Invalid type of action! ({0})".format(type_action))
                        exit(1)

                except (ConnectionError, TimeoutError, ValueError, SystemError) as corno:
                    print("==> Erro: {0}".format(corno))
                    exit(1)

            return func_wrapper

        return action_decotator

    def get_login_token(self, host, userdata):
        """
            Method to retrieve user token, required to run all others methods on Openshift class.

        :param host:        Openshift hostname to query.
        :param userdata:    User and password to login on Openshift.
        :return:            return the token in string format.
        """

        try:
            userpass = base64.b64encode(userdata)
            auth = 'Basic ' + userpass.decode()

            host += '/oauth/authorize?response_type=token&client_id=openshift-challenging-client'

            header = {'content-type': 'application/json', 'Authorization': auth, 'X-Csrf-Token': '1'}

            # Get token
            response = requests.get(host, verify=False, headers=header)

            # Save data
            data = str(response.url)

            # Find token in response
            value = data.find('_token') + 7
            data = data[value:]
            value = data.find('expires') - 1
            token = data[:value]

            # Return token
            return token

        except (ConnectionError, TimeoutError, ValueError, EOFError) as corno:
            raise corno

    # ============================================================================== #
    #   Functions to retrieve data from openshift API                                #
    #   session to create all GET functions of this class                            #
    # ============================================================================== #
    # Functions to catch all
    #
    @api_comunicator("get")
    def get_projects(self, host, token):
        """
            Method to get all projects on Openshift.

        :param host:        Openshift hostname.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/projects/'
        return self, host, token, None

    @api_comunicator("get")
    def get_services(self, host, project, token):
        """
            Method to get the services from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/api/v1/namespaces/{0}/services'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_deploymentconfigs(self, host, project, token):
        """
            Method to get all DeploymentConfigs from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/oapi/v1/namespaces/{0}/deploymentconfigs'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_deploymentconfigs_logs(self, host, project, token):
        """
            Method to get all logs from the DeploymentConfigs.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/oapi/v1/namespaces/{0}/log'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_deploymentconfigs_scale(self, host, project, token):
        """
            Method to get all scales from the DeploymentConfigs.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/oapi/v1/namespaces/{0}/scale'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_pods(self, host, project, token):
        """
            Method to get all pods from a project and their status.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/api/v1/namespaces/{0}/pods'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_events(self, host, project, token):
        """
            Method to get all events from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/api/v1/namespaces/{0}/events'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_routes(self, host, project, token):
        """
            Method to get all routes from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/oapi/v1/namespaces/{0}/routes'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_project_quotas(self, host, project, token):
        """
            Method to get all quotas configured in a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/api/v1/namespaces/{0}/resourcequotas'.format(project)
        return self, host, token, None

    # ============================================================================== #
    # Functions to get specific ones
    #
    @api_comunicator("get")
    def get_project(self, host, project, token):
        """
            Method to get a specific project on Openshift.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/projects/{0}'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_deploymentconfig(self, host, project, token, name):
        """
            Method to get a specified DeploymentConfig.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param name:        Name of the specified DeploymentConfig.
        :return:            Return a JSON with all information about.
        """

        host += '/oapi/v1/namespaces/{0}/deploymentconfigs/{1}'.format(project, name)
        return self, host, token, None

    @api_comunicator("get")
    def get_deploymentconfig_scale(self, host, project, token, name):
        """
            Method to get a specified scale of deploymentconfig

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param name:        Name of the specified DeploymentConfig.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/deploymentconfigs/{1}/scale'.format(project, name)
        return self, host, token, None

    @api_comunicator("get")
    def get_deploymentconfig_autoscale(self, host, project, token, dc):
        """
            Function to return HPA data from a deploymentconfig

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param dc:          Specific name of the deployment-config.
        :return:            Return a JSON with all information about.
        """
        host += '/apis/autoscaling/v1/namespaces/{0}/horizontalpodautoscalers/{1}'.format(project, dc)
        return self, host, token, None

    @api_comunicator("get")
    def get_project_quota(self, host, project, token, name):
        """
            Method to get all quotas configured in a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/api/v1/namespaces/{0}/resourcequotas/{1}'.format(project, name)
        return self, host, token, None

    # ============================================================================== #
    # Functions to list/get specific or many datas
    #
    @api_comunicator("get")
    def list_deploymentconfig(self, host, project, token):
        """

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/deploymentconfigs'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def list_deploymentconfigs(self, host, token):
        """

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/deploymentconfigs'
        return self, host, token, None

    # ============================================================================== #
    # Functions to get specific data
    #
    @api_comunicator("get")
    def get_rolebindings(self, host, project, token):
        """
            Method to get all rolebindings from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/oapi/v1/namespaces/{0}/rolebindings'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_configmap(self, host, project, token):
        """
            Method to get all configmaps (include replaces) from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """
        host += '/api/v1/namespaces/{0}/configmaps'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_endpoints(self, host, project, token):
        """
            Method to get all endpoints from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """

        host += '/api/v1/namespaces/{0}/endpoints'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_egressnetworkpolicies(self, host, project, token):
        """
            Method to get all egress-network-policies from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/egressnetworkpolicies'.format(project)
        return self, host, token, None

    @api_comunicator("get")
    def get_egressnetworkpolicy_specific(self, host, project, token, name):
        """
            Method to get a specific egress-network-policies from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param name:        Specific name of the egress-network-policies
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/egressnetworkpolicies/{1}'.format(project, name)
        return self, host, token, None

    # ============================================================================== #
    #   Functions to send data from openshift API                                    #
    #   session to create all PATCH functions of this class                          #
    # ============================================================================== #
    #
    @api_comunicator("patch")
    def update_deploymentconfig(self, host, project, token, dc, json_file):
        """
            Method to update a specified DeploymentConfig from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param dc:          Specific name of the deployment-config.
        :param json_file:   variable with all json formatted and ready to push to API/OAPI.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/deploymentconfigs/{1}'.format(project, dc)
        return self, host, token, json_file

    @api_comunicator("patch")
    def update_deploymentconfig_route(self, host, project, token, dc, json_file):
        """
             Method to update a specified DeploymentConfig from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param dc:          Specific name of the deployment-config.
        :param json_file:   variable with all json formatted and ready to push to API/OAPI.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/routes/{1}'.format(project, dc)
        return self, host, token, json_file

    @api_comunicator("patch")
    def update_deploymentconfig_scale(self, host, project, token, dc, json_file):
        """
             Method to update a specified DeploymentConfig from a project.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param dc:          Specific name of the deployment-config.
        :param json_file:   variable with all json formatted and ready to push to API/OAPI.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/deploymentconfigs/{1}/scale'.format(project, dc)
        return self, host, token, json_file

    @api_comunicator("patch")
    def update_deploymentconfig_autoscaler(self, host, project, token, dc, json_file):
        """
            Function to return HPA data from a deploymentconfig

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param dc:          Specific name of the deployment-config.
        :param json_file:   variable with all json formatted and ready to push to API/OAPI.
        :return:            Return a JSON with all information about.
        """
        host += '/apis/autoscaling/v1/namespaces/{0}/horizontalpodautoscalers/{1}'.format(project, dc)
        return self, host, token, json_file


    # ============================================================================== #
    #   Functions to send data from openshift API                                    #
    #   session to create all POST functions of this class                           #
    # ============================================================================== #
    #
    @api_comunicator("post")
    def set_project(self, host, project, token, json_file):
        """
            Not tested
        """
        host += '/oapi/v1/projects/{0}'.format(project)
        return self, host, token, json_file

    @api_comunicator("post")
    def set_deploymentconfig_autoscaler(self, host, project, token, json_file):
        """
            Not tested
        """
        host += '/apis/autoscaling/v1/namespaces/{0}/horizontalpodautoscalers'.format(project)
        return self, host, token, json_file

    # ============================================================================== #
    #   Functions to send data from openshift API                                    #
    #   session to create all PUT functions of this class                            #
    # ============================================================================== #
    #
    @api_comunicator("put")
    def create_deploymentconfig_autoscaler(self, host, project, token, dc, json_file):
        """
            Not tested
        """
        host += '/apis/autoscaling/v1/namespaces/{0}/horizontalpodautoscalers'.format(project, dc)
        return self, host, token, json_file

    @api_comunicator("put")
    def create_deploymentconfig_scale(self, host, project, token, dc, json_file):
        """
            Method to create or update a scale from a deploymentconfig.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param dc:          Name of the deploymentconfig in openshift project.
        :param json_file:   Variable with all json formatted and ready to push to API/OAPI.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/deploymentconfigs/{1}/scale'.format(project, dc)
        return self, host, token, json_file

    @api_comunicator("put")
    def create_route(self, host, project, token, json_file):
        """
            Method to create or update a route from a project.
            if exists, update only a few informations like tls and service.
            (hostname and name are blocked like the webui)

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param json_file:   Variable with all json formatted and ready to push to API/OAPI.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/routes'.format(project)
        return self, host, token, json_file

    # ============================================================================== #
    #   Functions to send data from openshift API                                    #
    #   session to create all DELETE functions of this class                            #
    # ============================================================================== #
    #
    @api_comunicator("delete")
    def __delete_deploymentconfig_scale(self, host, project, token, dc, json_file):
        """
            NOT TESTED.

        :param host:        Openshift hostname.
        :param project:     Project name on Openshift.
        :param token:       User token to communicate with OAPI/API.
        :param dc:          Name of the deploymentconfig in openshift project.
        :param json_file:   Variable with all json formatted and ready to push to API/OAPI.
        :return:            Return a JSON with all information about.
        """
        host += '/oapi/v1/namespaces/{0}/deploymentconfigs/{1}/scale'.format(project, dc)
        return self, host, token, json_file


