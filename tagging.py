import collections
import json
import boto3 
from botocore.exceptions import ClientError


ec2 = boto3.resource('ec2')

servers = ec2.instances.all()

tags_to_be_searched = [{'Author': 'Anish'}]

tags_missing_instances = collections.defaultdict(list)

for instance in servers:
    current_instance_tag = instance.tags 
    for tag in tags_to_be_searched:
        if tag not in current_instance_tag:
            instance_url = 'https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#Instances:instanceId=' + str(instance.id)
            tags_missing_instances[instance_url].append(tag)


sender = "anish.k@consultadd.com"
reciever = "anish.k@consultadd.com"
aws_region = "ap-south-1"

subject = "Amazon EC2 instance tags missing notification"

message = """
<html>
<head></head>
<body>
  <h1>Amazon EC2 instance with tags missing</h1>
  <ol>
    {% for instance, tags in tags_missing_instances.items() %}
        <a href={{instance}}></a>
        <p>Missing tags</p>
        <ul>
            {% for tag in tags %}
                <li>{{tag}}</li>
            {% endfor %}
        </ul>
    {% endfor %}
  </ol>
</body>
</html>
"""            

CHARSET = "UTF-8"

client = boto3.client('ses',region_name=aws_region)

try:
    response = client.send_email(
        Destination={
            'ToAddresses': [
                reciever,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Data': message
                }
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': subject,
            },
        },
        Source=sender
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! With Message ID:", response['MessageId'])
