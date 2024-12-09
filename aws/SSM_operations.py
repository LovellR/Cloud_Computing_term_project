import boto3
import time

def init_ssm():
    try:
        session = boto3.Session(profile_name='default')
        ssm = session.client('ssm', region_name='us-east-1')
        return ssm
    except Exception as e:
        print(f"Error initializing SSM: {str(e)}")
        exit()

def execute_condor_status(ssm, instance_id):
    print(f"Executing 'condor_status' on instance {instance_id}...")
    try:
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": ["condor_status"]}
        )
        command_id = response['Command']['CommandId']
        print(f"Command sent! Command ID: {command_id}")

        time.sleep(1)  # Adjust wait time as needed

        output = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id
        )
        print("Command Output:")
        print(output['StandardOutputContent'])
        print("Error Output:")
        print(output['StandardErrorContent'])
    except Exception as e:
        print(f"Error: {str(e)}")
