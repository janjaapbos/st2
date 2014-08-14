import httplib
from pecan import abort
from pecan.rest import RestController

from wsme import types as wstypes
import wsmeext.pecan as wsme_pecan

from st2common import log as logging
from st2common.exceptions.db import StackStormDBObjectNotFoundError
from st2common.models.base import jsexpose
from st2common.models.api.action import RunnerTypeAPI
from st2common.persistence.action import RunnerType
from st2common.util.action_db import get_runnertype_by_id


LOG = logging.getLogger(__name__)


class RunnerTypesController(RestController):
    """
        Implements the RESTful web endpoint that handles
        the lifecycle of an RunnerType in the system.
    """

    @staticmethod
    def __get_by_id(id):
        try:
            return RunnerType.get_by_id(id)
        except (ValueError, ValidationError) as e:
            msg = 'Database lookup for id="%s" resulted in exception. %s' % (id, e.message)
            LOG.exception(msg)
            abort(httplib.NOT_FOUND, msg)

    @staticmethod
    def __get_by_name(name):
        try:
            return [RunnerType.get_by_name(name)]
        except ValueError as e:
            LOG.debug('Database lookup for name="%s" resulted in exception : %s.', name, e)
            return []

    @jsexpose(str)
    def get_one(self, id):
        """
            List RunnerType objects by id.

            Handle:
                GET /runnertypes/1
        """
        LOG.info('GET /runnertypes/ with id=%s', id)
        runnertype_db = RunnerTypesController.__get_by_id(id)
        runnertype_api = RunnerTypeAPI.from_model(runnertype_db)
        LOG.debug('GET /runnertypes/ with id=%s, client_result=%s', id, runnertype_api)
        return runnertype_api

    @jsexpose(str)
    def get_all(self, name=None):
        """
            List all RunnerType objects.

            Handles requests:
                GET /runnertypes/
        """
        LOG.info('GET all /runnertypes/ and name=%s', str(name))
        runnertype_dbs = (RunnerType.get_all() if name is None else
                          RunnerTypesController.__get_by_name(name))
        runnertype_apis = [RunnerTypeAPI.from_model(runnertype_db)
                           for runnertype_db in runnertype_dbs]
        LOG.debug('GET all /runnertypes/ client_result=%s', runnertype_apis)
        return runnertype_apis

    @jsexpose(body=RunnerTypeAPI, status_code=httplib.NOT_IMPLEMENTED)
    def post(self, runnertype):
        """
            Update not supported for RunnerType.

            Create a new RunnerType object.

            Handles requests:
                POST /runnertypes/
        """

        abort(httplib.NOT_IMPLEMENTED)

    @jsexpose(str, body=RunnerTypeAPI, status_code=httplib.NOT_IMPLEMENTED)
    def put(self, runnertype):
        """
            Update not supported for RunnerType.

            Handles requests:
                POST /runnertypes/1?_method=put
                PUT /runnertypes/1
        """

        abort(httplib.METHOD_NOT_ALLOWED)

    @jsexpose(status_code=httplib.NOT_IMPLEMENTED)
    def delete(self):
        """
            Delete an RunnerType.

            Handles requests:
                POST /runnertypes/1?_method=delete
                DELETE /runnertypes/1
        """

        # TODO: Support delete by name
        abort(httplib.NOT_IMPLEMENTED)
