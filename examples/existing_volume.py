"""
This example showcases how Hera supports mounting existing volumes. These volumes are expected to already be
provisioned and available as a persistent volume claim in the K8S cluster where Argo runs.
"""
from hera.v1.existing_volume import ExistingVolume
from hera.v1.resources import Resources
from hera.v1.task import Task
from hera.v1.workflow import Workflow
from hera.v1.workflow_service import WorkflowService


def download(path: str):
    # we can run this task asynchronously for downloading some big file to an existing volume!
    print(f'Would have downloaded from {path} to /vol')


# TODO: replace the domain and token with your own
ws = WorkflowService('my-argo-server.com', 'my-auth-token')
w = Workflow('download-to-volume', ws)
d = Task(
    'download',
    download,
    [{'path': '/whatever/path'}],
    resources=Resources(existing_volume=ExistingVolume(name='my-vol-claim', mount_path='/vol')),
)

w.add_task(d)
w.submit()
