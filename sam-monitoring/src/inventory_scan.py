import jinja2
import boto3
import os
import json

config = boto3.client("config")
cloudformation = boto3.client("cloudformation")

STACK_NAME = os.environ["STACK_NAME"]
EMERGENCY_TOPIC = os.environ["EMERGENCY_TOPIC"]
QUERY_INSTANCE_IDS_OF_RUNNING_EC2S = """
SELECT
  resourceId,
  resourceName,
  resourceType,
  configuration.instanceType,
  tags,
  availabilityZone,
  configuration.state.name
WHERE
  resourceType = 'AWS::EC2::Instance'
  AND configuration.state.name = 'running'"""
CREATE_CW_ALARMS = "CreateCWAlarms.j2"


def query_running_ec2s(event, _):
    query = config.select_resource_config(Expression=QUERY_INSTANCE_IDS_OF_RUNNING_EC2S)
    results = query["Results"]
    ids = []
    for r in results:
        instance_data = json.loads(r)
        ids.append(instance_data["resourceId"])
    return ids


def parse_template(file, instance_ids):
    with open(file) as file_:
        template = jinja2.Template(file_.read())
    rendered_doc = template.render(
        instance_ids=instance_ids, EMERGENCY_TOPIC=EMERGENCY_TOPIC
    )
    return rendered_doc


def create_cloudformation(template_body):
    cloudformation.create_stack(
        StackName=STACK_NAME,
        TemplateBody=template_body,
        Tags=[
            {"Key": "string", "Value": "string"},
        ],
    )


def update_cloudformation(template_body):
    cloudformation.update_stack(
        StackName=STACK_NAME,
        TemplateBody=template_body,
        Tags=[
            {"Key": "string", "Value": "string"},
        ],
    )


def handler(event, context):
    instance_ids = query_running_ec2s(event, context)
    # Prepare a CloudFormation stack
    template_body = parse_template(CREATE_CW_ALARMS, instance_ids)
    # Deploy CloudFormation stack
    try:
        create_cloudformation(template_body)
    except cloudformation.exceptions.AlreadyExistsException:
        update_cloudformation(template_body)
    except Exception:
        raise