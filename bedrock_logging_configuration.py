import boto3

REGION="us-east-1"
bedrock = boto3.client("bedrock", region_name=REGION)
cf = boto3.client("cloudformation", region_name=REGION)

STACK_NAME = "bedrock-logging"
log_group_name = None
log_role_arn = None
bucket_name = None

# with open('bedrock-logging.yml', 'r') as cfn_template:
#     template_body = yaml.safe_load(cfn_template)
#     response = cf.create_stack(
#         StackName=STACK_NAME,
#         TemplateBody=yaml.dump(template_body),
#         Capabilities=["NAMED_IAM_CAPABILITIES"],
#         Tags=[
#             {
#                 'Key': 'PrimaryOwner',
#                 'Value': 'stewmi@amazon.com'
#             },
#             {
#                 'Key': 'SecondaryOwner',
#                 'Value': 'stewmi@amazon.com'
#             },
#             {
#                 'Key': 'Name',
#                 'Value': 'Bedrock Logging'
#             },
#             {
#                 'Key': 'CostCenterID',
#                 'Value': '00000'
#             }
#         ]
#     )
# waiter = boto3.get_waiter("stack_create_complete")
# waiter.wait(StackName=STACK_NAME)

stack_details = cf.describe_stacks(StackName=STACK_NAME)
for output in stack_details['Stacks'][0]['Outputs']:
    if output['OutputKey'] == "LogGroupName":
        log_group_name = output['OutputValue']
    if output['OutputKey'] == "LogRoleArn":
        log_role_arn = output['OutputValue']
    if output['OutputKey'] == "Bucket":
        bucket_name = output['OutputValue']


response = bedrock.put_model_invocation_logging_configuration(
    loggingConfig={
        'cloudWatchConfig': {
            'logGroupName': log_group_name,
            'roleArn': log_role_arn,
            'largeDataDeliveryS3Config': {
                'bucketName': bucket_name,
                'keyPrefix': 'bedrock'
            }
        },
        's3Config': {
            'bucketName': bucket_name,
            'keyPrefix': 'bedrock'
        },
        'textDataDeliveryEnabled': True,
        'imageDataDeliveryEnabled': True,
        'embeddingDataDeliveryEnabled': True
    }
)
print(response)