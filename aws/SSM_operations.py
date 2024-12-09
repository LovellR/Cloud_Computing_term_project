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

def able_SSM(instance_id):
    try:
        ec2 = boto3.client('ec2')
        instance_profile_name = 'SSM'
        response = ec2.associate_iam_instance_profile(
            IamInstanceProfile={'Name': instance_profile_name},
            InstanceId=instance_id
        )
        print(f"Successfully associated IAM Instance Profile '{instance_profile_name}' with instance '{instance_id}'.")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error associating IAM Instance Profile: {e}")

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

def execute_command(ssm, instance_id):
    command = input("Enter the command to execute: ").strip()
    if not command:
        print("Command cannot be empty!")
        return
    print(f"Executing command '{command}' on instance {instance_id}...")
    try:
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": [command]}
        )
        command_id = response['Command']['CommandId']
        print(f"Command sent! Command ID: {command_id}")

        time.sleep(2)  # Adjust wait time as needed

        output = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id
        )
        print("Command Output:")
        print(output['StandardOutputContent'])
        print("Error Output:")
        print(output['StandardErrorContent'])
    except Exception as e:
        print(f"Error executing custom command: {str(e)}")

def SSM_operations_menu(ec2, ssm):
    while True:
        print("\n------------------------------------------------------------")
        print("                 Amazon AWS Control Panel                   ")
        print("------------------------------------------------------------")
        print("  1. condor_status                2. Enable_SSM(IAM role)   ")
        print("  3. Execute Command                                        ")
        print("                                 99. back to menu           ")
        print("------------------------------------------------------------")

        try:
            number = int(input("Enter an integer: "))
        except ValueError:
            print("Invalid input!")
            continue

        if number == 99:
            break
        elif number == 1:
            instance_id = input("Enter instance ID: ").strip()
            if instance_id:
                execute_condor_status(ssm, instance_id)
        elif number == 2:
            instance_id = input("Enter instance ID: ").strip()
            if instance_id:
                able_SSM(instance_id)
        elif number == 3:
            instance_id = input("Enter instance ID: ").strip()
            if instance_id:
                execute_command(ssm, instance_id)
        else:
            print("Invalid option!")